import re
import datetime
from typing import Optional

from .config import SPORTS_SERIES

_MONTH_MAP = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
}


def words(name: str) -> list:
    """Lower-case words longer than 2 chars."""
    return [w for w in re.split(r"\W+", name.lower()) if len(w) > 2]


def overlap(text: str, team: str) -> int:
    tw = set(words(text))
    return sum(1 for w in words(team) if w in tw)


def parse_ticker_date(series: str, ticker: str) -> Optional[datetime.date]:
    """
    Extracts the game date encoded in a Kalshi ticker.
    Pattern after series prefix: YY{MON}DD  e.g. 26MAR26 → March 26 2026.
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
