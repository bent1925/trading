#!/usr/bin/env python3
"""
Cancel all resting orders, then run the bot fresh.
Usage:
    python3 claude_code/cancel_and_retrade.py           # cancel + live trade
    python3 claude_code/cancel_and_retrade.py --dry-run # cancel + dry-run preview
"""
import sys
import os

# Make sure we can import the bot from any working directory
sys.path.insert(0, os.path.dirname(__file__))

from kalshi_sports_bot import KalshiClient, run_bot, KALSHI_KEY_ID, KALSHI_KEY_FILE

def cancel_open_orders(client: KalshiClient) -> int:
    orders = client.get_open_orders()
    if not orders:
        print("No resting orders found.")
        return 0

    cancelled = 0
    for order in orders:
        oid    = order.get("order_id", "")
        ticker = order.get("ticker", "")
        side   = order.get("side", "")
        count  = order.get("remaining_count", order.get("count", "?"))
        price  = order.get("yes_price") or order.get("no_price")
        print(f"  Cancelling {oid[:12]}…  {ticker}  {side} ×{count} @ {price}¢  … ", end="", flush=True)
        try:
            client.cancel_order(oid)
            print("cancelled")
            cancelled += 1
        except Exception as e:
            print(f"FAILED: {e}")

    return cancelled


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv

    if not KALSHI_KEY_ID or not KALSHI_KEY_FILE:
        print("Error: set KALSHI_KEY_ID and KALSHI_KEY_FILE environment variables.")
        sys.exit(1)

    client = KalshiClient(KALSHI_KEY_ID, KALSHI_KEY_FILE)

    print("=" * 68)
    print("  STEP 1 — Cancel open orders")
    print("=" * 68)
    n = cancel_open_orders(client)
    print(f"\n  Cancelled {n} order(s).\n")

    print("=" * 68)
    print("  STEP 2 — Place new trades")
    print("=" * 68)
    run_bot(dry_run=dry_run)
