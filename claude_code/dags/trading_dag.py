"""
Kalshi Sports Trading DAG
=========================
Runs daily at 06:00 America/Los_Angeles.

Tasks
-----
1. build_model        — fetch Kalshi markets, ESPN games, Polymarket prices;
                        compute all opportunities above the edge threshold.
2. log_model_output   — write today's model analysis to model_outputs/YYYY-MM-DD.md.
3. make_trades        — execute the top-N trades on Kalshi; persist to JSON log.
4. update_trade_log   — append / replace today's section in TRADES.md.

Data flows between tasks via XCom (all values are plain JSON dicts/lists).
"""

import datetime
import logging
import os
import sys

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

# Make the kalshi package importable when Airflow runs this file
sys.path.insert(0, os.path.dirname(__file__))

from kalshi.client      import KalshiClient
from kalshi.config      import (KALSHI_KEY_ID, KALSHI_KEY_FILE,
                                 MAX_TRADES_PER_DAY, TRADES_MD,
                                 MODEL_OUTPUTS_DIR)
from kalshi.model       import ProbabilityModel, find_opportunities
from kalshi.polymarket  import PolymarketSource
from kalshi.trade_log   import load_today, save_today

log = logging.getLogger(__name__)


# ── Task 1: Build Model ───────────────────────────────────────────────────────

def build_model(**context) -> dict:
    """
    Fetches all data sources and computes trading opportunities.
    Returns a dict pushed to XCom for downstream tasks.
    """
    date_str = str(datetime.date.today())

    if not KALSHI_KEY_ID or not KALSHI_KEY_FILE:
        raise RuntimeError("KALSHI_KEY_ID and KALSHI_KEY_FILE must be set.")

    client  = KalshiClient(KALSHI_KEY_ID, KALSHI_KEY_FILE)
    balance = client.get_balance_usd()
    log.info(f"Account balance: ${balance:.2f}")

    log.info("Fetching Kalshi markets…")
    markets = client.get_todays_game_markets()
    log.info(f"Found {len(markets)} game markets")

    log.info("Building ESPN probability model…")
    model = ProbabilityModel()
    games = model.get_todays_games()
    log.info(f"ESPN returned {len(games)} games")

    log.info("Fetching Polymarket prices…")
    pm = PolymarketSource()
    pm_count = pm.load()

    log.info("Finding opportunities…")
    opps = find_opportunities(markets, games, polymarket=pm)
    log.info(f"Found {len(opps)} opportunities above threshold")

    return {
        "date":             date_str,
        "run_time":         datetime.datetime.utcnow().isoformat() + "Z",
        "balance":          round(balance, 2),
        "markets_found":    len(markets),
        "games_found":      len(games),
        "polymarket_count": pm_count,
        "opportunities":    opps,   # already flat JSON-safe dicts
    }


# ── Task 2: Log Model Output ──────────────────────────────────────────────────

