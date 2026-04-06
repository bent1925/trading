#!/usr/bin/env python3
"""
Kalshi Sports Trading Bot
=========================
- Finds sports game markets (NBA, MLB, NHL, WTA, ATP) closing today
- Builds an independent win-probability model from ESPN's public API
  (consensus sportsbook money-lines when available; season-record ratio otherwise)
- Only trades when Polymarket has a matching market (cross-market arb signal)
- Buys "yes" when Polymarket > kalshi_mid + 10pp (Kalshi underprices relative to Polymarket)
- Buys "no"  when Polymarket < kalshi_mid - 10pp
- Max 10 trades/day, proportional sizing ($10 at 10pp edge → $20 at 20pp+)
- Logs every execution to kalshi_trades.json

Usage:
    python3 kalshi_sports_bot.py            # live run
    python3 kalshi_sports_bot.py --dry-run  # show opportunities without placing orders
"""

import os
import sys
import json
import uuid
import base64
import logging
import datetime
import time
import re
from difflib import SequenceMatcher
from typing import Optional

import requests
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# ─── Configuration ──────────────────────────────────────────────────────────

KALSHI_BASE_URL = "https://api.elections.kalshi.com"
KALSHI_KEY_ID   = os.environ.get("KALSHI_KEY_ID", "")
KALSHI_KEY_FILE = os.environ.get("KALSHI_KEY_FILE", "")

MAX_TRADES_PER_RUN = 10
MIN_EDGE_PP          = 10.0    # minimum |kalshi_mid - model_prob| in pp to trade
TRADE_HORIZON_HOURS  = 3      # only trade events starting within this many hours

# Inverse sizing: budget scales down as edge grows (large edge = model likely wrong)
BASE_BUDGET        = 20.00
BASE_EDGE_PP       = 5.0
MIN_BUDGET         = 1.00

TRADE_LOG_FILE     = "kalshi_trades.json"

ESPN_BASE = "http://site.api.espn.com/apis/site/v2/sports"

# Series tickers to scan → (espn_sport_path, espn_league_path)
SPORTS_SERIES = {
    "KXNBAGAME":  ("basketball", "nba"),
    "KXMLBGAME":  ("baseball",   "mlb"),
    "KXNHLGAME":  ("hockey",     "nhl"),
    "KXWTAMATCH": ("tennis",     "wta"),
    "KXATPMATCH": ("tennis",     "atp"),
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ─── Kalshi Auth & Client ───────────────────────────────────────────────────

class KalshiClient:
    def __init__(self, key_id: str, key_file: str, base_url: str = KALSHI_BASE_URL):
        self.key_id   = key_id
        self.base_url = base_url
        with open(key_file, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(), password=None, backend=default_backend()
            )

    def _auth_headers(self, method: str, path: str) -> dict:
        # Use time.time() — avoids the naive-datetime-as-local-time pitfall
        ts  = str(int(time.time() * 1000))
        msg = ts + method.upper() + path.split("?")[0]
        sig = self._sign_pss(msg)
        return {
            "KALSHI-ACCESS-KEY":       self.key_id,
            "KALSHI-ACCESS-SIGNATURE": sig,
            "KALSHI-ACCESS-TIMESTAMP": ts,
            "Content-Type":            "application/json",
        }

    def _sign_pss(self, text: str) -> str:
        sig = self.private_key.sign(
            text.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.DIGEST_LENGTH,
            ),
            hashes.SHA256(),
        )
        return base64.b64encode(sig).decode("utf-8")

    def get(self, path: str, params: dict = None) -> dict:
        url = self.base_url + path
        r   = requests.get(url, headers=self._auth_headers("GET", path),
                           params=params, timeout=15)
        r.raise_for_status()
        return r.json()

    def post(self, path: str, body: dict) -> dict:
        url = self.base_url + path
        r   = requests.post(url, headers=self._auth_headers("POST", path),
                            json=body, timeout=15)
        r.raise_for_status()
        return r.json()

    def delete(self, path: str) -> dict:
        url = self.base_url + path
        r   = requests.delete(url, headers=self._auth_headers("DELETE", path),
                              timeout=15)
        r.raise_for_status()
        return r.json()

    def get_open_orders(self) -> list[dict]:
        """Returns all resting (open) orders."""
        data = self.get("/trade-api/v2/portfolio/orders", params={"status": "resting"})
        return data.get("orders", [])

    def cancel_order(self, order_id: str) -> dict:
        return self.delete(f"/trade-api/v2/portfolio/orders/{order_id}")

    # ── Public helpers ──────────────────────────────────────────────────────

    def get_balance_usd(self) -> float:
        data = self.get("/trade-api/v2/portfolio/balance")
        # balance is in cents
        return data["balance"] / 100.0

    def get_todays_game_markets(self) -> list[dict]:
        """
        Returns open single-game markets whose game date is TODAY.
        Uses the date encoded in the Kalshi ticker (e.g. KXNBAGAME-26MAR26NYKCHA
        encodes 26 MAR 2026) as the authoritative filter.
        """
        today   = datetime.date.today()
        markets = []

        for series_ticker in SPORTS_SERIES:
            cursor = None
            while True:
                params = {"status": "open", "series_ticker": series_ticker,
                          "limit": 200}
                if cursor:
                    params["cursor"] = cursor
                try:
                    data = self.get("/trade-api/v2/markets", params=params)
                except requests.HTTPError as e:
                    log.warning(f"HTTP error fetching {series_ticker}: {e}")
                    break

                for m in data.get("markets", []):
                    game_date = _parse_ticker_date(series_ticker,
                                                   m.get("ticker", ""))
                    if game_date == today:
                        m["_series"] = series_ticker
                        markets.append(m)

                cursor = data.get("cursor")
                if not cursor:
                    break

        return markets

    def place_order(self, ticker: str, side: str, price_cents: int,
                    count: int) -> dict:
        """
        Place a limit buy order.
        side        : "yes" or "no"
        price_cents : limit price in integer cents (1-99)
        count       : number of contracts
        """
        body = {
            "ticker":           ticker,
            "client_order_id":  str(uuid.uuid4()),
            "action":           "buy",
            "side":             side,
            "type":             "limit",
            "count":            count,
        }
        if side == "yes":
            body["yes_price"] = price_cents
        else:
            body["no_price"]  = price_cents
        return self.post("/trade-api/v2/portfolio/orders", body)


