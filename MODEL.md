# Probability Model

The bot estimates each team's win probability from multiple independent sources, then compares that estimate against Kalshi's implied probability (the mid-price) to find edges worth trading.

---

## Overview

For each Kalshi sports game market, three independent signals are gathered and blended into a single model probability. The weight each signal gets depends on what is available:

| Scenario | ESPN sportsbook | Polymarket | Weight split |
|----------|:-:|:-:|---|
| Both available | ✅ | ✅ | 50% ESPN sportsbook + 50% Polymarket |
| Sportsbook only | ✅ | ❌ | 100% ESPN sportsbook |
| Polymarket only | ❌ | ✅ | 75% Polymarket + 25% ESPN win-rate |
| Neither | ❌ | ❌ | 100% ESPN win-rate (+ recent form if available) |

A trade is placed when `|model_prob − kalshi_mid| > 10 pp`.

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

Once a model probability is assembled, it is compared against Kalshi's mid-price:

$$\text{edge} = (\text{model\_prob} - \text{kalshi\_mid}) \times 100\ \text{pp}$$

where `kalshi_mid = (yes_ask + yes_bid) / 2`.

| Edge | Action |
|------|--------|
| `edge > +10 pp` | BUY YES — model says contract is underpriced |
| `edge < −10 pp` | BUY NO — model says contract is overpriced |
| `|edge| ≤ 10 pp` | No trade |

---

## Source Priority and Labeling

The `model_source` field logged with each trade shows exactly which signals were blended:

| Label | Meaning |
|-------|---------|
| `espn_odds(50%)+polymarket(50%)` | ESPN sportsbook + Polymarket |
| `polymarket(75%)+win_pct(25%)` | Polymarket + season win-rate (no ESPN lines) |
| `polymarket(75%)+win_pct+form(25%)` | Polymarket + blended season/recent win-rate |
| `espn:espn_odds` | ESPN sportsbook only (no Polymarket match) |
| `espn:win_pct` | Season win-rate only |
| `espn:win_pct+form` | Season win-rate blended with last-10 form |
| `ranking(#N vs #M)` | Tennis log-rank model |

---

## Data Quality and Limitations

| Issue | Detail |
|-------|--------|
| Tennis look-ahead bias | ESPN rankings are current-only; backtests exclude ATP/WTA |
| Early-season records | Teams with <5 games are skipped (win-rate is too noisy) |
| Polymarket matching | Fuzzy word-overlap; low-quality matches (score < 2) are discarded |
| Polymarket framing | Yes/No outcome framing is inferred heuristically; edge cases may misidentify the YES team |
| Kalshi mid as fair value | The mid-price is used as the market's probability estimate, ignoring spread |

---

## Relationship to Backtests

Backtests (`BACKTEST_SUMMARY.md`) use only the ESPN win-rate model with NBA and NHL data. Polymarket and recent-form signals are **live-only** additions and have not been backtested. The backtest finding that "trusting the market beats trusting the ESPN model" motivates the heavy weighting toward Polymarket in the ensemble (75% when ESPN sportsbook lines are unavailable).
