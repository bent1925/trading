from __future__ import annotations

import json
import logging
import os
from typing import Optional
from datetime import datetime

import requests

log = logging.getLogger(__name__)


class OpponentStrengthDB:
    """
    Manages opponent strength tracking — learns which opponents are strong/weak
    based on head-to-head records from official league APIs.

    Structure:
    {
      "opponent_strength_date": "2026-04-16",
      "data": {
        "team_name": {
          "opponent_name": 0.55,  # win rate vs this opponent
          ...
        },
        ...
      }
    }
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.db = self._load()

    def _load(self) -> dict:
        """Load opponent strength from JSON file, or return empty dict if missing."""
        if not os.path.exists(self.filepath):
            log.info(f"Opponent strength file not found: {self.filepath}. Starting fresh.")
            return {"opponent_strength_date": "", "data": {}}
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except Exception as e:
            log.warning(f"Failed to load opponent strength JSON: {e}. Starting fresh.")
            return {"opponent_strength_date": "", "data": {}}

    def save(self) -> None:
        """Persist to JSON file."""
        try:
            with open(self.filepath, "w") as f:
                json.dump(self.db, f, indent=2)
            log.info(f"Opponent strength saved to {self.filepath}")
        except Exception as e:
            log.error(f"Failed to save opponent strength JSON: {e}")

    def get_opponent_strength(self, team: str, opponent: str) -> float:
        """
        Return the observed win rate for team when playing against opponent.
        If not found, return 0.5 (neutral).
        """
        team_data = self.db.get("data", {}).get(team, {})
        return team_data.get(opponent, 0.5)

    def set_opponent_strength(self, team: str, opponent: str, win_rate: float) -> None:
        """Record or update a team's win rate vs an opponent."""
        if "data" not in self.db:
            self.db["data"] = {}
        if team not in self.db["data"]:
            self.db["data"][team] = {}
        self.db["data"][team][opponent] = round(win_rate, 4)
        self.db["opponent_strength_date"] = datetime.now().isoformat()

    def update_from_trade_result(self, game: dict, winner: str) -> None:
        """
        Update opponent strength based on a resolved trade.

        Args:
            game: {home, away, ...}
            winner: 'home' or 'away' (the team that won)
        """
        home = game.get("home", "")
        away = game.get("away", "")
        if not home or not away:
            return

        # Update home team's record vs away team
        home_won = (winner == "home")
        home_strength = self.get_opponent_strength(home, away)
        # Simple moving average: weight new result at 10%
        updated_home_strength = home_strength * 0.9 + (1.0 if home_won else 0.0) * 0.1
        self.set_opponent_strength(home, away, updated_home_strength)

        # Update away team's record vs home team
        away_won = (winner == "away")
        away_strength = self.get_opponent_strength(away, home)
        updated_away_strength = away_strength * 0.9 + (1.0 if away_won else 0.0) * 0.1
        self.set_opponent_strength(away, home, updated_away_strength)

        log.debug(
            f"Updated opponent strength: {home} vs {away} "
            f"(winner={winner}, home_new={updated_home_strength:.3f}, away_new={updated_away_strength:.3f})"
        )


# ── Bootstrap from ESPN Standings API ──────────────────────────────────────

ESPN_BASE = "https://site.api.espn.com/apis/v2/sports"

_LEAGUE_CONFIGS = [
    ("basketball", "nba"),
    ("baseball",   "mlb"),
    ("hockey",     "nhl"),
]


def _bootstrap_espn_standings(sport: str, league: str) -> dict:
    """
    Fetch team win percentages from ESPN standings (one API call per league).
    Stores each opponent's overall win rate as a proxy for their strength.

    Returns: {team: {opponent: opponent_win_pct, ...}, ...}
    """
    url = f"{ESPN_BASE}/{sport}/{league}/standings"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        log.warning(f"ESPN standings ({sport}/{league}) failed: {e}")
        return {}

    # Extract entries — handle both conference-grouped and flat formats
    entries = []
    for child in data.get("children", []):
        entries.extend(child.get("standings", {}).get("entries", []))
    if not entries:
        entries = data.get("standings", {}).get("entries", [])

    team_win_pcts: dict[str, float] = {}
    for entry in entries:
        name = entry.get("team", {}).get("displayName", "")
        if not name:
            continue
        stats_by_name = {s["name"]: s.get("value") for s in entry.get("stats", []) if "name" in s}

        # Most leagues provide winPercent directly; NHL uses wins/losses/otLosses
        if "winPercent" in stats_by_name and stats_by_name["winPercent"] is not None:
            team_win_pcts[name] = float(stats_by_name["winPercent"])
        elif "wins" in stats_by_name:
            w   = float(stats_by_name.get("wins", 0) or 0)
            l   = float(stats_by_name.get("losses", 0) or 0)
            otl = float(stats_by_name.get("otLosses", 0) or 0)
            gp  = w + l + otl
            if gp >= 5:
                team_win_pcts[name] = round(w / gp, 4)

    if not team_win_pcts:
        log.warning(f"No teams parsed from ESPN standings ({sport}/{league})")
        return {}

    # For each team, store every other team's win pct as their "strength"
    result: dict[str, dict[str, float]] = {}
    for team in team_win_pcts:
        result[team] = {
            opp: round(pct, 4)
            for opp, pct in team_win_pcts.items()
            if opp != team
        }

    log.info(f"ESPN standings ({league}): {len(result)} teams")
    return result


def bootstrap_daily(db: OpponentStrengthDB) -> None:
    """
    Refresh opponent strength from ESPN standings for all active leagues.
    Skips if the database was already updated today.
    """
    today = datetime.now().date().isoformat()
    last_update = db.db.get("opponent_strength_date", "")[:10]
    if last_update == today:
        log.info("Opponent strength already up-to-date for today — skipping bootstrap.")
        return

    log.info("Bootstrapping opponent strength from ESPN standings…")
    merged = {**db.db.get("data", {})}

    for sport, league in _LEAGUE_CONFIGS:
        league_data = _bootstrap_espn_standings(sport, league)
        for team, opponents in league_data.items():
            if team not in merged:
                merged[team] = {}
            merged[team].update(opponents)

    db.db["data"] = merged
    db.db["opponent_strength_date"] = datetime.now().isoformat()
    db.save()
    log.info(f"Bootstrap complete — {len(merged)} teams in database.")
