import json
import logging
from typing import Optional

import requests

from .utils import words

log = logging.getLogger(__name__)


class PolymarketSource:
    """
    Fetches Polymarket prices via targeted per-game searches against the Gamma API.
    Uses the API's `q` search parameter so only relevant markets are fetched,
    rather than bulk-loading all 48,000+ active markets.
    """
    GAMMA_URL = "https://gamma-api.polymarket.com/markets"

    # Per-league blocklist: words that disqualify a Polymarket market.
    # Prevents cross-sport name matches (e.g. NBA team matching MLS draw market).
    _BLOCKLIST = {
        "nba": {"draw", "soccer", "mls", "nhl", "hockey", "tennis", "wta",
                "atp", "baseball", "mlb", "nfl", "football"},
        "nhl": {"draw", "soccer", "mls", "nba", "basketball", "tennis", "wta",
                "atp", "baseball", "mlb", "nfl", "football"},
        "mlb": {"draw", "soccer", "mls", "nba", "basketball", "tennis", "wta",
                "atp", "nhl", "hockey", "nfl", "football"},
        "wta": {"draw", "soccer", "mls", "nba", "basketball", "nhl", "hockey",
                "baseball", "mlb", "nfl", "football"},
        "atp": {"draw", "soccer", "mls", "nba", "basketball", "nhl", "hockey",
                "baseball", "mlb", "nfl", "football"},
    }

    def _search(self, query: str) -> list:
        """Search Polymarket for markets matching query. Returns list of markets."""
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

        Searches Polymarket for markets matching each team name, applies
        blocklist filtering, then selects the best fuzzy match.
        """
        yes_w     = set(words(yes_team))
        other_w   = set(words(other_team))
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
                q_w = set(words(m.get("question", "")))
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
            outcomes = json.loads(best_m.get("outcomes",      "[]"))
        except (json.JSONDecodeError, TypeError):
            return None
        if len(prices) < 2:
            return None

        p0       = float(prices[0])
        question = best_m.get("question", "")

        # If outcomes are team-labeled, match directly
        out0_w = set(words(outcomes[0])) if outcomes else set()
        out1_w = set(words(outcomes[1])) if len(outcomes) > 1 else set()
        if yes_w & out0_w:
            return (p0, question)
        if yes_w & out1_w:
            return (1.0 - p0, question)

        # Yes/No outcomes — use which team appears first in the question
        q_lower     = question.lower()
        first_yes   = min((q_lower.find(w) for w in yes_w   if w in q_lower), default=9999)
        first_other = min((q_lower.find(w) for w in other_w if w in q_lower), default=9999)
        if first_yes == 9999 and first_other == 9999:
            return None
        return (p0, question) if first_yes <= first_other else (1.0 - p0, question)
