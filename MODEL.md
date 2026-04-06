# Probability Model

The bot compares Polymarket's implied probability against Kalshi's mid-price to find cross-market pricing discrepancies. When the two markets disagree by more than 10pp, it bets on Kalshi to converge toward Polymarket.

---

## Overview

For each Kalshi sports game market, Polymarket is the primary signal. A trade is only placed when a Polymarket match is found. ESPN sportsbook money-lines are blended in when available (both are liquid market prices); ESPN win-rate data is ignored as it is too noisy relative to a live market price.

| Scenario | ESPN sportsbook | Polymarket | Model |
|----------|:-:|:-:|---|
| Both available | ✅ | ✅ | 50% ESPN sportsbook + 50% Polymarket |
| Polymarket only | ❌ | ✅ | 100% Polymarket |
| No Polymarket | — | ❌ | Skip — no trade |

A trade is placed when all of the following hold:
- A Polymarket match is found for the game
- The game starts within **3 hours** of the run (uses ESPN's scheduled start time)
- `|model_prob − kalshi_mid| > 10 pp`

**Edge direction (fade Kalshi):**

| Edge | Action |
|------|--------|
| `model_prob > kalshi_mid + 10pp` | BUY YES — Kalshi underprices relative to Polymarket |
| `model_prob < kalshi_mid − 10pp` | BUY NO — Kalshi overprices relative to Polymarket |

**Sizing (proportional to spread):**

| Edge | Budget |
|------|--------|
| 10pp | $10 |
| 15pp | $15 |
| 20pp+ | $20 (max) |

---

## Signal 1 — ESPN Sportsbook Consensus Lines

**Source:** ESPN's public scoreboard API
**Endpoint:** `http://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard?dates=YYYYMMDD`
**No API key required.**

ESPN embeds consensus sportsbook money-line odds directly in game events under `competitions[0].odds[].homeTeamOdds.moneyLine` and `awayTeamOdds.moneyLine`. These represent the closing line aggregated across multiple books (typically includes DraftKings, FanDuel, BetMGM, etc.).

**Conversion from American money-lines to implied probability:**

$$p = \begin{cases} \dfrac{100}{ML + 100} & \text{if } ML > 0 \\ \dfrac{|ML|}{|ML| + 100} & \text{if } ML < 0 \end{cases}$$

**De-vigging (removing the house edge):**

$$p_{\text{home}} = \frac{p_{\text{home,raw}}}{p_{\text{home,raw}} + p_{\text{away,raw}}}$$

Dividing by the sum of both raw implied probabilities strips out the vig so probabilities sum to 1.

**When available:** Most NBA and NHL games include these lines. MLB coverage is variable. Tennis rarely has embedded lines.

---

## Signal 2 — ESPN Season Win-Rate + Recent Form

**Source:** ESPN's public scoreboard API (same endpoint as above)
**No API key required.**

When sportsbook lines are not embedded, team records are extracted from `competitions[0].competitors[].records[]`.

### Season win-rate

Each competitor's season record is read from the entry with `type == "total"` (NBA) or `type == "ytd"` (NHL). The summary string follows the format `W-L` or `W-L-OT` (e.g. `"38-34"` or `"28-40-8"`).

Teams with fewer than 5 games played are excluded — early-season records are too noisy to be informative.

$$p_{\text{home,season}} = \frac{W_{\text{home}}}{W_{\text{home}} + L_{\text{home}}}$$

### Recent form (last 10 games)

When ESPN includes a record entry with `type == "lastTen"` or `type == "last10"`, the last-10-game win rate is extracted and blended with the season record:

$$p_{\text{home,blended}} = 0.6 \times p_{\text{home,season}} + 0.4 \times p_{\text{home,lastTen}}$$

This gives more weight to recent performance while keeping the season-long baseline.

### Converting to a game probability

$$p_{\text{home}} = \frac{p_{\text{home,blended}}}{p_{\text{home,blended}} + p_{\text{away,blended}}}$$

A **home advantage** of +4 pp is then added for NBA and NHL (not applied to tennis):

$$p_{\text{home,final}} = \text{clip}(p_{\text{home}} + 0.04,\ 0.05,\ 0.95)$$

---

## Signal 3 — Polymarket Implied Probability

**Source:** Polymarket Gamma API
**Endpoint:** `https://gamma-api.polymarket.com/markets?active=true&closed=false`
**No API key required.**

Polymarket is a decentralized prediction market. Its prices reflect the collective wisdom of real-money bettors and are generally well-calibrated for popular sporting events.

All active, non-closed markets are fetched at startup (paginated, up to ~2,000 markets). For each game, both team names are matched against market questions using word-overlap scoring. A match is accepted only if at least one word from each team name appears in the question.

### Determining outcome framing

Polymarket questions come in two formats:

1. **Team-labeled outcomes** — `outcomes = ["Memphis Grizzlies", "Houston Rockets"]`. The price at index 0 is P(Memphis wins). If the YES team matches `outcomes[0]`, return `prices[0]`; if it matches `outcomes[1]`, return `1 − prices[0]`.

2. **Yes/No outcomes** — `outcomes = ["Yes", "No"]`. The question is inspected to see which team is the subject: whichever team name appears first in the question is assumed to be the team whose win corresponds to "Yes". If the YES team appears first, return `prices[0]`; otherwise return `1 − prices[0]`.

---

## Signal 4 — Tennis Ranking Model (ATP / WTA)

**Source:** ESPN rankings API
**Endpoint:** `http://site.api.espn.com/apis/site/v2/sports/tennis/{league}/rankings`
**No API key required.**

For ATP and WTA matches, a log-rank model is used. Player world rankings are fetched and converted to win probabilities:

$$p_1 = \frac{\ln(r_2 + 1)}{\ln(r_1 + 1) + \ln(r_2 + 1)}$$

where $r_1$ and $r_2$ are the world rankings of player 1 and player 2 (lower rank = better). Unranked players default to rank 200.

**Caveat:** ESPN's rankings endpoint returns **current** rankings, not historical ones. This means the tennis model cannot be backtested without look-ahead bias — March rankings are used even when evaluating January matches. For this reason, tennis is **excluded from all backtests** but remains active in the live bot. Live trades on ATP/WTA should be interpreted with this limitation in mind.

---

## Edge Calculation

$$\text{edge} = (\text{model\_prob} - \text{kalshi\_mid}) \times 100\ \text{pp}$$

where `kalshi_mid = (yes_ask + yes_bid) / 2`.

A positive edge means Polymarket prices YES higher than Kalshi — the bot buys YES on Kalshi expecting convergence. A negative edge means Polymarket prices YES lower — the bot buys NO.

---

## Source Labels

The `model_source` field logged with each trade shows which signals were blended:

| Label | Meaning |
|-------|---------|
| `espn_odds(50%)+polymarket(50%)` | ESPN sportsbook + Polymarket (both market prices) |
| `polymarket` | Polymarket only (no ESPN sportsbook lines available) |
| `ranking(#N vs #M)` | Tennis log-rank model (Polymarket match also required) |

---

## Data Quality and Limitations

| Issue | Detail |
|-------|--------|
| No Polymarket match = no trade | Markets without a Polymarket counterpart are skipped entirely |
| Polymarket matching | Fuzzy word-overlap; low-quality matches (score < 2) are discarded |
| Polymarket framing | Yes/No outcome framing is inferred heuristically; edge cases may misidentify the YES team |
| Polymarket liquidity | Prices are used regardless of market volume — thin markets may have stale prices |
| Tennis look-ahead bias | ESPN rankings are current-only; backtests exclude ATP/WTA |
| Kalshi mid as fair value | The mid-price is used as the market's probability estimate, ignoring spread |

---

## Relationship to Backtests

Backtests (`BACKTEST_SUMMARY.md`) used the ESPN win-rate model with NBA and NHL data. The current live strategy (Polymarket as primary signal, fade Kalshi) has not been formally backtested — Polymarket historical price data is not readily available. The theoretical basis is cross-market arbitrage: two liquid markets pricing the same binary event should converge at settlement.
