# Kalshi Sports Trading — Backtest Summary

**Period:** January 1 – March 25, 2026
**Starting balance:** $10,000
**Sports covered:** NBA, NHL (see [Data Quality](#data-quality) for why tennis was excluded)

---

## Overview

This project builds a trading bot for Kalshi sports prediction markets and tests four progressively more sophisticated strategies in backtests. The core idea: use ESPN's public API to build an independent probability model for each game, then trade when that model disagrees with Kalshi's implied probability by a meaningful margin.

**Files:**
| File | Description |
|------|-------------|
| `claude_code/kalshi_sports_bot.py` | Live trading bot |
| `claude_code/backtest.ipynb` | Strategy 1: Fade Kalshi |
| `claude_code/kalshi_trust_backtest.ipynb` | Strategy 2: Trust Kalshi |
| `claude_code/active_learning_backtest.ipynb` | Strategy 3: Active Learning |
| `claude_code/inverse_sizing_backtest.ipynb` | Strategy 4: Inverse Sizing |

---

## The Probability Model

For each Kalshi game market, an independent probability estimate is built from ESPN's public API (no API key required):

- **NBA / NHL:** Pull the historical scoreboard for the game date (`?dates=YYYYMMDD`). Extract team win-loss records as of that date. Compute `prob_home = (win_pct_home / (win_pct_home + win_pct_away)) + 0.04` (4pp home advantage). When ESPN embeds sportsbook money-line odds in the response, those are used instead (de-vigged by dividing each implied probability by the sum).
- **Tennis (ATP/WTA):** Log-rank model using player rankings. *Excluded from backtests — see [Data Quality](#data-quality).*

**Pre-game Kalshi price proxy:** Each settled Kalshi market exposes `previous_yes_ask_dollars` and `previous_yes_bid_dollars` — the bid/ask from the trading day before the game. These are used as the simulated entry price, making the backtest independent of any live market data.

**Edge definition:** `edge = model_prob − kalshi_mid`, where `kalshi_mid = (prev_ask + prev_bid) / 2`.

---

## Data Quality

### What's historical
| Data | Source | Historical? |
|------|--------|-------------|
| Kalshi pre-game prices | `previous_yes_ask/bid_dollars` | ✅ Genuine pre-game prices |
| Game outcomes | Kalshi `result` field | ✅ True historical outcomes |
| NBA/NHL team records | ESPN scoreboard `?dates=YYYYMMDD` | ✅ Records as of game date |
| ESPN money-line odds | Embedded in historical scoreboard | ✅ Closing lines from game day |

### What was excluded due to look-ahead bias
| Data | Problem |
|------|---------|
| ATP/WTA tennis | ESPN only exposes **current** rankings, not historical ones. Using March 2026 rankings to model January 2026 matches means the model "knows" how players' rankings evolved — look-ahead bias. Tennis is excluded from all backtests. |

### NHL parsing bug (fixed)
The original backtest silently produced zero NHL trades because `_record_win_pct` filtered for `type == "total"` — the NBA record type. NHL uses `type == "ytd"` and a `W-L-OT` format. After fixing the filter to accept both types and deleting stale empty cache files, NHL data was re-fetched and correctly parsed.

---

## Strategy Results

All four strategies trade NBA and NHL markets only, using `$10,000` starting balance and `$10/trade` (unless noted).

| Strategy | Trades | Win Rate | Total P&L | Return | Max DD | Sharpe |
|----------|--------|----------|-----------|--------|--------|--------|
| **1. Fade Kalshi** | 24 | 16.7% | −$94.59 | −0.95% | −0.95% | −2.26 |
| **2. Trust Kalshi** | 55 | 67.3% | −$25.77 | −0.26% | −0.43% | −1.43 |
| **3. Active Learning** | 57 | 71.9% | **+$17.12** | **+0.17%** | −0.27% | +0.75 |
| **4. Inverse Sizing** | 57 | 71.9% | **+$16.16** | **+0.16%** | **−0.21%** | **+0.85** |

---

## Strategy Details

### Strategy 1 — Fade Kalshi (`backtest.ipynb`)
The base strategy. Fade Kalshi's prices: when the model says a team is more likely to win than Kalshi implies by >10pp, buy YES; when the model says less likely, buy NO. Max 4 trades/day.

**Result:** Loses consistently. 16.7% win rate means contracts are cheap (near the edges the model identifies), but the market is right and the model is wrong. Sharpe −2.26.

---

### Strategy 2 — Trust Kalshi (`kalshi_trust_backtest.ipynb`)
Inverts Strategy 1: follow Kalshi's signal instead of fading it. When Kalshi prices YES higher than the model by ≥5pp, buy YES. Min edge 5pp, max 20 trades/day.

**Signal:** `edge = kalshi_mid − model_prob` (sign flipped).

**Result:** 67.3% win rate — dramatically better than Strategy 1. But win payouts on heavily-favored contracts are small, so despite winning more often the P&L is still negative (−$25.77). The market's pricing of favorites is efficient; edges are explained by the market knowing things the simple model doesn't.

---

### Strategy 3 — Active Learning (`active_learning_backtest.ipynb`)
Combines both strategies adaptively:

1. **Exploration (trades 1–30):** One strategy is chosen at random and used for all 30 trades. Both virtual P&L streams are tracked simultaneously (the counterfactual is computable in backtest).
2. **Exploitation (every 10 trades after that):** Switch to whichever strategy has the higher cumulative P&L.

Each day selects the **10 markets with the largest absolute edge** (`|model_prob − kalshi_mid|`) — the highest-information trades.

**Result:** +$17.12, Sharpe +0.75. First profitable strategy. The random seed (42) picked Trust Kalshi at the start; after 30 trades Trust was ahead (+$13.95 vs Fade's −$19.33), and the strategy locked in Trust Kalshi for the remainder, never switching.

---

### Strategy 4 — Inverse Sizing (`inverse_sizing_backtest.ipynb`)
Identical to Strategy 3, but bet size is an **inverse function of edge**:

$$\text{bet} = \text{clip}\!\left(\frac{\$20 \times 5\text{pp}}{|\text{edge}|_\text{pp}},\ \$1,\ \$20\right)$$

| Edge | Bet |
|------|-----|
| ≤ 5 pp | $20 (max) |
| 10 pp | $10 |
| 20 pp | $5 |
| 50 pp | $2 |
| ≥ 100 pp | $1 (min) |

The intuition: a small gap between model and Kalshi suggests a subtle, reliable inefficiency — size up. A large gap is more likely to reflect a model error — size down.

**Result:** +$16.16, Sharpe **+0.85** (best). Similar P&L to Strategy 3 but with only $392 wagered vs $545 — better capital efficiency. Max drawdown also shrinks to −0.21%.

---

## Key Takeaways

1. **Fade the model, not the market.** Kalshi crowd pricing consistently outperforms the simple ESPN win-rate model. Fading Kalshi (Strategy 1) loses badly; following Kalshi (Strategies 2–4) wins.

2. **Bet more on smaller edges.** When the model and market broadly agree and a small discrepancy exists, that discrepancy tends to be real. Large model-vs-market gaps usually mean the model is wrong, not the market.

3. **Active selection matters.** Taking the top-10 trades by edge magnitude per day (instead of filtering by a fixed threshold) concentrates capital on the most informative markets.

4. **Removing look-ahead bias changed the picture.** Before fixing the tennis exclusion, all four strategies lost money. With clean NBA/NHL-only data, Strategies 3 and 4 become profitable.

5. **Small sample caveat.** 57 trades over ~85 days is a limited sample. The +$17 P&L and 71.9% win rate are encouraging but not yet statistically conclusive. A longer backtest period or live paper-trading would be the next step.

---

## Reproducing the Results

```bash
pip install requests cryptography pandas matplotlib jupyter nbconvert

export KALSHI_KEY_ID="your-api-key-id"
export KALSHI_KEY_FILE="/path/to/your/private_key.pem"

cd claude_code

# Run all four backtests (uses cached data on subsequent runs)
jupyter nbconvert --to notebook --execute --inplace backtest.ipynb
jupyter nbconvert --to notebook --execute --inplace kalshi_trust_backtest.ipynb
jupyter nbconvert --to notebook --execute --inplace active_learning_backtest.ipynb
jupyter nbconvert --to notebook --execute --inplace inverse_sizing_backtest.ipynb
```

Market data and ESPN game data are cached to `backtest_cache/` after the first run (excluded from git). Subsequent runs complete in seconds.
