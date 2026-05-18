"""
Balance chart: reads kalshi_balance_log.json and regenerates BALANCE.md
with an ASCII bar chart + data table. Called after every run.
"""
import logging
import os
import re

from .config import BALANCE_LOG_FILE, BALANCE_MD, MODEL_OUTPUTS_DIR

log = logging.getLogger(__name__)

_BAR_WIDTH = 44


def update_balance_md() -> None:
    with open(BALANCE_MD, "w") as f:
        f.write(_render_md())
    log.info("BALANCE.md updated")


def backfill_from_model_outputs() -> None:
    """Parse existing model_outputs/*.md to seed kalshi_balance_log.json."""
    import json
    if not os.path.isdir(MODEL_OUTPUTS_DIR):
        return
    existing = {(e.get("date") or e["timestamp"][:10]) for e in _load_log()}
    pattern  = re.compile(r"\*\*Account balance:\*\* \$([0-9]+\.[0-9]+)")
    new_entries = []

    for fname in sorted(os.listdir(MODEL_OUTPUTS_DIR)):
        if not fname.endswith(".md"):
            continue
        date_str = fname[:-3]
        if date_str in existing:
            continue
        path = os.path.join(MODEL_OUTPUTS_DIR, fname)
        with open(path) as f:
            text = f.read()
        m = pattern.search(text)
        if m:
            new_entries.append({
                "timestamp":   f"{date_str}T00:00:00Z",
                "date":        date_str,
                "balance_usd": float(m.group(1)),
            })

    if new_entries:
        entries = sorted(_load_log() + new_entries, key=lambda e: e["timestamp"])
        with open(BALANCE_LOG_FILE, "w") as f:
            json.dump(entries, f, indent=2)
        log.info(f"Backfilled {len(new_entries)} balance reading(s) from model_outputs/")


def _load_log() -> list:
    import json
    if not os.path.exists(BALANCE_LOG_FILE):
        return []
    with open(BALANCE_LOG_FILE) as f:
        return json.load(f)


def _render_md() -> str:
    entries = _load_log()
    if not entries:
        return "# Account Balance\n\nNo data yet.\n"

    # One display row per calendar date — keep the last reading of each day.
    # Entries from update_balance_log use "timestamp"; backfilled entries also
    # carry "date". Handle both formats.
    by_date: dict[str, float] = {}
    for e in entries:
        date_key = e.get("date") or e["timestamp"][:10]
        by_date[date_key] = e["balance_usd"]

    dates    = sorted(by_date)
    balances = [by_date[d] for d in dates]
    current  = balances[-1]
    start    = balances[0]
    delta    = current - start
    pnl_str  = f"+${delta:.2f}" if delta >= 0 else f"-${abs(delta):.2f}"

    lines = [
        "# Account Balance",
        "",
        f"**Current:** ${current:.2f}  ·  "
        f"**Starting:** ${start:.2f}  ·  "
        f"**Total P&L:** {pnl_str}",
        "",
        "## Chart",
        "",
        "```",
    ]

    min_bal   = min(balances)
    max_bal   = max(balances)
    bal_range = max_bal - min_bal

    for date, bal in zip(dates, balances):
        if bal_range > 0:
            bar_len = max(1, round((bal - min_bal) / bal_range * _BAR_WIDTH))
        else:
            bar_len = _BAR_WIDTH
        lines.append(f"{date}  ${bal:>8.2f}  {'█' * bar_len}")

    if bal_range > 0:
        lines.append(f"                   min ${min_bal:.2f}  max ${max_bal:.2f}")
    lines += ["```", ""]

    lines += [
        "## Data",
        "",
        "| Date | Balance | Change |",
        "|------|---------|--------|",
    ]
    prev = None
    for date, bal in zip(dates, balances):
        if prev is None:
            change = "—"
        else:
            d = bal - prev
            change = f"+${d:.2f}" if d >= 0 else f"-${abs(d):.2f}"
        lines.append(f"| {date} | ${bal:.2f} | {change} |")
        prev = bal
    lines.append("")

    return "\n".join(lines)