# ─── Polymarket Source ───────────────────────────────────────────────────────

class PolymarketSource:
    """
    Fetches active market prices from Polymarket's public Gamma API (no API key).
    Used as a second market-consensus signal alongside the ESPN model.
    """
    GAMMA_URL = "https://gamma-api.polymarket.com/markets"

    # Words that disqualify a Polymarket market for a given league.
    # Prevents cross-sport matches (e.g. NBA team names matching MLS draw markets).
    _BLOCKLIST: dict = {
        "nba":  {"draw", "soccer", "mls", "nhl", "hockey", "tennis", "wta", "atp", "baseball", "mlb", "nfl", "football"},
        "nhl":  {"draw", "soccer", "mls", "nba", "basketball", "tennis", "wta", "atp", "baseball", "mlb", "nfl", "football"},
        "mlb":  {"draw", "soccer", "mls", "nba", "basketball", "tennis", "wta", "atp", "nhl", "hockey", "nfl", "football"},
        "wta":  {"draw", "soccer", "mls", "nba", "basketball", "nhl", "hockey", "baseball", "mlb", "nfl", "football"},
        "atp":  {"draw", "soccer", "mls", "nba", "basketball", "nhl", "hockey", "baseball", "mlb", "nfl", "football"},
    }

    def _search(self, query: str) -> list:
        """Search Polymarket for markets matching query."""
        try:
            r = requests.get(
                self.GAMMA_URL,
                params={"active": "true", "closed": "false",
                        "limit": 50, "q": query},
                timeout=15,
            )
            r.raise_for_status()
            batch = r.json()
            return batch if isinstance(batch, list) else []
        except Exception as e:
            log.warning(f"Polymarket search ('{query}'): {e}")
            return []

    def get_prob(self, yes_team: str, other_team: str,
                 league: str = "") -> Optional[tuple]:
        """
        Returns (prob_yes_team_wins: float, matched_question: str) or None.
        Searches Polymarket with each team name, applies blocklist filtering,
        then selects the best fuzzy match across both result sets.
        """
        yes_w     = set(_words(yes_team))
        other_w   = set(_words(other_team))
        blocklist = self._BLOCKLIST.get(league, set())
        if not yes_w or not other_w:
            return None

        best_m, best_score = None, 0
        seen: set = set()
        for search_term in [yes_team, other_team]:
            for m in self._search(search_term):
                mid = m.get("id") or m.get("conditionId", "")
                if mid in seen:
                    continue
                seen.add(mid)
                q_w = set(_words(m.get("question", "")))
                if blocklist & q_w:
                    continue
                y_hit = len(yes_w   & q_w)
                o_hit = len(other_w & q_w)
                if y_hit == 0 or o_hit == 0:
                    continue
                score = y_hit + o_hit
                if score > best_score:
                    best_score, best_m = score, m

        if best_m is None or best_score < 2:
            return None

        try:
            prices   = json.loads(best_m.get("outcomePrices", "[]"))
            outcomes = json.loads(best_m.get("outcomes", "[]"))
        except (json.JSONDecodeError, TypeError):
            return None
        if len(prices) < 2:
            return None

        p0 = float(prices[0])   # probability that outcomes[0] occurs
        question = best_m.get("question", "")

        # Check if outcomes explicitly name a team (not just "Yes"/"No")
        out0_w = set(_words(outcomes[0])) if outcomes else set()
        out1_w = set(_words(outcomes[1])) if len(outcomes) > 1 else set()
        if yes_w & out0_w:
            return (p0, question)
        if yes_w & out1_w:
            return (1.0 - p0, question)

        # Outcomes are Yes/No — whichever team appears first in the question
        # is the subject of "Yes"
        q_lower = question.lower()
        first_yes   = min((q_lower.find(w) for w in yes_w   if w in q_lower), default=9999)
        first_other = min((q_lower.find(w) for w in other_w if w in q_lower), default=9999)
        if first_yes == 9999 and first_other == 9999:
            return None
        if first_yes <= first_other:
            return (p0, question)
        return (1.0 - p0, question)


