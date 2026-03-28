#!/usr/bin/env python3
"""
Standalone daily runner — equivalent to the Airflow DAG without requiring Airflow.
Called by run_daily.sh, which is scheduled via launchd at 06:00 PT.

Steps
-----
1. build_model       — fetch Kalshi markets, ESPN games, Polymarket prices
2. log_model_output  — write model_outputs/YYYY-MM-DD.md
3. make_trades       — execute orders on Kalshi, persist to kalshi_trades.json
4. update_trade_log  — insert/replace today's section in TRADES.md
5. git_push          — commit changed files and push to GitHub
"""

import datetime
import logging
import os
import subprocess
import sys

# Make the kalshi package importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "dags"))

from kalshi.client     import KalshiClient
from kalshi.config     import (KALSHI_KEY_ID, KALSHI_KEY_FILE,
                                MAX_TRADES_PER_DAY, TRADING_ROOT,
                                TRADES_MD, MODEL_OUTPUTS_DIR)
from kalshi.model      import ProbabilityModel, find_opportunities
from kalshi.polymarket import PolymarketSource
from kalshi.reporting  import write_model_output, update_trades_md
from kalshi.trade_log  import load_today, save_today

logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s %(levelname)-8s %(message)s",
    datefmt = "%H:%M:%S",
)
log = logging.getLogger(__name__)


def main() -> None:
    date_str = str(datetime.date.today())
    log.info(f"{'='*60}")
    log.info(f"  Daily trading run — {date_str}")
    log.info(f"{'='*60}")

    # ── Step 1: Build model ───────────────────────────────────────────────────
    if not KALSHI_KEY_ID or not KALSHI_KEY_FILE:
        log.error("KALSHI_KEY_ID and KALSHI_KEY_FILE must be set.")
        sys.exit(1)

    client  = KalshiClient(KALSHI_KEY_ID, KALSHI_KEY_FILE)
    balance = client.get_balance_usd()
    log.info(f"Balance: ${balance:.2f}")

    log.info("Fetching Kalshi markets…")
    markets = client.get_todays_game_markets()
    log.info(f"Found {len(markets)} game markets")

    log.info("Building ESPN probability model…")
    games = ProbabilityModel().get_todays_games()
    log.info(f"ESPN returned {len(games)} games")

    log.info("Fetching Polymarket prices…")
    pm       = PolymarketSource()
    pm_count = pm.load()

    log.info("Finding opportunities…")
    opps = find_opportunities(markets, games, polymarket=pm)
    log.info(f"Found {len(opps)} opportunities above threshold")

    # ── Step 2: Log model output ──────────────────────────────────────────────
    log.info("Writing model output…")
    write_model_output(
        date_str  = date_str,
        balance   = balance,
        markets_n = len(markets),
        games_n   = len(games),
        pm_count  = pm_count,
        opps      = opps,
    )

    # ── Step 3: Make trades ───────────────────────────────────────────────────
    trade_log = load_today(date_str)
    already   = trade_log["count"]

    if already >= MAX_TRADES_PER_DAY:
        log.info(f"Already placed {already} trades today — skipping.")
    else:
        selected = opps[:MAX_TRADES_PER_DAY - already]
        if not selected:
            log.info("No opportunities to trade today.")
        else:
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
                    "league":       opp["league"],
                    "order_id":     oid,
                    "status":       status,
                })
                trade_log["count"] += 1

            save_today(trade_log)
            log.info(
                f"Placed {trade_log['count'] - already} trades; "
                f"daily total {trade_log['count']}/{MAX_TRADES_PER_DAY}"
            )

    # ── Step 4: Update TRADES.md ──────────────────────────────────────────────
    log.info("Updating TRADES.md…")
    update_trades_md(date_str=date_str, trades=trade_log["trades"])

    # ── Step 5: Git commit and push ───────────────────────────────────────────
    log.info("Pushing to GitHub…")
    _git_push(date_str, trade_log["count"])

    log.info("Done.")


def _git_push(date_str: str, n_trades: int) -> None:
    def run(cmd):
        result = subprocess.run(
            cmd, cwd=TRADING_ROOT, capture_output=True, text=True
        )
        if result.stdout.strip():
            log.info(result.stdout.strip())
        if result.returncode != 0 and result.stderr.strip():
            log.warning(result.stderr.strip())
        return result.returncode

    # Stage markdown files and model outputs
    run(["git", "add", "TRADES.md",
         os.path.relpath(MODEL_OUTPUTS_DIR, TRADING_ROOT)])

    # Check if there's anything staged
    diff = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=TRADING_ROOT
    )
    if diff.returncode == 0:
        log.info("Nothing new to commit.")
        return

    msg = f"Daily update {date_str}: {n_trades} trade(s)"
    rc  = run(["git", "commit", "-m", msg])
    if rc != 0:
        log.error("git commit failed — skipping push.")
        return

    rc = run(["git", "push"])
    if rc != 0:
        log.error("git push failed.")
    else:
        log.info("Pushed to GitHub.")


if __name__ == "__main__":
    main()
