# Kalshi Sports Trading Bot

Automatically trades sports game markets on [Kalshi](https://kalshi.com) by comparing an independent probability model against current contract prices.

## How it works

1. **Finds today's games** — scans Kalshi for NBA, MLB, NHL, WTA, and ATP markets whose game is scheduled for today (date is parsed directly from the market ticker).

2. **Builds a probability model** — pulls data from ESPN's public API, independently of Kalshi:
   - NBA / NHL / MLB: season win-rate ratio with home-court/home-ice advantage
   - When ESPN has consensus sportsbook money-lines, those are used instead (de-vigged)
   - Tennis (ATP / WTA): log-rank model using ESPN's live player rankings

3. **Trades on edge** — if the model's probability differs from the Kalshi mid-price by more than 10 percentage points, it places a limit buy order:
   - Model > Kalshi mid by >10pp → buy **YES** (contract is undervalued)
   - Model < Kalshi mid by >10pp → buy **NO** (contract is overvalued)

4. **Position sizing** — each trade is allocated $10, buying as many contracts as that allows at the current ask price. Maximum 4 trades per day.

## Setup

```bash
pip install requests cryptography
```

Set environment variables for your Kalshi credentials:

```bash
export KALSHI_KEY_ID="your-api-key-id"
export KALSHI_KEY_FILE="/path/to/your/private_key.pem"
```

## Usage

```bash
# Preview opportunities without placing orders
python3 claude_code/kalshi_sports_bot.py --dry-run

# Execute trades
python3 claude_code/kalshi_sports_bot.py
```

## Output

```
====================================================================
  KALSHI SPORTS TRADING BOT
====================================================================
  Date             : 2026-03-26
  Account balance  : $70.78
  Trades today     : 0/4
  Kalshi markets   : 60
  ESPN games       : 12
  Edges >10pp found: 3
  Trades to make   : 3

────────────────────────────────────────────────────────────────────
  Trade 1/3
────────────────────────────────────────────────────────────────────
  Market  : Sacramento at Orlando Winner?
  Game    : Sacramento Kings @ Orlando Magic  (NBA)
  Source  : model built from win_pct

  Kalshi yes-bid / yes-ask : 9¢ / 10¢  (mid = 9.5¢)
  Model probability (yes)  : 29.0%
  Edge                     : +19.5 pp  →  BUY YES

  Price per contract : 10¢  ($0.10)
  Budget             : $10.00
  Contracts          : 100 × 10¢ = $10.00

  Order status : executed   filled = 0 contracts
  Order ID     : 2e36cbab-...
```

Executed trades are logged to `kalshi_trades.json` with timestamps, tickers, prices, contract counts, model probabilities, and order IDs. The daily trade counter resets at midnight.
