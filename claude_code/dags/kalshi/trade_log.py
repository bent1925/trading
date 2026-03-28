import json
import os
from typing import Optional

from .config import TRADE_LOG_FILE


def load_today(date: str) -> dict:
    """
    Returns {"date": date, "trades": [...], "count": N} for the given date.
    Reads the multi-day JSON log; migrates old single-day format if needed.
    """
    all_logs = _read_all()
    if date in all_logs:
        e = all_logs[date]
        return {"date": date, "trades": e["trades"], "count": e["count"]}
    return {"date": date, "trades": [], "count": 0}


def save_today(log_data: dict) -> None:
    """Merge today's entry into the full multi-day log and write to disk."""
    date     = log_data["date"]
    all_logs = _read_all()
    all_logs[date] = {"trades": log_data["trades"], "count": log_data["count"]}
    with open(TRADE_LOG_FILE, "w") as f:
        json.dump(all_logs, f, indent=2)


def _read_all() -> dict:
    if not os.path.exists(TRADE_LOG_FILE):
        return {}
    with open(TRADE_LOG_FILE) as f:
        data = json.load(f)
    # Migrate old single-day format {"date":…,"trades":…,"count":…}
    if "date" in data and "trades" in data and isinstance(data["trades"], list):
        old_date  = data["date"]
        old_entry = {"trades": data["trades"],
                     "count":  data.get("count", len(data["trades"]))}
        data = {old_date: old_entry}
        with open(TRADE_LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)
    return data
