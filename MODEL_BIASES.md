# Model Biases & Known Limitations

Notes from code review, April 2026. See `MODEL.md` for full model description.

---

## How the model works (summary)

*Last updated: Apr 7, 2026. See `MODEL.md` for full detail.*

The bot runs at 06:00 PT and places orders immediately. For each Kalshi sports market closing today it:

1. Fetches Polymarket implied probability for the game via fuzzy team-name matching — **skips the market if no match is found**
2. Fetches ESPN sportsbook money-lines (de-vigged); if available, blends 50/50 with Polymarket. If not, uses Polymarket alone. ESPN win-rate is ignored.
3. Tennis uses a log-rank model alongside Polymarket (Polymarket match still required)
4. Computes `edge_pp = (model_prob − kalshi_mid) × 100`; trades when `|edge_pp| > 10pp`
5. Bets *against* Kalshi (fade Kalshi / cross-market arb): when Polymarket prices a side higher than Kalshi, buys that side on Kalshi expecting convergence
6. Sizes proportionally to the spread: $10 at 10pp, $20 at 20pp+; up to 10 trades/day

---

## Known biases

### 1. Stale price snapshot
**Severity: Very Low** *(addressed Apr 7)*

The bot runs every 3 hours and only trades games starting within the next 3 hours. The maximum staleness at time of trade is 3 hours, and prices are re-fetched fresh on every run.

Residual risk: late-breaking news (injury announced 30 minutes before tip-off, after the last run) won't be captured. This is a small and unavoidable gap.

---

### 2. Correlated signal blending
**Severity: Low** *(partially addressed Apr 7)*

When ESPN sportsbook odds are available, the blend is 50% ESPN + 50% Polymarket. Both are market prices reflecting similar public information — they are correlated, not independent signals. The blend is now treated as a single "market consensus" estimate rather than two independent views, which is the right framing. The residual issue is that the 50/50 weight is arbitrary and not calibrated.

When ESPN has only win-rate data (no sportsbook lines), the ESPN signal is now dropped entirely and Polymarket is used alone. This removes the noisiest part of the old blend.

**To fix:** Weight the ESPN/Polymarket blend by relative liquidity or recency.

---

### 3. Polymarket fuzzy matching ambiguity
**Severity: Low** *(partially addressed Apr 7)*

The minimum word length for matching was raised from 3 to 4 characters, removing short ambiguous tokens ("san", "los", "new", "bay") from scoring. "San Antonio Spurs" now matches on "antonio" and "spurs" rather than "san", eliminating the cross-sport false match (San Francisco Giants) that was observed in testing.

Residual risk: same-city teams sharing a 4+ char token (e.g. "angeles" for Lakers and Clippers) can still collide. In practice the blocklist and score threshold prevent most cases.

**To fix:** Validate that the matched question contains the team's mascot or city name as a substring before accepting the match.

---

### 4. Fixed home advantage
**Severity: Low–Medium**

`HOME_EDGE = 0.04` is applied uniformly to NBA, NHL, and MLB regardless of venue, team, or sport. Actual home advantage varies by sport (basketball > hockey > baseball) and has declined in recent years. Additionally, the bump is applied only to the win-rate fallback path — the ESPN sportsbook path (which already embeds home advantage in the lines) does not get double-counted, which is correct, but the asymmetry is not documented anywhere in the code.

**To fix:** Use sport-specific home edge constants. Consider removing it entirely given that Polymarket (a market price) dominates the blend at 75%.

---

### 5. Win rate ignores strength of schedule
**Severity: N/A** *(removed Apr 7)*

ESPN win-rate and recent form are no longer used. When ESPN has no sportsbook odds, the model falls back to Polymarket alone rather than ESPN win-rate. This signal has been removed from the live bot.

---

### 6. Polymarket liquidity and settlement conditions
**Severity: Low–Medium**

Polymarket prices are used at face value regardless of market liquidity or trading volume. A thinly-traded or stale Polymarket market gets the same weight as a liquid one. Additionally, Polymarket and Kalshi may have different settlement conditions for the same game (e.g. overtime rules, series vs. single game), meaning their prices aren't directly comparable.

**To fix:** Check the `volume` or `liquidityNum` field from the Gamma API and skip or downweight low-liquidity markets.

---

### 7. Tennis look-ahead bias (backtests only)
**Severity: High for backtests, N/A for live trading**

ESPN only exposes *current* rankings, not historical ones. Replaying past dates using the rankings API returns today's rankings, not the rankings as of that date — making all tennis backtest results meaningless. This is why ATP/WTA is excluded from all backtests.

In live trading this is not a bias per se, but today's rankings reflect results from matches that have already happened this week/month, which is appropriate. The practical risk is that unranked players default to rank #200, which is an arbitrary floor that can produce bad signals for qualification-round matches where many players are unranked.

**To fix (live):** Widen the default rank (e.g. #300) or skip markets where both players default to the floor rank.

---

### 8. De-vig method assumption
**Severity: Low**

ESPN sportsbook lines are de-vigged by normalizing: `hi / (hi + ai)`. This is multiplicative de-vig, which assumes the bookmaker's margin is distributed proportionally across outcomes. Additive de-vig (subtracting equal margin from each side) gives slightly different probabilities, particularly for heavy favorites. The true margin distribution is unknown.

**To fix:** Low priority — the difference between methods is small for near-even games, which are the ones most likely to produce a 10pp edge against Kalshi.

---

## Summary table

| # | Bias | Severity | Status |
|---|------|----------|--------|
| 1 | Stale price snapshot | Very Low | Addressed Apr 7 |
| 2 | Correlated signal blending | Low | Partially addressed Apr 7 |
| 3 | Polymarket fuzzy match ambiguity | Low | Partially addressed Apr 7 |
| 4 | Fixed home advantage | Low–Medium | Open |
| 5 | Win rate ignores strength of schedule | N/A | Removed Apr 7 |
| 6 | Polymarket liquidity / settlement mismatch | Low–Medium | Open |
| 7 | Tennis look-ahead bias (backtests) | High / N/A live | Excluded from backtests |
| 8 | De-vig method assumption | Low | Open |
