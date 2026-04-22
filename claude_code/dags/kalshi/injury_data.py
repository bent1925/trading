"""
Injury data integration using ESPN's free public API.

Fetches "Out" and "Questionable" players per team for NBA, MLB, and NHL.
No API key required. Used to dampen win-probability estimates in the
win-rate fallback model path (Tier 4 only — sportsbook odds and Polymarket
already price in injuries).
"""

from __future__ import annotations

import logging
from typing import Optional

import requests

log = logging.getLogger(__name__)

ESPN_BASE = "http://site.api.espn.com/apis/site/v2/sports"

# ESPN sport/league paths for supported leagues
_LEAGUE_PATHS = {
    "nba": ("basketball", "nba"),
    "mlb": ("baseball",   "mlb"),
    "nhl": ("hockey",     "nhl"),
}

# Statuses treated as "out" (full deduction) vs "questionable" (half deduction)
_OUT_STATUSES         = {"out", "injured reserve", "physically unable to perform", "suspended"}
_QUESTIONABLE_STATUSES = {"questionable", "day-to-day"}


class ESPNInjurySource:
    """
    Fetches team injury reports from ESPN's public API.

    Data is fetched once per instance and cached in memory for the lifetime
    of the run — one bot run fetches injuries once, then reuses the cache
    for all market evaluations.

    Usage:
        source = ESPNInjurySource()
        unavailable = source.get_unavailable("Boston Celtics", "nba")
        # → {"Jaylen Brown": "questionable", "Kristaps Porziņģis": "out"}
    """

    def __init__(self):
        # Cache: {league: {team_display_name: {player: status}}}
        self._cache: dict[str, dict[str, dict[str, str]]] = {}

    def _fetch_league(self, league: str) -> dict[str, dict[str, str]]:
        """Fetch and parse injury report for one league. Returns {team: {player: status}}."""
        if league not in _LEAGUE_PATHS:
            return {}
        sport, lg = _LEAGUE_PATHS[league]
        url = f"{ESPN_BASE}/{sport}/{lg}/injuries"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            log.warning(f"ESPN injuries ({league}) failed: {e}")
            return {}

        result: dict[str, dict[str, str]] = {}
        for team_block in data.get("injuries", []):
            # Team name is at the top level as "displayName"
            team_name = team_block.get("displayName", "")
            if not team_name:
                continue
            players: dict[str, str] = {}
            for entry in team_block.get("injuries", []):
                player = entry.get("athlete", {}).get("displayName", "")
                # status field (e.g. "Out", "Questionable") is the clearest signal
                status = entry.get("status", "").lower().strip()
                if not status:
                    # fall back to type description
                    status = entry.get("type", {}).get("description", "").lower().strip()
                if player and status:
                    players[player] = status
            if players:
                result[team_name] = players

        log.info(
            f"ESPN injuries ({league}): {len(result)} teams, "
            f"{sum(len(v) for v in result.values())} players listed"
        )
        return result

    def get_unavailable(self, team: str, league: str) -> dict[str, str]:
        """
        Returns {player_name: status_string} for players who are Out or
        Questionable for the given team.

        Args:
            team:   ESPN display name, e.g. "Boston Celtics"
            league: lowercase league key, e.g. "nba", "mlb", "nhl"

        Returns:
            Dict of player → status for Out/Questionable players only.
            Empty dict if no data available or team not found.
        """
        if league not in self._cache:
            self._cache[league] = self._fetch_league(league)

        team_injuries = self._cache[league].get(team, {})

        # Filter to only actionable statuses
        return {
            player: status
            for player, status in team_injuries.items()
            if any(s in status for s in (*_OUT_STATUSES, *_QUESTIONABLE_STATUSES))
        }
