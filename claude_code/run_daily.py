#!/usr/bin/env python3
"""
Standalone daily runner — equivalent to the Airflow DAG without requiring Airflow.
Called by run_daily.sh, which is scheduled via launchd at 06:00 PT.

Steps
-----
0. resolve_previous  — fetch Kalshi results for prior days' trades; update TRADES.md
1. build_model       — fetch Kalshi markets, ESPN games, Polymarket prices
2. log_model_output  — write model_outputs/YYYY-MM-DD.md
3. make_trades       — execute orders on Kalshi, persist to kalshi_trades.json
4. update_trade_log  — insert/replace today's section in TRADES.md
5. git_push          — commit changed files and push to GitHub
"""

import datetime
import logging
import os
import re
import subprocess
import sys

# Make the kalshi package importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "dags"))

from kalshi.client     import KalshiClient
from kalshi.config     import (KALSHI_KEY_ID, KALSHI_KEY_FILE,
                                MAX_TRADES_PER_RUN, MIN_BALANCE_TO_TRADE,
                                TRADING_PAUSED_UNTIL, INJURY_DATA_ENABLED,
                                TRADING_ROOT, TRADES_MD, MODEL_OUTPUTS_DIR,
                                TRADE_LOG_FILE, OPPONENT_STRENGTH_FILE)
from kalshi.model      import ProbabilityModel, find_opportunities
from kalshi.polymarket import PolymarketSource
from kalshi.reporting  import write_model_output, update_trades_md
from kalshi.resolve    import resolve_past_trades
from kalshi.trade_log  import load_today, load_all, save_today
from kalshi.opponent_strength import OpponentStrengthDB, bootstrap_daily
from kalshi.injury_data import ESPNInjurySource

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

    # ── Step 0: Resolve previous trades ──────────────────────────────────────
    if not KALSHI_KEY_ID or not KALSHI_KEY_FILE:
        log.error("KALSHI_KEY_ID and KALSHI_KEY_FILE must be set.")
        sys.exit(1)

    client = KalshiClient(KALSHI_KEY_ID, KALSHI_KEY_FILE)

    log.info("Resolving previous trades…")
    updated_dates = resolve_past_trades(client)
    if updated_dates:
        all_logs = load_all()
        for ds in sorted(updated_dates):
            if ds != date_str:
                update_trades_md(date_str=ds, trades=all_logs[ds]["trades"])
        log.info(f"Rebuilt TRADES.md for {sorted(updated_dates)}")

    # ── Step 1: Build model ───────────────────────────────────────────────────
    balance = client.get_balance_usd()
    log.info(f"Balance: ${balance:.2f}")

    log.info("Fetching Kalshi markets…")
    markets = client.get_todays_game_markets()
    log.info(f"Found {len(markets)} game markets")

    # Refresh opponent strength (skips if already done today)
    log.info("Refreshing opponent strength…")
    opp_db = OpponentStrengthDB(OPPONENT_STRENGTH_FILE)
    bootstrap_daily(opp_db)

    # Set up injury source (ESPN public API, no key needed)
    injury_source = ESPNInjurySource() if INJURY_DATA_ENABLED else None
    if injury_source:
        log.info("Injury data enabled (ESPN public API)")

    log.info("Building ESPN probability model…")
    games = ProbabilityModel(
        opp_strength_db=opp_db,
        injury_source=injury_source,
    ).get_todays_games()
    log.info(f"ESPN returned {len(games)} games")

    log.info("Fetching Polymarket prices per game…")
    pm = PolymarketSource()

    # Load today's already-traded event tickers to skip in this run
    trade_log_pre = load_today(date_str)
    already_traded_events = {
        re.sub(r"-(YES|NO)$", "", t.get("event_ticker", t.get("ticker", "")),
               flags=re.IGNORECASE)
        for t in trade_log_pre["trades"]
    }
    if already_traded_events:
        log.info(f"Skipping {len(already_traded_events)} already-traded event(s) this run")

    log.info("Finding opportunities…")
    opps = find_opportunities(markets, games, polymarket=pm,
                              already_traded_events=already_traded_events,
                              balance=balance)
    log.info(f"Found {len(opps)} opportunities above threshold")

    # ── Step 2: Log model output ──────────────────────────────────────────────
    log.info("Writing model output…")
    write_model_output(
        date_str  = date_str,
        balance   = balance,
        markets_n = len(markets),
        games_n   = len(games),
        opps      = opps,
    )

    # ── Step 3: Make trades ───────────────────────────────────────────────────
    trade_log = trade_log_pre
    already   = trade_log["count"]

    if TRADING_PAUSED_UNTIL and date_str < TRADING_PAUSED_UNTIL:
        log.info(f"Trading paused until {TRADING_PAUSED_UNTIL} — skipping order placement.")
        update_trades_md(date_str=date_str, trades=trade_log["trades"])
        _git_push(date_str, trade_log["count"])
        log.info("Done.")
        return

    selected = opps[:MAX_TRADES_PER_RUN]
    if not selected:
        log.info("No opportunities found this run.")
    elif balance < MIN_BALANCE_TO_TRADE:
        log.info(
            f"Balance ${balance:.2f} is below minimum ${MIN_BALANCE_TO_TRADE:.2f} — skipping trades."
        )
    else:
        available = balance
        for opp in selected:
            if opp["cost_usd"] > available:
                log.warning(
                    f"Insufficient balance (${available:.2f}) for "
                    f"{opp['ticker']} (${opp['cost_usd']:.2f}) — skipping."
                )
                continue
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
                "event_ticker": opp.get("event_ticker", ""),
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
                "strategy":     opp["strategy"],
                "order_id":     oid,
                "status":       status,
            })
            trade_log["count"] += 1
            available -= opp["cost_usd"]

        save_today(trade_log)
        log.info(
            f"Placed {trade_log['count'] - already} trades this run; "
            f"daily total {trade_log['count']}"
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