def log_model_output(ti=None, **context) -> None:
    """
    Writes today's model analysis to model_outputs/YYYY-MM-DD.md.
    Captures all opportunities (above threshold) before any trades are placed.
    """
    data = ti.xcom_pull(task_ids="build_model")
    if not data:
        raise ValueError("No data from build_model task.")

    date_str  = data["date"]
    opps      = data["opportunities"]
    selected  = opps[:MAX_TRADES_PER_DAY]

    os.makedirs(MODEL_OUTPUTS_DIR, exist_ok=True)
    path = os.path.join(MODEL_OUTPUTS_DIR, f"{date_str}.md")

    lines = [
        f"# Model Output — {date_str}",
        "",
        f"**Run time (UTC):** {data['run_time']}",
        f"**Account balance:** ${data['balance']:.2f}",
        f"**Kalshi markets scanned:** {data['markets_found']}",
        f"**ESPN games found:** {data['games_found']}",
        f"**Polymarket markets loaded:** {data['polymarket_count']:,}",
        "",
    ]

    if not opps:
        lines += [
            "## Result",
            "",
            "No opportunities above the edge threshold today.",
        ]
    else:
        lines += [
            f"## Opportunities Above Threshold (|edge| > 10 pp)",
            "",
            "| # | Market | Sport | Side | Model | ESPN | Kalshi Mid | Edge | Source |",
            "|---|--------|-------|------|-------|------|-----------|------|--------|",
        ]
        for i, o in enumerate(opps, 1):
            selected_marker = " ✓" if i <= MAX_TRADES_PER_DAY else ""
            lines.append(
                f"| {i}{selected_marker} "
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

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")

    log.info(f"Model output written to {path}")


# ── Task 3: Make Trades ───────────────────────────────────────────────────────

def make_trades(ti=None, **context) -> dict:
    """
    Executes the selected trades on Kalshi, updates the JSON trade log.
    Returns the list of executed trades for the update_trade_log task.
    """
    data = ti.xcom_pull(task_ids="build_model")
    if not data:
        raise ValueError("No data from build_model task.")

    date_str  = data["date"]
    opps      = data["opportunities"]
    trade_log = load_today(date_str)
    already   = trade_log["count"]

    if already >= MAX_TRADES_PER_DAY:
        log.info(f"Already placed {already} trades today — skipping.")
        return {"date": date_str, "trades": trade_log["trades"]}

    remaining = MAX_TRADES_PER_DAY - already
    selected  = opps[:remaining]

    if not selected:
        log.info("No opportunities to trade today.")
        return {"date": date_str, "trades": trade_log["trades"]}

    client = KalshiClient(KALSHI_KEY_ID, KALSHI_KEY_FILE)

    for opp in selected:
        try:
            result = client.place_order(
                ticker      = opp["ticker"],
                side        = opp["side"],
                price_cents = opp["price_cents"],
                count       = opp["contracts"],
            )
            order  = result.get("order", {})
            status = order.get("status", "unknown")
            oid    = order.get("order_id")
            log.info(
                f"Order {status}: {opp['ticker']} {opp['side'].upper()} "
                f"×{opp['contracts']} @ {opp['price_cents']}¢  id={oid}"
            )
        except Exception as e:
            log.error(f"Order failed for {opp['ticker']}: {e}")
            status, oid = "failed", None

        trade_log["trades"].append({
            "timestamp":    datetime.datetime.utcnow().isoformat() + "Z",
            "ticker":       opp["ticker"],
            "title":        opp["title"],
            "side":         opp["side"],
            "price_cents":  opp["price_cents"],
            "contracts":    opp["contracts"],
            "cost_usd":     opp["cost_usd"],
            "model_prob":   opp["model_prob"],
            "espn_prob":    opp["espn_prob"],
            "model_source": opp["model_source"],
            "kalshi_mid":   opp["kalshi_mid"],
            "edge_pp":      opp["edge_pp"],
            "order_id":     oid,
            "status":       status,
        })
        trade_log["count"] += 1

    save_today(trade_log)
    log.info(f"Placed {trade_log['count'] - already} trades; "
             f"daily total {trade_log['count']}/{MAX_TRADES_PER_DAY}")

    return {"date": date_str, "trades": trade_log["trades"]}


# ── Task 4: Update Trade Log (TRADES.md) ─────────────────────────────────────

def update_trade_log(ti=None, **context) -> None:
    """
    Inserts or replaces today's section in TRADES.md.
    """
    result = ti.xcom_pull(task_ids="make_trades")
    if not result:
        raise ValueError("No data from make_trades task.")

    date_str = result["date"]
    trades   = result["trades"]

    # Build today's markdown section
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
            yes_team = t.get("title", "")
            side_str = f"BUY {t['side'].upper()}"
            amount   = f"${t['cost_usd']:.2f} ({t['contracts']} × {t['price_cents']}¢)"
            mid_str  = f"{t['kalshi_mid']*100:.1f}¢"
            section_lines.append(
                f"| {i} | {t['title']} | {t.get('league','').upper()} "
                f"| {side_str} | {amount} "
                f"| {t['espn_prob']*100:.1f}% "
                f"| {t['model_prob']*100:.1f}% "
                f"| {mid_str} "
                f"| {t['edge_pp']:+.1f} pp "
                f"| {t['model_source']} "
                f"| pending |"
            )
            total_cost += t["cost_usd"]
        section_lines += ["", f"**Total wagered: ${total_cost:.2f}**", ""]

    section_lines.append("---")
    section_lines.append("")
    today_section = "\n".join(section_lines)

    # Read existing TRADES.md and splice in today's section
    if os.path.exists(TRADES_MD):
        with open(TRADES_MD) as f:
            content = f.read()
    else:
        content = _default_trades_header()

    # Split on date-section boundaries (## YYYY-MM-DD)
    import re
    parts = re.split(r"(?=^## \d{4}-\d{2}-\d{2})", content, flags=re.MULTILINE)
    header = parts[0]
    dated  = parts[1:]

    # Remove existing section for today if present
    dated = [p for p in dated if not p.startswith(f"## {date_str}")]

    # Insert today's section at the top (most recent first)
    new_content = header + today_section + "".join(dated)

    with open(TRADES_MD, "w") as f:
        f.write(new_content)

    log.info(f"TRADES.md updated with {len(trades)} trade(s) for {date_str}")


def _default_trades_header() -> str:
    return """\
# Trade Log

All trades placed by the Kalshi sports trading DAG (`claude_code/dags/trading_dag.py`).
Prices are the limit-order ask price (YES bets) or `1 − bid` (NO bets).
Model and ESPN probabilities are for the YES outcome.

---

"""


# ── DAG Definition ────────────────────────────────────────────────────────────

with DAG(
    dag_id           = "kalshi_sports_trading",
    description      = "Daily Kalshi sports trading bot",
    schedule_interval= "0 6 * * *",
    start_date       = pendulum.datetime(2026, 3, 29, tz="America/Los_Angeles"),
    catchup          = False,
    default_args     = {
        "retries":           1,
        "retry_delay":       datetime.timedelta(minutes=5),
        "execution_timeout": datetime.timedelta(minutes=30),
    },
    tags=["trading", "kalshi", "sports"],
) as dag:

    t1_build_model = PythonOperator(
        task_id         = "build_model",
        python_callable = build_model,
    )

    t2_log_model = PythonOperator(
        task_id         = "log_model_output",
        python_callable = log_model_output,
    )

    t3_make_trades = PythonOperator(
        task_id         = "make_trades",
        python_callable = make_trades,
    )

    t4_update_log = PythonOperator(
        task_id         = "update_trade_log",
        python_callable = update_trade_log,
    )

    t1_build_model >> t2_log_model >> t3_make_trades >> t4_update_log