# ─── ESPN Probability Model ─────────────────────────────────────────────────

class ProbabilityModel:
    """
    Fetches today's game data from ESPN's unofficial public API.
    Priority:
      1. Consensus money-line odds embedded in ESPN response → de-vigged prob
      2. Season win-rate ratio with home-court/home-ice advantage
    Returns a dict keyed by (home_display_name, away_display_name).
    """

    def _fetch_scoreboard(self, sport: str, league: str,
                          date_str: str) -> list[dict]:
        url = f"{ESPN_BASE}/{sport}/{league}/scoreboard"
        try:
            r = requests.get(url, params={"dates": date_str}, timeout=10)
            r.raise_for_status()
            return r.json().get("events", [])
        except Exception as e:
            log.warning(f"ESPN {sport}/{league} error: {e}")
            return []

    @staticmethod
    def _ml_to_implied(ml: float) -> float:
        """American money-line → implied probability (includes vig)."""
        if ml > 0:
            return 100.0 / (ml + 100.0)
        return abs(ml) / (abs(ml) + 100.0)

    @staticmethod
    def _record_win_pct(competitor: dict) -> Optional[float]:
        """
        Returns season win percentage, or None if fewer than 5 games played.
        ESPN encodes records as a summary string "W-L[-OT]" (e.g. "38-34" or "28-40-8").
        """
        for rec in competitor.get("records", []):
            if rec.get("type") == "total":
                summary = rec.get("summary", "")
                m = re.match(r"^(\d+)-(\d+)", summary)
                if m:
                    w, l = int(m.group(1)), int(m.group(2))
                    if w + l >= 5:
                        return w / (w + l)
        return None

    @staticmethod
    def _recent_form_pct(competitor: dict) -> Optional[float]:
        """
        Returns win percentage over the last 10 games, or None if not available.
        ESPN exposes this as record type "lastTen" (NBA) or "last10" (some leagues).
        """
        for rec in competitor.get("records", []):
            if rec.get("type") in ("lastTen", "last10"):
                summary = rec.get("summary", "")
                m = re.match(r"^(\d+)-(\d+)", summary)
                if m:
                    w, l = int(m.group(1)), int(m.group(2))
                    if w + l > 0:
                        return w / (w + l)
        return None

    def _parse_event(self, event: dict, sport: str,
                     league: str) -> Optional[dict]:
        """
        Returns a game record or None.
        {home, away, prob_home, prob_away, sport, league, source}
        """
        comps = event.get("competitions", [])
        if not comps:
            return None
        comp        = comps[0]
        competitors = comp.get("competitors", [])
        if len(competitors) < 2:
            return None

        home = next((c for c in competitors if c.get("homeAway") == "home"),
                    competitors[0])
        away = next((c for c in competitors if c.get("homeAway") == "away"),
                    competitors[1])

        home_name = home.get("team", {}).get("displayName", "")
        away_name = away.get("team", {}).get("displayName", "")
        if not home_name or not away_name:
            return None

        # 1. Try sportsbook money-line odds from ESPN
        for odds in comp.get("odds", []):
            hml = odds.get("homeTeamOdds", {}).get("moneyLine")
            aml = odds.get("awayTeamOdds", {}).get("moneyLine")
            if hml is not None and aml is not None:
                hi = self._ml_to_implied(float(hml))
                ai = self._ml_to_implied(float(aml))
                total = hi + ai
                if total > 0:
                    return dict(home=home_name, away=away_name,
                                prob_home=hi/total, prob_away=ai/total,
                                sport=sport, league=league,
                                source="espn_odds",
                                start_time=comp.get("date", ""))

        # 2. Fallback: season win-rate blended with recent form + home advantage
        h_season = self._record_win_pct(home)
        a_season = self._record_win_pct(away)
        if h_season is None and a_season is None:
            return None   # no basis for a model estimate

        h_form = self._recent_form_pct(home)
        a_form = self._recent_form_pct(away)

        # Blend season + recent form (60/40) when last-10 is available
        def _blend(season: Optional[float], form: Optional[float]) -> float:
            if season is None and form is None:
                return 0.5
            if season is None:
                return form
            if form is None:
                return season
            return 0.6 * season + 0.4 * form

        h_pct = _blend(h_season, h_form)
        a_pct = _blend(a_season, a_form)
        total  = h_pct + a_pct
        p_home = (h_pct / total) if total > 0 else 0.5
        HOME_EDGE = 0.04 if league not in ("wta", "atp") else 0.0
        p_home = min(0.95, max(0.05, p_home + HOME_EDGE))
        source = "win_pct+form" if (h_form is not None or a_form is not None) else "win_pct"
        return dict(home=home_name, away=away_name,
                    prob_home=p_home, prob_away=1.0 - p_home,
                    sport=sport, league=league, source=source,
                    start_time=comp.get("date", ""))

    # ── Tennis: ranking-based model ─────────────────────────────────────────

    def _fetch_tennis_rankings(self, league: str) -> dict[str, int]:
        """
        Returns {player_display_name → world_rank} for top-200 players.
        Uses ESPN's /rankings endpoint.
        """
        url = f"{ESPN_BASE}/tennis/{league}/rankings"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        except Exception as e:
            log.warning(f"Tennis rankings fetch ({league}) failed: {e}")
            return {}
        out = {}
        for ranking_group in r.json().get("rankings", []):
            for entry in ranking_group.get("ranks", []):
                rank = entry.get("current")
                name = entry.get("athlete", {}).get("displayName", "")
                if rank and name:
                    out[name] = int(rank)
        return out

    def _get_todays_tennis_matches(self, league: str) -> list[dict]:
        """
        Parses ESPN tennis scoreboard groupings to extract today's matches.
        Returns same format as _parse_event.
        """
        rankings = self._fetch_tennis_rankings(league)
        url      = f"{ESPN_BASE}/tennis/{league}/scoreboard"
        today    = datetime.date.today().isoformat()
        try:
            r = requests.get(url, params={"dates": today.replace("-", "")},
                             timeout=10)
            r.raise_for_status()
            events = r.json().get("events", [])
        except Exception as e:
            log.warning(f"Tennis scoreboard ({league}) failed: {e}")
            return []

        games = []
        for event in events:
            for group in event.get("groupings", []):
                for comp in group.get("competitions", []):
                    if comp.get("date", "")[:10] != today:
                        continue
                    competitors = comp.get("competitors", [])
                    if len(competitors) < 2:
                        continue
                    p1 = competitors[0].get("athlete", {}).get("displayName", "")
                    p2 = competitors[1].get("athlete", {}).get("displayName", "")
                    if not p1 or not p2:
                        continue
                    r1 = rankings.get(p1)
                    r2 = rankings.get(p2)
                    if r1 is None and r2 is None:
                        continue  # no ranking data
                    # Default unranked to 200
                    r1 = r1 if r1 else 200
                    r2 = r2 if r2 else 200
                    # Log-rank probability: higher rank number = worse player
                    import math
                    l1, l2 = math.log(r1 + 1), math.log(r2 + 1)
                    # p1 wins = l2/(l1+l2) since lower rank is better
                    p_p1 = l2 / (l1 + l2)
                    p_p1 = min(0.95, max(0.05, p_p1))
                    games.append(dict(
                        home=p1, away=p2,
                        prob_home=p_p1, prob_away=1.0 - p_p1,
                        sport="tennis", league=league,
                        source=f"ranking(#{r1} vs #{r2})",
                        start_time=comp.get("date", ""),
                    ))
        return games

    def get_todays_games(self) -> list[dict]:
        date_str = datetime.date.today().strftime("%Y%m%d")
        games    = []
        for series, (sport, league) in SPORTS_SERIES.items():
            if league in ("wta", "atp"):
                games.extend(self._get_todays_tennis_matches(league))
            else:
                events = self._fetch_scoreboard(sport, league, date_str)
                for ev in events:
                    rec = self._parse_event(ev, sport, league)
                    if rec:
                        games.append(rec)
        return games


