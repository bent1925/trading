import datetime
import logging
import math
import re
from typing import Optional

import requests

from .config import (ESPN_BASE, SPORTS_SERIES, MIN_EDGE_PP,
                     KELLY_FRACTION, MAX_BET, TRADE_HORIZON_HOURS,
                     SOS_MULTIPLIER, OPPONENT_STRENGTH_FILE,
                     INJURY_ADJUSTMENT_PP, INJURY_ADJUSTMENT_MAX_PP)
from .polymarket import PolymarketSource
from .opponent_strength import OpponentStrengthDB
from .injury_data import ESPNInjurySource
from .utils import words, overlap

log = logging.getLogger(__name__)


# ── ESPN Probability Model ────────────────────────────────────────────────────

class ProbabilityModel:
    """
    Builds win-probability estimates from ESPN's public API.

    Priority per game:
      1. Consensus sportsbook money-line odds embedded in ESPN response
      2. Season win-rate blended with last-10-game form + home advantage
         (optionally adjusted by strength-of-schedule)
      3. Log-rank model (tennis only)
    """

    def __init__(self, opp_strength_db: Optional[OpponentStrengthDB] = None,
                 injury_source: Optional[ESPNInjurySource] = None):
        self.opp_strength_db = opp_strength_db or OpponentStrengthDB(OPPONENT_STRENGTH_FILE)
        self.injury_source   = injury_source

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

    def _apply_sos_adjustment(self, home_pct: float, away_pct: float,
                               home_name: str, away_name: str) -> tuple:
        """
        Adjust win-rate probabilities based on opponent strength.

        If opponent is weak (low win %), boost our prob.
        If opponent is strong (high win %), dampen our prob.

        Returns: (adjusted_home_pct, adjusted_away_pct)
        """
        if SOS_MULTIPLIER <= 0:
            return (home_pct, away_pct)

        # Get opponent strength (win rate when facing them)
        away_strength = self.opp_strength_db.get_opponent_strength(home_name, away_name)
        home_strength = self.opp_strength_db.get_opponent_strength(away_name, home_name)

        # Adjustment = (0.5 - opponent_strength) * multiplier
        # Example: if away team is weak (0.4), adjustment = (0.5 - 0.4) * 0.2 = +0.02
        home_adjustment = (0.5 - away_strength) * SOS_MULTIPLIER
        away_adjustment = (0.5 - home_strength) * SOS_MULTIPLIER

        # Apply multiplicative adjustment to maintain probabilities in [0, 1]
        h_pct_adjusted = home_pct * (1.0 + home_adjustment)
        a_pct_adjusted = away_pct * (1.0 + away_adjustment)

        # Clamp to [0.05, 0.95]
        h_pct_adjusted = min(0.95, max(0.05, h_pct_adjusted))
        a_pct_adjusted = min(0.95, max(0.05, a_pct_adjusted))

        # Normalize to sum to 1
        total = h_pct_adjusted + a_pct_adjusted
        if total > 0:
            h_pct_adjusted /= total
            a_pct_adjusted /= total
        else:
            h_pct_adjusted = 0.5
            a_pct_adjusted = 0.5

        log.debug(
            f"SOS adjustment: {home_name} vs {away_name} — "
            f"home {home_pct:.3f} → {h_pct_adjusted:.3f} "
            f"(away_strength={away_strength:.3f}, adj={home_adjustment:.3f})"
        )

        return (h_pct_adjusted, a_pct_adjusted)

    def _injury_adjustment(self, team: str, league: str) -> float:
        """
        Returns a negative probability adjustment (0.0 to -INJURY_ADJUSTMENT_MAX_PP/100)
        based on Out/Questionable players for the team.

        Only called for the win-rate fallback — sportsbook odds and Polymarket
        already reflect injury information.
        """
        if self.injury_source is None:
            return 0.0
        unavailable = self.injury_source.get_unavailable(team, league)
        out_pp = sum(
            INJURY_ADJUSTMENT_PP if any(s in status for s in ("out", "injured reserve",
                                                                "physically unable", "suspended"))
            else INJURY_ADJUSTMENT_PP * 0.33
            for status in unavailable.values()
        )
        capped = min(out_pp, INJURY_ADJUSTMENT_MAX_PP)
        if capped > 0:
            log.debug(
                f"Injury adjustment {team} ({league}): "
                f"{len(unavailable)} player(s) → -{capped:.1f}pp"
            )
        return -capped / 100.0

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
                                source="espn_odds",
                                start_time=comp.get("date", ""))

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

        # Apply strength-of-schedule adjustment (win-rate fallback only)
        if SOS_MULTIPLIER > 0:
            p_home, p_away = self._apply_sos_adjustment(p_home, 1.0 - p_home,
                                                         home_name, away_name)
        else:
            p_away = 1.0 - p_home

        # Apply injury adjustment (win-rate fallback only)
        if self.injury_source is not None:
            h_inj = self._injury_adjustment(home_name, league)
            a_inj = self._injury_adjustment(away_name, league)
            p_home = min(0.95, max(0.05, p_home + h_inj))
            p_away = min(0.95, max(0.05, p_away + a_inj))
            total  = p_home + p_away
            if total > 0:
                p_home /= total
                p_away  = 1.0 - p_home

        source = "win_pct+form" if (h_form is not None or a_form is not None) \
                 else "win_pct"
        return dict(home=home_name, away=away_name,
                    prob_home=p_home, prob_away=p_away,
                    sport=sport, league=league, source=source,
                    start_time=comp.get("date", ""))

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

    def _get_tennis_matches(self, league: str,
                            fetch_date: datetime.date) -> list:
        rankings  = self._fetch_tennis_rankings(league)
        date_iso  = fetch_date.isoformat()
        url       = f"{ESPN_BASE}/tennis/{league}/scoreboard"
        try:
            r = requests.get(url,
                             params={"dates": date_iso.replace("-", "")},
                             timeout=10)
            r.raise_for_status()
            events = r.json().get("events", [])
        except Exception as e:
            log.warning(f"Tennis scoreboard ({league} {date_iso}) failed: {e}")
            return []

        games = []
        for event in events:
            for group in event.get("groupings", []):
                for comp in group.get("competitions", []):
                    if comp.get("date", "")[:10] != date_iso:
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
                        start_time=comp.get("date", ""),
                    ))
        return games

    def get_todays_games(self) -> list:
        """
        Fetches ESPN games for today AND yesterday (UTC).  Fetching yesterday
        covers late US evening games that start after UTC midnight (e.g. 9 pm ET
        = 01:00 UTC next day) but whose ESPN date is still the previous day.
        Duplicate games (same matchup and start_time) are deduplicated.
        """
        et        = datetime.timezone(datetime.timedelta(hours=-4), name="ET")
        today     = datetime.datetime.now(et).date()
        yesterday = today - datetime.timedelta(days=1)
        games: list       = []
        seen_keys: set    = set()
        for fetch_date in (yesterday, today):
            date_str = fetch_date.strftime("%Y%m%d")
            for series, (sport, league) in SPORTS_SERIES.items():
                if league in ("wta", "atp"):
                    for g in self._get_tennis_matches(league, fetch_date):
                        key = (g["home"], g["away"], g["start_time"])
                        if key not in seen_keys:
                            seen_keys.add(key)
                            games.append(g)
                else:
                    for ev in self._fetch_scoreboard(sport, league, date_str):
                        rec = self._parse_event(ev, sport, league)
                        if rec:
                            key = (rec["home"], rec["away"], rec["start_time"])
                            if key not in seen_keys:
                                seen_keys.add(key)
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
                       polymarket: Optional[PolymarketSource] = None,
                       already_traded_events: set = None,
                       balance: float = 0.0) -> list:
    """
    Returns all tradeable opportunities sorted by |edge| descending.
    Each opportunity is a flat, JSON-serializable dict.

    Model hierarchy (best available signal used):
      1. Polymarket + ESPN sportsbook odds (50/50 blend)
      2. Polymarket alone
      3. ESPN sportsbook odds alone
      4. ESPN win-rate / recent form

    Strategy: Fade Kalshi — bet on convergence toward model probability.
      edge_pp = (model_prob − kalshi_mid) × 100
      edge_pp > 0 → BUY YES  edge_pp < 0 → BUY NO

    Sizing: fractional Kelly criterion (quarter-Kelly).
      For YES at ask price p:  kelly_f = (model_prob - p) / (1 - p)
      For NO  at ask price p:  kelly_f = ((1-model_prob) - p) / (1 - p)
      bet = kelly_f * KELLY_FRACTION * balance, capped at MAX_BET.
    """
    seen_events: set = set(already_traded_events or [])
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
                    model_prob   = pm_prob
                    model_source = "polymarket"
                log.info(
                    f"Polymarket [{yes_team}]: ESPN={espn_prob:.3f} "
                    f"PM={pm_prob:.3f} blended={model_prob:.3f} "
                    f"'{pm_q[:55]}'"
                )
            else:
                log.info(
                    f"No Polymarket match for [{yes_team}] — "
                    f"using ESPN ({espn_source}): {espn_prob:.3f}"
                )

        kalshi_mid = (yes_ask_f + yes_bid_f) / 2.0
        edge_pp    = (model_prob - kalshi_mid) * 100.0

        if abs(edge_pp) < MIN_EDGE_PP:
            continue

        # Fade Kalshi: buy YES when model (Polymarket) > Kalshi mid, NO otherwise.
        if edge_pp > 0:
            side, price_f = "yes", yes_ask_f
        else:
            side, price_f = "no",  1.0 - yes_bid_f
        price_cents = round(price_f * 100)

        if price_cents < 1 or price_cents > 99:
            continue

        # Fractional Kelly sizing
        # kelly_f = edge / (1 - price) for both YES and NO
        # (for NO, edge = (1-model_prob) - p_no and 1-p_no = yes_bid,
        #  but since we already flipped signs, |edge|/(1-price_f) works uniformly)
        kelly_f  = abs(edge_pp) / 100.0 / (1.0 - price_f) if price_f < 1.0 else 0.0
        budget   = min(MAX_BET, kelly_f * KELLY_FRACTION * balance)
        contracts = int(budget / price_f)
        if contracts < 1:
            continue

        seen_events.add(event_ticker)
        g = match["game"]
        opps.append({
            # Trade execution fields
            "ticker":        market["ticker"],
            "event_ticker":  event_ticker,
            "strategy":     "fade_kalshi",
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
