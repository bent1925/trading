#!/usr/bin/env python3
"""
Kalshi Sports Trading Bot
=========================
- Finds sports game markets (NBA, MLB, NHL, WTA, ATP) closing today
- Builds an independent win-probability model from ESPN's public API
  (consensus sportsbook money-lines when available; season-record ratio otherwise)
- Buys "yes" when model_prob > kalshi_mid + 10pp
- Buys "no"  when model_prob < kalshi_mid - 10pp
- Max 4 trades/day, $10 per trade (as many contracts as $10 allows)
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

MAX_TRADES_PER_DAY = 4
BUDGET_USD         = 10.00     # dollars allocated per trade
MIN_EDGE_PP        = 10.0      # minimum edge in percentage points to trade

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
        Returns win percentage, or None if no games have been played.
        ESPN encodes records as a summary string "W-L" (e.g. "38-34").
        """
        for rec in competitor.get("records", []):
            if rec.get("type") == "total":
                summary = rec.get("summary", "")
                m = re.match(r"^(\d+)-(\d+)", summary)
                if m:
                    w, l = int(m.group(1)), int(m.group(2))
                    if w + l >= 5:          # require at least 5 games; early-season records are noise
                        return w / (w + l)
        return None  # no data

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
                                source="espn_odds")

        # 2. Fallback: season win-rate ratio + home advantage
        h_pct = self._record_win_pct(home)
        a_pct = self._record_win_pct(away)
        # Require at least one team to have actual record data
        if h_pct is None and a_pct is None:
            return None   # no basis for a model estimate
        h_pct = h_pct if h_pct is not None else 0.5
        a_pct = a_pct if a_pct is not None else 0.5
        total = h_pct + a_pct
        p_home = (h_pct / total) if total > 0 else 0.5
        HOME_EDGE = 0.04 if league not in ("wta", "atp") else 0.0
        p_home = min(0.95, max(0.05, p_home + HOME_EDGE))
        return dict(home=home_name, away=away_name,
                    prob_home=p_home, prob_away=1.0 - p_home,
                    sport=sport, league=league,
                    source="win_pct")

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
    """Lower-case words longer than 2 chars."""
    return [w for w in re.split(r"\W+", name.lower()) if len(w) > 2]

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
    today = str(datetime.date.today())
    if os.path.exists(TRADE_LOG_FILE):
        with open(TRADE_LOG_FILE) as f:
            data = json.load(f)
        if data.get("date") == today:
            return data
    return {"date": today, "trades": [], "count": 0}

def save_trade_log(log_data: dict) -> None:
    with open(TRADE_LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=2)


# ─── Opportunity Finder ──────────────────────────────────────────────────────

def find_opportunities(markets: list[dict], games: list[dict]) -> list[dict]:
    """
    For each market, compute edge. Return trades sorted by |edge| descending.
    Deduplicates so at most one trade per event_ticker.
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

        kalshi_mid = (yes_ask_f + yes_bid_f) / 2.0   # 0–1 range
        model_prob = match["prob_yes"]                 # 0–1 range
        edge_pp    = (model_prob - kalshi_mid) * 100.0 # percentage points

        if abs(edge_pp) < MIN_EDGE_PP:
            continue

        # Decide side and price
        if edge_pp > 0:
            # Model says yes is cheap → buy yes at yes_ask
            side        = "yes"
            price_f     = yes_ask_f          # 0–1
            price_cents = round(price_f * 100)
        else:
            # Model says yes is expensive → buy no at no_ask ≈ 1 – yes_bid
            side        = "no"
            price_f     = 1.0 - yes_bid_f   # 0–1
            price_cents = round(price_f * 100)

        if price_cents < 1 or price_cents > 99:
            continue

        contracts = int(BUDGET_USD / price_f)
        if contracts < 1:
            continue

        seen_events.add(event_ticker)
        opps.append(dict(
            market      = market,
            match       = match,
            side        = side,
            price_cents = price_cents,
            price_f     = price_f,
            kalshi_mid  = kalshi_mid,
            model_prob  = model_prob,
            edge_pp     = edge_pp,
            contracts   = contracts,
            cost_usd    = contracts * price_f,
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
    print(f"  Source  : model built from {game['source']}")
    print()
    print(f"  Kalshi yes-bid / yes-ask : {yb:.0f}¢ / {ya:.0f}¢  "
          f"(mid = {mid:.1f}¢)")
    print(f"  Model probability (yes)  : {mp:.1f}%")
    print(f"  Edge                     : {ep:+.1f} pp  →  BUY {opp['side'].upper()}")
    print()
    print(f"  Price per contract : {opp['price_cents']}¢  (${opp['price_f']:.2f})")
    print(f"  Budget             : ${BUDGET_USD:.2f}")
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

    if trades_done >= MAX_TRADES_PER_DAY:
        print(f"Already executed {MAX_TRADES_PER_DAY} trades today. Nothing to do.")
        return

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

    # Find trading opportunities
    opps = find_opportunities(markets, games)

    trades_remaining = MAX_TRADES_PER_DAY - trades_done
    selected         = opps[:trades_remaining]

    # ── Header ──────────────────────────────────────────────────────────────
    print()
    print("=" * 68)
    print("  KALSHI SPORTS TRADING BOT")
    print("=" * 68)
    print(f"  Date             : {datetime.date.today()}")
    print(f"  Account balance  : ${balance:.2f}")
    print(f"  Trades today     : {trades_done}/{MAX_TRADES_PER_DAY}")
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
                    "timestamp"   : datetime.datetime.utcnow().isoformat() + "Z",
                    "ticker"      : opp["market"]["ticker"],
                    "title"       : opp["market"].get("title", ""),
                    "side"        : opp["side"],
                    "price_cents" : opp["price_cents"],
                    "contracts"   : opp["contracts"],
                    "cost_usd"    : round(opp["cost_usd"], 2),
                    "model_prob"  : round(opp["model_prob"], 4),
                    "kalshi_mid"  : round(opp["kalshi_mid"], 4),
                    "edge_pp"     : round(opp["edge_pp"],    2),
                    "order_id"    : order_result.get("order", {}).get("order_id"),
                    "status"      : order_result.get("order", {}).get("status"),
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
        print(f"  Daily total     : {trade_log['count']}/{MAX_TRADES_PER_DAY}")
        save_trade_log(trade_log)
        print(f"  Log saved to    : {TRADE_LOG_FILE}")
    print("=" * 68)


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    run_bot(dry_run=dry)