# ─── Ticker Date Parser ──────────────────────────────────────────────────────

_MONTH_MAP = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
}

def _parse_ticker_date(series: str, ticker: str) -> Optional[datetime.date]:
    """
    Extracts the game date from a Kalshi ticker.
    Pattern after series prefix: YY{MON}DD  e.g. 26MAR26 = March 26 2026.
    """
    prefix = series + "-"
    if not ticker.startswith(prefix):
        return None
    rest = ticker[len(prefix):]
    m = re.match(r"^(\d{2})([A-Z]{3})(\d{2})", rest)
    if not m:
        return None
    yy, mon, dd = m.group(1), m.group(2), m.group(3)
    month = _MONTH_MAP.get(mon)
    if not month:
        return None
    try:
        return datetime.date(2000 + int(yy), month, int(dd))
    except ValueError:
        return None


# ─── Team-Name Matching ─────────────────────────────────────────────────────

def _words(name: str) -> list[str]:
    """Lower-case words longer than 3 chars (filters 'san', 'los', 'new', etc.)."""
    return [w for w in re.split(r"\W+", name.lower()) if len(w) > 3]

def _overlap(title: str, team: str) -> int:
    tw = set(_words(title))
    return sum(1 for w in _words(team) if w in tw)

def match_market_to_game(market: dict, games: list[dict]) -> Optional[dict]:
    """
    Match a Kalshi market to an ESPN game entry.
    Returns {game, prob_yes, match_info} or None.

    Strategy:
      - Restrict candidate games to the same sport/league as the Kalshi series.
      - Use rules_primary + title + yes_sub_title to identify yes-side team.
      - Find game whose home/away name shares the most tokens.
    """
    rules     = market.get("rules_primary", "")
    title     = market.get("title", "")
    yes_sub   = market.get("yes_sub_title", "")   # e.g. "Charlotte"
    full_text = f"{rules} {title} {yes_sub}"

    # Narrow to the correct sport/league so "Utah" NBA ≠ "Utah" NHL
    series    = market.get("_series", "")
    league_filter = SPORTS_SERIES.get(series, (None, None))[1]  # e.g. "nba"

    best_game       = None
    best_prob_yes   = None
    best_score      = 0
    best_info       = ""

    for game in games:
        if league_filter and game.get("league") != league_filter:
            continue
        h, a = game["home"], game["away"]

        h_score = _overlap(full_text, h)
        a_score = _overlap(full_text, a)

        # Require BOTH teams to appear in the market text.
        # Prevents "Los Angeles Angels" matching an LA Dodgers market just
        # because "Los Angeles" appears while "Houston" does not.
        if h_score == 0 or a_score == 0:
            continue

        # Which team is the "yes" side?
        # yes_sub_title is the clearest signal (e.g. "Charlotte" or "Sabalenka")
        yes_h = _overlap(yes_sub or title, h)
        yes_a = _overlap(yes_sub or title, a)

        if yes_h >= yes_a and yes_h > 0:
            prob_yes = game["prob_home"]
            yes_team = h
        elif yes_a > yes_h:
            prob_yes = game["prob_away"]
            yes_team = a
        else:
            # Tie – skip ambiguous
            continue

        score = h_score + a_score + max(yes_h, yes_a)
        if score > best_score:
            best_score    = score
            best_game     = game
            best_prob_yes = prob_yes
            best_info     = f"yes={yes_team}"

    if best_game and best_score >= 2:
        return dict(game=best_game, prob_yes=best_prob_yes, info=best_info)
    return None


