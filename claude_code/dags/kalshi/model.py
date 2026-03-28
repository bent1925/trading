import datetime
import logging
import math
import re
from typing import Optional

import requests

from .config import ESPN_BASE, SPORTS_SERIES, BUDGET_USD, MIN_EDGE_PP
from .polymarket import PolymarketSource
from .utils import words, overlap

log = logging.getLogger(__name__)


# ── ESPN Probability Model ────────────────────────────────────────────────────

class ProbabilityModel:
    """
    Builds win-probability estimates from ESPN's public API.

    Priority per game:
      1. Consensus sportsbook money-line odds embedded in ESPN response
      2. Season win-rate blended with last-10-game form + home advantage
      3. Log-rank model (tennis only)
    """

    def _fetch_scoreboard(self, sport: str, league: str,
                          date_str: str) -> list:
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
        if ml > 0:
            return 100.0 / (ml + 100.0)
        return abs(ml) / (abs(ml) + 100.0)

    @staticmethod
    def _season_win_pct(competitor: dict) -> Optional[float]:
        """Season record W-L, min 5 games."""
        for rec in competitor.get("records", []):
            if rec.get("type") == "total":
                m = re.match(r"^(\d+)-(\d+)", rec.get("summary", ""))
                if m:
                    w, l = int(m.group(1)), int(m.group(2))
                    if w + l >= 5:
                        return w / (w + l)
        return None

    @staticmethod
    def _recent_form_pct(competitor: dict) -> Optional[float]:
        """Last-10-game win rate."""
        for rec in competitor.get("records", []):
            if rec.get("type") in ("lastTen", "last10"):
                m = re.match(r"^(\d+)-(\d+)", rec.get("summary", ""))
                if m:
                    w, l = int(m.group(1)), int(m.group(2))
                    if w + l > 0:
                        return w / (w + l)
        return None

    def _parse_event(self, event: dict, sport: str,
                     league: str) -> Optional[dict]:
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

        # 1. Sportsbook money-lines
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

        # 2. Season win-rate + recent form
        h_season = self._season_win_pct(home)
        a_season = self._season_win_pct(away)
        if h_season is None and a_season is None:
            return None

        h_form = self._recent_form_pct(home)
        a_form = self._recent_form_pct(away)

        def _blend(season, form):
            if season is None and form is None:
                return 0.5
            if season is None:
                return form
            if form is None:
                return season
            return 0.6 * season + 0.4 * form

        h_pct  = _blend(h_season, h_form)
        a_pct  = _blend(a_season, a_form)
        total  = h_pct + a_pct
        p_home = (h_pct / total) if total > 0 else 0.5
        HOME_EDGE = 0.04 if league not in ("wta", "atp") else 0.0
        p_home = min(0.95, max(0.05, p_home + HOME_EDGE))
        source = "win_pct+form" if (h_form is not None or a_form is not None) \
                 else "win_pct"
        return dict(home=home_name, away=away_name,
                    prob_home=p_home, prob_away=1.0 - p_home,
                    sport=sport, league=league, source=source)

    def _fetch_tennis_rankings(self, league: str) -> dict:
        url = f"{ESPN_BASE}/tennis/{league}/rankings"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        except Exception as e:
            log.warning(f"Tennis rankings ({league}) failed: {e}")
            return {}
        out = {}
        for group in r.json().get("rankings", []):
            for entry in group.get("ranks", []):
                rank = entry.get("current")
                name = entry.get("athlete", {}).get("displayName", "")
                if rank and name:
                    out[name] = int(rank)
        return out

    def _get_todays_tennis_matches(self, league: str) -> list:
        rankings = self._fetch_tennis_rankings(league)
        today    = datetime.date.today().isoformat()
        url      = f"{ESPN_BASE}/tennis/{league}/scoreboard"
        try:
            r = requests.get(url,
                             params={"dates": today.replace("-", "")},
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
                    r1 = rankings.get(p1) or 200
                    r2 = rankings.get(p2) or 200
                    l1, l2 = math.log(r1 + 1), math.log(r2 + 1)
                    p_p1 = min(0.95, max(0.05, l2 / (l1 + l2)))
                    games.append(dict(
                        home=p1, away=p2,
                        prob_home=p_p1, prob_away=1.0 - p_p1,
                        sport="tennis", league=league,
                        source=f"ranking(#{r1} vs #{r2})",
                    ))
        return games

    def get_todays_games(self) -> list:
        date_str = datetime.date.today().strftime("%Y%m%d")
        games    = []
        for series, (sport, league) in SPORTS_SERIES.items():
            if league in ("wta", "atp"):
                games.extend(self._get_todays_tennis_matches(league))
            else:
                for ev in self._fetch_scoreboard(sport, league, date_str):
                    rec = self._parse_event(ev, sport, league)
                    if rec:
                        games.append(rec)
        return games


# ── Market ↔ Game Matching ────────────────────────────────────────────────────

def match_market_to_game(market: dict, games: list) -> Optional[dict]:
    """
    Returns {game, prob_yes, info} matching the Kalshi market, or None.
    Restricts candidates to the correct sport/league, then selects by
    token-overlap of market text against team display names.
    """
    rules     = market.get("rules_primary", "")
    title     = market.get("title", "")
    yes_sub   = market.get("yes_sub_title", "")
    full_text = f"{rules} {title} {yes_sub}"
    series    = market.get("_series", "")
    league_filter = SPORTS_SERIES.get(series, (None, None))[1]

    best_game, best_prob_yes, best_score, best_info = None, None, 0, ""

    for game in games:
        if league_filter and game.get("league") != league_filter:
            continue
        h, a    = game["home"], game["away"]
        h_score = overlap(full_text, h)
        a_score = overlap(full_text, a)
        if h_score == 0 or a_score == 0:
            continue

        yes_h = overlap(yes_sub or title, h)
        yes_a = overlap(yes_sub or title, a)

        if yes_h >= yes_a and yes_h > 0:
            prob_yes, yes_team = game["prob_home"], h
        elif yes_a > yes_h:
            prob_yes, yes_team = game["prob_away"], a
        else:
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


# ── Opportunity Finder ────────────────────────────────────────────────────────

def find_opportunities(markets: list, games: list,
                       polymarket: Optional[PolymarketSource] = None) -> list:
    """
    Returns all tradeable opportunities sorted by |edge| descending.
    Each opportunity is a flat, JSON-serializable dict.

    Blending weights when Polymarket price is available:
      ESPN sportsbook odds  → 50% ESPN + 50% Polymarket
      ESPN win-rate/form    → 25% ESPN + 75% Polymarket
    """
    seen_events: set = set()
    opps: list       = []

    for market in markets:
        event_ticker = market.get("event_ticker", market["ticker"])
        try:
            yes_ask_f = float(market["yes_ask_dollars"])
            yes_bid_f = float(market["yes_bid_dollars"])
        except (KeyError, ValueError):
            continue
        if yes_ask_f <= 0 or yes_bid_f <= 0:
            continue
        if event_ticker in seen_events:
            continue

        match = match_market_to_game(market, games)
        if not match:
            continue

        espn_prob    = match["prob_yes"]
        espn_source  = match["game"]["source"]
        model_prob   = espn_prob
        model_source = f"espn:{espn_source}"

        if polymarket is not None:
            yes_team  = match["info"].replace("yes=", "")
            g         = match["game"]
            h_ov      = overlap(yes_team, g["home"])
            a_ov      = overlap(yes_team, g["away"])
            other     = g["away"] if h_ov >= a_ov else g["home"]
            pm_result = polymarket.get_prob(yes_team, other,
                                            league=g.get("league", ""))
            if pm_result is not None:
                pm_prob, pm_q = pm_result
                if espn_source == "espn_odds":
                    model_prob   = 0.5 * espn_prob + 0.5 * pm_prob
                    model_source = "espn_odds(50%)+polymarket(50%)"
                else:
                    model_prob   = 0.25 * espn_prob + 0.75 * pm_prob
                    model_source = f"polymarket(75%)+{espn_source}(25%)"
                log.info(
                    f"Polymarket [{yes_team}]: ESPN={espn_prob:.3f} "
                    f"PM={pm_prob:.3f} blended={model_prob:.3f} "
                    f"'{pm_q[:55]}'"
                )

        kalshi_mid = (yes_ask_f + yes_bid_f) / 2.0
        edge_pp    = (model_prob - kalshi_mid) * 100.0

        if abs(edge_pp) < MIN_EDGE_PP:
            continue

        if edge_pp > 0:
            side, price_f = "yes", yes_ask_f
        else:
            side, price_f = "no",  1.0 - yes_bid_f
        price_cents = round(price_f * 100)

        if price_cents < 1 or price_cents > 99:
            continue

        contracts = int(BUDGET_USD / price_f)
        if contracts < 1:
            continue

        seen_events.add(event_ticker)
        g = match["game"]
        opps.append({
            # Trade execution fields
            "ticker":       market["ticker"],
            "title":        market.get("title", ""),
            "side":         side,
            "price_cents":  price_cents,
            "price_f":      price_f,
            "contracts":    contracts,
            "cost_usd":     round(contracts * price_f, 2),
            # Model fields
            "model_prob":   round(model_prob,  4),
            "espn_prob":    round(espn_prob,   4),
            "model_source": model_source,
            "kalshi_mid":   round(kalshi_mid,  4),
            "edge_pp":      round(edge_pp,     2),
            # Game context
            "game_home":    g["home"],
            "game_away":    g["away"],
            "sport":        g["sport"],
            "league":       g["league"],
            "match_info":   match["info"],
            # Raw prices for reporting
            "yes_ask_cents": round(yes_ask_f * 100),
            "yes_bid_cents": round(yes_bid_f * 100),
        })

    opps.sort(key=lambda x: abs(x["edge_pp"]), reverse=True)
    return opps
