"""
Shared reporting helpers used by both trading_dag.py (Airflow)
and run_daily.py (standalone). No Airflow dependency.
"""
import logging
import os
import re

from .config import MAX_TRADES_PER_DAY, MODEL_OUTPUTS_DIR, TRADES_MD

log = logging.getLogger(__name__)


def write_model_output(date_str: str, balance: float, markets_n: int,
                       games_n: int, pm_count: int, opps: list) -> str:
    """
    Write today's model analysis to model_outputs/YYYY-MM-DD.md.
    Returns the path written.
    """
    import datetime
    selected = opps[:MAX_TRADES_PER_DAY]

    lines = [
        f"# Model Output — {date_str}",
        "",
        f"**Run time (UTC):** {datetime.datetime.utcnow().isoformat()}Z",
        f"**Account balance:** ${balance:.2f}",
        f"**Kalshi markets scanned:** {markets_n}",
        f"**ESPN games found:** {games_n}",
        f"**Polymarket markets loaded:** {pm_count:,}",
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
            marker = " ✓" if i <= MAX_TRADES_PER_DAY else ""
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
            f"**Selected for trading:** {len(selected)} / {MAX_TRADES_PER_DAY} daily slots",
        ]

    os.makedirs(MODEL_OUTPUTS_DIR, exist_ok=True)
    path = os.path.join(MODEL_OUTPUTS_DIR, f"{date_str}.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    log.info(f"Model output → {path}")
    return path


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
            "| Kalshi Mid | Edge | Source | Result |",
            "|---|--------|-------|-----|--------|------|-----------------|"
            "-----------|------|--------|--------|",
        ]
        total_cost = 0.0
        for i, t in enumerate(trades, 1):
            section_lines.append(
                f"| {i} "
                f"| {t['title']} "
                f"| {t.get('league', t.get('sport', '')).upper()} "
                f"| BUY {t['side'].upper()} "
                f"| ${t['cost_usd']:.2f} ({t['contracts']} × {t['price_cents']}¢) "
                f"| {t['espn_prob']*100:.1f}% "
                f"| {t['model_prob']*100:.1f}% "
                f"| {t['kalshi_mid']*100:.1f}¢ "
                f"| {t['edge_pp']:+.1f} pp "
                f"| {t['model_source']} "
                f"| pending |"
            )
            total_cost += t["cost_usd"]
        section_lines += ["", f"**Total wagered: ${total_cost:.2f}**", ""]

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