# ─── Trade Logger ────────────────────────────────────────────────────────────

def load_trade_log() -> dict:
    """
    Returns today's log entry as {"date": today, "trades": [...], "count": N}.
    Past days' entries are preserved in the file under their own date keys.
    """
    today = str(datetime.date.today())
    all_logs: dict = {}
    if os.path.exists(TRADE_LOG_FILE):
        with open(TRADE_LOG_FILE) as f:
            all_logs = json.load(f)
        # Migrate old single-day format ({"date":…,"trades":…,"count":…}) to multi-day
        if "date" in all_logs and "trades" in all_logs and isinstance(all_logs["trades"], list):
            old_date  = all_logs["date"]
            old_entry = {"trades": all_logs["trades"], "count": all_logs.get("count", len(all_logs["trades"]))}
            all_logs  = {old_date: old_entry}
            with open(TRADE_LOG_FILE, "w") as f:
                json.dump(all_logs, f, indent=2)
    if today in all_logs:
        entry = all_logs[today]
        return {"date": today, "trades": entry["trades"], "count": entry["count"]}
    return {"date": today, "trades": [], "count": 0}


def save_trade_log(log_data: dict) -> None:
    """Merge today's entry back into the full multi-day history and write to disk."""
    today = log_data["date"]
    all_logs: dict = {}
    if os.path.exists(TRADE_LOG_FILE):
        with open(TRADE_LOG_FILE) as f:
            all_logs = json.load(f)
        # Handle file still in old single-day format
        if "date" in all_logs and "trades" in all_logs and isinstance(all_logs["trades"], list):
            old_date  = all_logs["date"]
            old_entry = {"trades": all_logs["trades"], "count": all_logs.get("count", len(all_logs["trades"]))}
            all_logs  = {old_date: old_entry}
    all_logs[today] = {"trades": log_data["trades"], "count": log_data["count"]}
    with open(TRADE_LOG_FILE, "w") as f:
        json.dump(all_logs, f, indent=2)


