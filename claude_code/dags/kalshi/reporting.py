"""
Shared reporting helpers used by both trading_dag.py (Airflow)
and run_daily.py (standalone). No Airflow dependency.
"""
import json
import logging
import os
import re

from .config import (BALANCE_LOG_DISPLAY_ROWS, BALANCE_LOG_FILE,
                     MAX_TRADES_PER_RUN, MODEL_OUTPUTS_DIR, TRADES_MD)

log = logging.getLogger(__name__)


def write_model_output(date_str: str, balance: float, markets_n: int,
                       games_n: int, opps: list) -> str:
    """
    Write today's model analysis to model_outputs/YYYY-MM-DD.md.
    Returns the path written.
    """
    import datetime
    selected = opps[:MAX_TRADES_PER_RUN]

    lines = [
        f"# Model Output — {date_str}",
        "",
        f"**Run time (UTC):** {datetime.datetime.utcnow().isoformat()}Z",
        f"**Account balance:** ${balance:.2f}",
        f"**Kalshi markets scanned:** {markets_n}",
        f"**ESPN games found:** {games_n}",
        "",
    ]

    if not opps:
        lines += ["## Result", "", "No opportunities above the edge threshold today."]
    else:
        lines += [
            "## Opportunities Above Threshold (|edge| > 10 pp)",
            "",
            "| # | Market | Sport | Side | Model | ESPN | Kalshi Mid | Edge | Source |",
            "|---|--------|-------|------|-------|------|-----------|------|--------|",
        ]
        for i, o in enumerate(opps, 1):
            marker = " ✓" if i <= MAX_TRADES_PER_RUN else ""
            lines.append(
                f"| {i}{marker} "
                f"| {o['title']} "
                f"| {o['league'].upper()} "
                f"| BUY {o['side'].upper()} "
                f"| {o['model_prob']*100:.1f}% "
                f"| {o['espn_prob']*100:.1f}% "
                f"| {o['kalshi_mid']*100:.1f}¢ "
                f"| {o['edge_pp']:+.1f} pp "
                f"| {o['model_source']} |"
            )
        lines += [
            "",
            f"**Selected for trading:** {len(selected)} / {MAX_TRADES_PER_RUN} daily slots",
        ]

    os.makedirs(MODEL_OUTPUTS_DIR, exist_ok=True)
    path = os.path.join(MODEL_OUTPUTS_DIR, f"{date_str}.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    log.info(f"Model output → {path}")
    return path


def _strategy_desc(model_source: str) -> str:
    """Convert a model_source label into a human-readable strategy description."""
    s = (model_source or "").strip()
    if not s or s == "—":
        return "unknown"
    if s == "espn_odds(50%)+polymarket(50%)":
        return "Fade Kalshi → 50% ESPN sportsbook + 50% Polymarket"
    if s == "polymarket":
        return "Fade Kalshi → Polymarket"
    if s == "espn:espn_odds":
        return "Fade Kalshi → ESPN sportsbook odds (no Polymarket match)"
    if s.startswith("espn:win_pct+form"):
        return "Fade Kalshi → ESPN win-rate + recent form (no Polymarket or ESPN odds)"
    if s.startswith("espn:win_pct"):
        return "Fade Kalshi → ESPN season win-rate (weakest fallback)"
    if "ranking" in s:
        return f"Fade Kalshi → tennis ranking model ({s})"
    return s


def update_trades_md(date_str: str, trades: list) -> None:
    """
    Insert or replace today's section in TRADES.md (most-recent-first order).
    """
    section_lines = [f"## {date_str}", ""]

    if not trades:
        section_lines += ["No trades placed today.", ""]
    else:
        section_lines += [
            "| # | Market | Sport | Bet | Amount | ESPN | Model (blended) "
            "| Kalshi Mid | Edge | Strategy | Result |",
            "|---|--------|-------|-----|--------|------|-----------------|"
            "-----------|------|----------|--------|",
        ]
        total_cost = 0.0
        total_pnl = 0.0
        all_resolved = True
        for i, t in enumerate(trades, 1):
            if t.get("resolved"):
                filled = t.get("filled", 0)
                pnl    = t.get("pnl_usd", 0.0)
                total_pnl += pnl
                won = (t["side"] == "yes" and t["market_result"] == "yes") or \
                      (t["side"] == "no"  and t["market_result"] == "no")
                if filled == 0:
                    result_str = "— (unfilled)"
                elif won:
                    result_str = f"✅ WIN +${pnl:.2f}"
                else:
                    result_str = f"❌ LOSS −${abs(pnl):.2f}"
            else:
                result_str  = "pending"
                all_resolved = False

            espn_col = f"| {t['espn_prob']*100:.1f}% " if 'espn_prob' in t else "| — "
            strategy = _strategy_desc(t.get("model_source", ""))
            section_lines.append(
                f"| {i} "
                f"| {t['title']} "
                f"| {t.get('league', t.get('sport', '')).upper()} "
                f"| BUY {t['side'].upper()} "
                f"| ${t['cost_usd']:.2f} ({t['contracts']} × {t['price_cents']}¢) "
                + espn_col +
                f"| {t['model_prob']*100:.1f}% "
                f"| {t['kalshi_mid']*100:.1f}¢ "
                f"| {t['edge_pp']:+.1f} pp "
                f"| {strategy} "
                f"| {result_str} |"
            )
            total_cost += t["cost_usd"]

        summary = f"**Total wagered: ${total_cost:.2f}**"
        if all_resolved:
            pnl_sign = "+" if total_pnl >= 0 else "−"
            summary += f"  |  **Net P&L: {pnl_sign}${abs(total_pnl):.2f}**"
        section_lines += ["", summary, ""]

    section_lines += ["---", ""]
    today_section = "\n".join(section_lines)

    if os.path.exists(TRADES_MD):
        with open(TRADES_MD) as f:
            content = f.read()
    else:
        content = _default_header()

    # Split on date-section markers (## YYYY-MM-DD), keep header intact
    parts  = re.split(r"(?=^## \d{4}-\d{2}-\d{2})", content, flags=re.MULTILINE)
    header = parts[0]
    dated  = [p for p in parts[1:] if not p.startswith(f"## {date_str}")]

    with open(TRADES_MD, "w") as f:
        f.write(header + today_section + "".join(dated))
    log.info(f"TRADES.md updated ({len(trades)} trade(s) for {date_str})")


def _default_header() -> str:
    return """\
# Trade Log

All trades placed by `claude_code/dags/trading_dag.py`.
Prices are the limit-order ask price (YES bets) or `1 − bid` (NO bets).
Model and ESPN probabilities are for the YES outcome.

---

"""


# ── Balance log ─────────────────────────────────────────────────────────────

def _load_balance_log() -> list:
    """Return the full balance history, or [] if the file does not exist."""
    if not os.path.exists(BALANCE_LOG_FILE):
        return []
    with open(BALANCE_LOG_FILE) as f:
        return json.load(f)


def _save_balance_log(entries: list) -> None:
    with open(BALANCE_LOG_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def _render_balance_section(entries: list) -> str:
    """Build the markdown for the `## Account Balance` section."""
    if not entries:
        return ""

    latest      = entries[-1]
    latest_bal  = latest["balance_usd"]
    latest_when = latest["timestamp"].replace("T", " ").rstrip("Z")[:16]
    first_bal   = entries[0]["balance_usd"]
    delta       = latest_bal - first_bal
    delta_sign  = "+" if delta >= 0 else "−"

    lines = [
        "## Account Balance",
        "",
        f"**Current cash balance:** ${latest_bal:.2f} "
        f"(as of {latest_when} UTC) "
        f"&nbsp;·&nbsp; **Since first log:** {delta_sign}${abs(delta):.2f}",
        "",
        "Cash balance only — does not include the value of open limit orders or unsettled positions. "
        f"Showing the most recent {BALANCE_LOG_DISPLAY_ROWS} of {len(entries)} entries.",
        "",
        "| Timestamp (UTC) | Cash Balance |",
        "|-----------------|-------------:|",
    ]
    for e in reversed(entries[-BALANCE_LOG_DISPLAY_ROWS:]):
        ts = e["timestamp"].replace("T", " ").rstrip("Z")[:16]
        lines.append(f"| {ts} | ${e['balance_usd']:.2f} |")

    lines += ["", "---", ""]
    return "\n".join(lines) + "\n"


def update_balance_log(balance: float, when_iso: str) -> None:
    """
    Append a balance entry to the JSON log and rewrite the
    `## Account Balance` section in TRADES.md.
    """
    entries = _load_balance_log()
    entries.append({"timestamp": when_iso, "balance_usd": round(balance, 2)})
    _save_balance_log(entries)

    section = _render_balance_section(entries)

    if os.path.exists(TRADES_MD):
        with open(TRADES_MD) as f:
            content = f.read()
    else:
        content = _default_header()

    # Replace existing section or insert before the first dated section
    bal_re = re.compile(
        r"(?ms)^## Account Balance\b.*?(?=^## |\Z)"
    )
    if bal_re.search(content):
        new_content = bal_re.sub(section, content, count=1)
    else:
        date_match = re.search(r"^## \d{4}-\d{2}-\d{2}", content, flags=re.MULTILINE)
        if date_match:
            new_content = content[:date_match.start()] + section + content[date_match.start():]
        else:
            new_content = content + section

    with open(TRADES_MD, "w") as f:
        f.write(new_content)
    log.info(f"Balance log updated: ${balance:.2f} ({len(entries)} entries total)")
