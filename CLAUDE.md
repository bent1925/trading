# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An automated sports betting bot that trades game-winner markets on [Kalshi](https://kalshi.com). It compares an independent probability model (sourced from Polymarket and ESPN) against Kalshi's mid-price, then places limit buy orders when the discrepancy exceeds a threshold. The strategy is cross-market arbitrage: fade Kalshi toward Polymarket prices.

## Setup

```bash
pip install requests cryptography
```

Credentials go in a `.env` file at the repo root (loaded by `run_daily.sh`):
```
KALSHI_KEY_ID=your-api-key-id
KALSHI_KEY_FILE=/path/to/private_key.pem
```

Or export them directly:
```bash
export KALSHI_KEY_ID="your-api-key-id"
export KALSHI_KEY_FILE="/path/to/your/private_key.pem"
```

## Running the Bot

```bash
# Dry run — preview opportunities without placing orders
python3 claude_code/kalshi_sports_bot.py --dry-run

# Execute trades (standalone runner, no Airflow needed)
python3 claude_code/run_daily.py

# Shell wrapper (used by launchd scheduler on macOS)
bash claude_code/run_daily.sh
```

The bot is also expressed as an Airflow DAG at `claude_code/dags/trading_dag.py` (daily at 06:00 PT), but `run_daily.py` is the primary standalone runner.

## Architecture

### Entry Points

| File | Purpose |
|------|---------|
| `claude_code/kalshi_sports_bot.py` | Original monolithic bot; supports `--dry-run` |
| `claude_code/run_daily.py` | Modular standalone runner; used in production |
| `claude_code/dags/trading_dag.py` | Airflow DAG equivalent of `run_daily.py` |

### Core Package: `claude_code/dags/kalshi/`

| Module | Role |
|--------|------|
| `config.py` | All tuneable parameters: edge threshold, Kelly fraction, max bet, trade horizon, file paths, `TRADING_PAUSED_UNTIL` |
| `client.py` | `KalshiClient` — RSA-PSS signed HTTP calls to Kalshi Trade API v2; fetches markets, portfolio balance, places/cancels orders |
| `model.py` | `ProbabilityModel` (ESPN data → win probabilities) + `find_opportunities()` (signal blending, edge calc, Kelly sizing) |
| `polymarket.py` | `PolymarketSource` — fetches Polymarket Gamma API; fuzzy-matches markets to games |
| `resolve.py` | Fetches Kalshi settlement results for prior-day trades; updates P&L in the trade log |
| `trade_log.py` | Reads/writes `kalshi_trades.json` (one key per date) |
| `reporting.py` | Writes `model_outputs/YYYY-MM-DD.md` and `TRADES.md` |
| `utils.py` | `parse_ticker_date`, `words`, `overlap` (token matching helpers) |

### Data Flow (one run)

```
KalshiClient.get_todays_game_markets()   →  list of Kalshi market dicts
ProbabilityModel.get_todays_games()      →  list of ESPN game dicts
PolymarketSource.get_prob(team, other)   →  per-game probability lookups

find_opportunities(markets, games, pm)   →  ranked list of trade opportunities
  └─ match_market_to_game()             →  links Kalshi market ↔ ESPN game
  └─ signal blending (Polymarket > ESPN odds > ESPN win-rate)
  └─ Kelly sizing  →  contracts, cost_usd

KalshiClient.place_order()              →  order placed
save_today() / update_trades_md()       →  kalshi_trades.json + TRADES.md updated
git commit + push                        →  TRADES.md + model_outputs/ pushed to GitHub
```

### Signal Priority (per game)

1. Polymarket + ESPN sportsbook odds (50/50 blend) — both liquid market prices
2. Polymarket only — when no ESPN odds embedded
3. ESPN sportsbook odds only — when no Polymarket match
4. ESPN win-rate/form — weakest fallback; tennis excluded from backtests

### Key Parameters (`config.py`)

- `MIN_EDGE_PP` — minimum |model − kalshi_mid| in percentage points to consider a trade (currently 2 pp)
- `TRADE_HORIZON_HOURS` — only trade games starting within this many hours (3.5h; consecutive runs overlap 30 min)
- `KELLY_FRACTION` — fraction of full Kelly to bet (0.25 = quarter-Kelly)
- `MAX_BET` — hard cap per trade in dollars ($20)
- `MAX_TRADES_PER_RUN` — trades per execution (5)
- `TRADING_PAUSED_UNTIL` — set to a future date string to pause order placement without stopping model logging

### UTC Date Handling

US evening games start after UTC midnight but are dated the previous calendar day on both Kalshi and ESPN. Both `client.get_todays_game_markets()` and `model.get_todays_games()` fetch **yesterday + today (UTC)** and deduplicate by `(home, away, start_time)`.

### Persistent Files (gitignored)

- `kalshi_trades.json` — trade log, keyed by date string
- `.env` — credentials
- `logs/run_daily.log` — shell wrapper log
- `*.pem`, `*.key` — private key files

### Committed Output Files

- `TRADES.md` — human-readable trade log rebuilt daily
- `model_outputs/YYYY-MM-DD.md` — daily model analysis snapshot
- `BACKTEST_SUMMARY.md`, `MODEL.md`, `MODEL_BIASES.md` — strategy documentation