# ─── Opportunity Finder ──────────────────────────────────────────────────────

def find_opportunities(markets: list[dict], games: list[dict],
                       polymarket: Optional["PolymarketSource"] = None) -> list[dict]:
    """
    For each market, compute edge. Return trades sorted by |edge| descending.
    Deduplicates so at most one trade per event_ticker.

    If a PolymarketSource is provided, the ESPN probability is blended with
    Polymarket's implied price:
      - ESPN sportsbook odds available → 50% ESPN + 50% Polymarket
      - ESPN win-rate only             → 25% ESPN + 75% Polymarket
    """
    seen_events: set[str] = set()
    opps: list[dict]      = []

    for market in markets:
        event_ticker = market.get("event_ticker", market["ticker"])

        # Parse prices (dollar strings → float)
        try:
            yes_ask_f = float(market["yes_ask_dollars"])
            yes_bid_f = float(market["yes_bid_dollars"])
        except (KeyError, ValueError):
            continue

        if yes_ask_f <= 0 or yes_bid_f <= 0:
            continue

        # Skip if we already have a trade for this game
        if event_ticker in seen_events:
            continue

        match = match_market_to_game(market, games)
        if not match:
            continue

        start_time_str = match["game"].get("start_time", "")
        if not start_time_str:
            continue
        try:
            now      = datetime.datetime.now(datetime.timezone.utc)
            start_dt = datetime.datetime.fromisoformat(
                           start_time_str.replace("Z", "+00:00"))
            hours_until = (start_dt - now).total_seconds() / 3600
        except ValueError:
            continue
        if hours_until < 0 or hours_until > TRADE_HORIZON_HOURS:
            continue

        espn_prob    = match["prob_yes"]
        espn_source  = match["game"]["source"]
        model_prob   = espn_prob
        model_source = f"espn:{espn_source}"

        # Require a Polymarket match — it is the primary signal
        if polymarket is None:
            continue
        yes_team_name = match["info"].replace("yes=", "")
        g = match["game"]
        h_overlap = _overlap(yes_team_name, g["home"])
        a_overlap = _overlap(yes_team_name, g["away"])
        other_team = g["away"] if h_overlap >= a_overlap else g["home"]

        pm_result = polymarket.get_prob(yes_team_name, other_team,
                                        league=g.get("league", ""))
        if pm_result is None:
            continue
        pm_prob, pm_q = pm_result
        if espn_source == "espn_odds":
            model_prob   = 0.5 * espn_prob + 0.5 * pm_prob
            model_source = "espn_odds(50%)+polymarket(50%)"
        else:
            model_prob   = pm_prob
            model_source = "polymarket"
        log.info(
            f"Polymarket [{yes_team_name}]: "
            f"ESPN={espn_prob:.3f} PM={pm_prob:.3f} "
            f"blended={model_prob:.3f}  '{pm_q[:60]}'"
        )

        kalshi_mid = (yes_ask_f + yes_bid_f) / 2.0
        edge_pp    = (model_prob - kalshi_mid) * 100.0

        if abs(edge_pp) < MIN_EDGE_PP:
            continue

        # Fade Kalshi: buy YES when Polymarket > Kalshi mid, NO otherwise.
        if edge_pp > 0:
            side        = "yes"
            price_f     = yes_ask_f
            price_cents = round(price_f * 100)
        else:
            side        = "no"
            price_f     = 1.0 - yes_bid_f
            price_cents = round(price_f * 100)

        if price_cents < 1 or price_cents > 99:
            continue

        budget    = max(MIN_BUDGET, min(BASE_BUDGET, BASE_BUDGET * abs(edge_pp) / BASE_EDGE_PP))
        contracts = int(budget / price_f)
        if contracts < 1:
            continue

        seen_events.add(event_ticker)
        opps.append(dict(
            market       = market,
            match        = match,
            side         = side,
            price_cents  = price_cents,
            price_f      = price_f,
            kalshi_mid   = kalshi_mid,
            model_prob   = model_prob,
            espn_prob    = espn_prob,
            model_source = model_source,
            edge_pp      = edge_pp,
            contracts    = contracts,
            cost_usd     = contracts * price_f,
        ))

    opps.sort(key=lambda x: abs(x["edge_pp"]), reverse=True)
    return opps


