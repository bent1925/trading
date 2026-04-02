"""
Fetches market results and order fills for unresolved trades.
Enriches each trade record in kalshi_trades.json with:
  filled, market_result, pnl_usd, resolved=True
"""
import logging

from .trade_log import load_all, save_all

log = logging.getLogger(__name__)


def resolve_past_trades(client) -> set:
    """
    Iterates all trade log entries, fetches outcomes for unresolved trades.
    Returns the set of date strings that had at least one newly resolved trade.
    """
    all_logs       = load_all()
    updated_dates  = set()

    for date_str, entry in all_logs.items():
        for trade in entry["trades"]:
            if trade.get("resolved"):
                continue
            order_id = trade.get("order_id")
            ticker   = trade.get("ticker")
            if not order_id or not ticker:
                continue

            # Fetch market result — skip if still open
            try:
                mkt           = client.get(f"/trade-api/v2/markets/{ticker}")["market"]
                market_result = mkt.get("result")  # "yes" | "no" | None
                if not market_result:
                    continue
            except Exception as e:
                log.warning(f"Could not fetch market {ticker}: {e}")
                continue

            # Fetch actual fill count from the order
            try:
                order  = client.get(f"/trade-api/v2/portfolio/orders/{order_id}")["order"]
                filled = int(float(order.get("fill_count_fp", "0")))
            except Exception as e:
                log.warning(f"Could not fetch order {order_id}: {e}")
                filled = 0

            # P&L: win pays (100 - price_cents) per contract, loss costs price_cents
            side        = trade["side"]
            price_cents = trade["price_cents"]
            won = (side == "yes" and market_result == "yes") or \
                  (side == "no"  and market_result == "no")

            if filled == 0:
                pnl = 0.0
            elif won:
                pnl = filled * (100 - price_cents) / 100.0
            else:
                pnl = -filled * price_cents / 100.0

            trade["filled"]        = filled
            trade["market_result"] = market_result
            trade["pnl_usd"]       = round(pnl, 2)
            trade["resolved"]      = True
            updated_dates.add(date_str)

            log.info(
                f"Resolved {date_str} | {ticker} | {side.upper()} "
                f"{filled}×{price_cents}¢ → {market_result.upper()}  "
                f"pnl=${pnl:+.2f}"
            )

    if updated_dates:
        save_all(all_logs)
        log.info(f"Resolved trades for {sorted(updated_dates)}; kalshi_trades.json saved.")

    return updated_dates
