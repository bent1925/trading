import json
import logging
from typing import Optional

import requests

from .utils import words

log = logging.getLogger(__name__)


class PolymarketSource:
    """
    Fetches active market prices from Polymarket's public Gamma API (no API key).
    Used as a second market-consensus signal alongside the ESPN model.
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

    def __init__(self):
        self._markets: Optional[list] = None

    def load(self) -> int:
        """Fetch all active markets. Returns count loaded. Idempotent."""
        if self._markets is not None:
            return len(self._markets)
        all_markets: list = []
        offset = 0
        while True:
            try:
                r = requests.get(
                    self.GAMMA_URL,
                    params={"active": "true", "closed": "false",
                            "limit": 500, "offset": offset},
                    timeout=15,
                )
                r.raise_for_status()
                batch = r.json()
            except Exception as e:
                log.warning(f"Polymarket fetch failed (offset={offset}): {e}")
                break
            if not isinstance(batch, list) or not batch:
                break
            all_markets.extend(batch)
            if len(batch) < 500:
                break
            offset += 500
        self._markets = all_markets
        log.info(f"Polymarket: loaded {len(all_markets)} active markets")
        return len(all_markets)

    def get_prob(self, yes_team: str, other_team: str,
                 league: str = "") -> Optional[tuple]:
        """
        Returns (prob_yes_team_wins: float, matched_question: str) or None.

        Fuzzy-matches both team names against Polymarket questions.
        Markets containing blocklisted sport keywords are rejected.
        Outcome framing is determined by team name labels or question word order.
        """
        self.load()
        yes_w     = set(words(yes_team))
        other_w   = set(words(other_team))
        blocklist = self._BLOCKLIST.get(league, set())
        if not yes_w or not other_w:
            return None

        best_m, best_score = None, 0
        for m in self._markets:
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