# ─── Execution Report ────────────────────────────────────────────────────────

def print_trade_report(opp: dict, order_result: Optional[dict],
                       idx: int, total: int, dry_run: bool) -> None:
    market  = opp["market"]
    match   = opp["match"]
    game    = match["game"]
    ticker  = market["ticker"]
    title   = market.get("title", ticker)

    ya  = float(market["yes_ask_dollars"]) * 100
    yb  = float(market["yes_bid_dollars"]) * 100
    mid = opp["kalshi_mid"] * 100
    mp  = opp["model_prob"] * 100
    ep  = opp["edge_pp"]

    print(f"\n{'─'*68}")
    print(f"  Trade {idx}/{total}{'  [DRY RUN]' if dry_run else ''}")
    print(f"{'─'*68}")
    print(f"  Market  : {title}")
    print(f"  Ticker  : {ticker}")
    print(f"  Game    : {game['away']} @ {game['home']}  "
          f"({game['sport'].upper()} / {game['league'].upper()})")
    print(f"  Source  : {opp.get('model_source', game['source'])}")
    print()
    print(f"  Kalshi yes-bid / yes-ask : {yb:.0f}¢ / {ya:.0f}¢  "
          f"(mid = {mid:.1f}¢)")
    if "espn_prob" in opp and abs(opp["espn_prob"] - opp["model_prob"]) > 0.001:
        print(f"  ESPN probability (yes)   : {opp['espn_prob']*100:.1f}%")
    print(f"  Model probability (yes)  : {mp:.1f}%")
    print(f"  Edge                     : {ep:+.1f} pp  →  BUY {opp['side'].upper()}")
    print()
    print(f"  Price per contract : {opp['price_cents']}¢  (${opp['price_f']:.2f})")
    print(f"  Contracts          : {opp['contracts']} × {opp['price_cents']}¢"
          f" = ${opp['cost_usd']:.2f}")

    if order_result is not None:
        order = order_result.get("order", {})
        status = order.get("status", "unknown")
        filled = order.get("taker_fill_count", 0)
        oid    = order.get("order_id", "N/A")
        print()
        print(f"  Order status : {status}   filled = {filled} contracts")
        print(f"  Order ID     : {oid}")


# ─── Main Bot ────────────────────────────────────────────────────────────────

def run_bot(dry_run: bool = False) -> None:
    trade_log = load_trade_log()
    trades_done = trade_log["count"]

    # Auth client
    if not KALSHI_KEY_ID or not KALSHI_KEY_FILE:
        print("Error: set KALSHI_KEY_ID and KALSHI_KEY_FILE environment variables.")
        sys.exit(1)
    client = KalshiClient(KALSHI_KEY_ID, KALSHI_KEY_FILE)

    # Balance check
    try:
        balance = client.get_balance_usd()
        log.info(f"Account balance: ${balance:.2f}")
    except Exception as e:
        log.error(f"Could not fetch balance: {e}")
        return

    # Fetch today's Kalshi sports game markets
    log.info("Fetching today's Kalshi sports game markets…")
    markets = client.get_todays_game_markets()
    log.info(f"Found {len(markets)} game markets closing today")

    if not markets:
        print("No Kalshi sports markets found for today's games.")
        return

    # Fetch ESPN game data (independent probability model)
    log.info("Building probability model from ESPN data…")
    model  = ProbabilityModel()
    games  = model.get_todays_games()
    log.info(f"ESPN returned {len(games)} games across all sports")

    if not games:
        print("ESPN returned no game data for today. Cannot build model.")
        return

    # Fetch Polymarket prices for ensemble blending
    log.info("Fetching Polymarket prices per game…")
    polymarket = PolymarketSource()

    # Find trading opportunities
    opps = find_opportunities(markets, games, polymarket=polymarket)

    selected = opps[:MAX_TRADES_PER_RUN]

    # ── Header ──────────────────────────────────────────────────────────────
    print()
    print("=" * 68)
    print("  KALSHI SPORTS TRADING BOT")
    print("=" * 68)
    print(f"  Date             : {datetime.date.today()}")
    print(f"  Account balance  : ${balance:.2f}")
    print(f"  Trades today     : {trades_done} placed so far")
    print(f"  Kalshi markets   : {len(markets)}")
    print(f"  ESPN games       : {len(games)}")
    print(f"  Edges >{MIN_EDGE_PP:.0f}pp found : {len(opps)}")
    print(f"  Trades to make   : {len(selected)}")

    if not selected:
        print("\n  No opportunities with sufficient edge found today.")
        print("=" * 68)
        return

    # ── Execute ──────────────────────────────────────────────────────────────
    executed = 0
    for i, opp in enumerate(selected, 1):
        order_result = None
        if not dry_run:
            try:
                order_result = client.place_order(
                    ticker      = opp["market"]["ticker"],
                    side        = opp["side"],
                    price_cents = opp["price_cents"],
                    count       = opp["contracts"],
                )
                trade_log["trades"].append({
                    "timestamp"    : datetime.datetime.utcnow().isoformat() + "Z",
                    "ticker"       : opp["market"]["ticker"],
                    "title"        : opp["market"].get("title", ""),
                    "side"         : opp["side"],
                    "price_cents"  : opp["price_cents"],
                    "contracts"    : opp["contracts"],
                    "cost_usd"     : round(opp["cost_usd"], 2),
                    "model_prob"   : round(opp["model_prob"], 4),
                    "espn_prob"    : round(opp.get("espn_prob", opp["model_prob"]), 4),
                    "model_source" : opp.get("model_source", ""),
                    "kalshi_mid"   : round(opp["kalshi_mid"], 4),
                    "edge_pp"      : round(opp["edge_pp"],    2),
                    "order_id"     : order_result.get("order", {}).get("order_id"),
                    "status"       : order_result.get("order", {}).get("status"),
                })
                trade_log["count"] += 1
                executed += 1
            except Exception as e:
                log.error(f"Order failed for {opp['market']['ticker']}: {e}")
                order_result = None

        print_trade_report(opp, order_result, i, len(selected), dry_run)

    # ── Footer ───────────────────────────────────────────────────────────────
    print()
    print("=" * 68)
    if dry_run:
        print(f"  DRY RUN — no orders placed.")
    else:
        print(f"  Trades executed : {executed}/{len(selected)}")
        print(f"  Daily total     : {trade_log['count']}")
        save_trade_log(trade_log)
        print(f"  Log saved to    : {TRADE_LOG_FILE}")
    print("=" * 68)


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    run_bot(dry_run=dry)
