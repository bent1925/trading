# Probability Model

The bot compares Polymarket's implied probability against Kalshi's mid-price to find cross-market pricing discrepancies. When the two markets disagree by more than 2pp, it bets on Kalshi to converge toward Polymarket.

---

## Overview

For each Kalshi sports game market, Polymarket is the primary signal. A trade is placed when a Polymarket match is found; when no match exists, the bot falls back to ESPN sportsbook odds, then win-rate/form. ESPN win-rate data is the weakest signal and is only used as a last resort.

| Scenario | ESPN sportsbook | Polymarket | Model |
|----------|:-:|:-:|---|
| Both available | ✅ | ✅ | 50% ESPN sportsbook + 50% Polymarket |
| Polymarket only | ❌ | ✅ | 100% Polymarket |
| No Polymarket match | ✅ | ❌ | 100% ESPN sportsbook (fallback) |
| No Polymarket, no ESPN odds | — | ❌ | ESPN win-rate/form (weakest signal) |

Polymarket is the preferred signal. When no Polymarket market can be matched, the bot falls back to ESPN rather than skipping the game entirely. This ensures liquid, well-covered games are still traded even when Polymarket has not yet listed them.

A trade is placed when all of the following hold:
- The game starts within **3.0 hours** of the run (uses ESPN's scheduled start time)
- `|model_prob − kalshi_mid| > 2 pp`
- The same game has not already been traded in an earlier run today (deduplication by event ticker)

**Edge direction (fade Kalshi):**

| Edge | Action |
|------|--------|
| `model_prob > kalshi_mid + 2pp` | BUY YES — Kalshi underprices relative to Polymarket |
| `model_prob < kalshi_mid − 2pp` | BUY NO — Kalshi overprices relative to Polymarket |

**Sizing (fractional Kelly criterion):**

For a YES trade at ask price `p`:

$$f = \frac{|\text{edge\_pp}|/100}{1 - p}$$

$$\text{budget} = \min(\text{MAX\_BET},\ f \times \text{KELLY\_FRACTION} \times \text{balance})$$

where `KELLY_FRACTION = 0.25` (quarter-Kelly) and `MAX_BET = $20`. A small edge (e.g. 2pp) at a mid-priced market naturally yields a very small bet; the cap only binds on large edges.

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

### SOS Adjustment

After computing the blended win-rate probability, an opponent-strength (SOS) correction is applied when `SOS_MULTIPLIER > 0` (currently **0.15**):

$$\text{adj}_{\text{home}} = (0.5 - \text{opp\_win\_pct}_{\text{away}}) \times \text{SOS\_MULTIPLIER}$$

where `opp_win_pct_away` is the away team's league-wide win percentage from ESPN standings. A strong away opponent (win pct > 0.5) reduces the home team's estimated probability; a weak opponent increases it. The adjustment is symmetric for both teams and the result is re-normalized. The database is bootstrapped once per day from ESPN standings (`/standings` endpoint, all three leagues).

### Injury Adjustment (win-rate fallback only)

When the model falls back to ESPN win-rate (Tiers 3–4), an injury penalty is applied per team. The ESPN public `/injuries` endpoint is queried once per run and cached in memory.

- **Out / IR / Suspended:** −1.5 pp per player
- **Questionable / Day-to-day:** −0.5 pp per player (one-third weight)
- **Cap:** −5.0 pp maximum per team

This adjustment is **not applied** when ESPN sportsbook odds or Polymarket are used — those market prices already reflect injury information.

---

## Signal 3 — Polymarket Implied Probability

**Source:** Polymarket Gamma API
**Endpoint:** `https://gamma-api.polymarket.com/markets?active=true&closed=false`
**No API key required.**

Polymarket is a decentralized prediction market. Its prices reflect the collective wisdom of real-money bettors and are generally well-calibrated for popular sporting events.

For each game, both team names are searched against Polymarket via the Gamma API's `q` parameter (targeted per-game searches rather than bulk loading). A match is accepted only if at least one word (≥4 chars) from each team name appears in the question.

### Determining outcome framing

Polymarket questions come in two formats:

1. **Team-labeled outcomes** — `outcomes = ["Memphis Grizzlies", "Houston Rockets"]`. The price at index 0 is P(Memphis wins). If the YES team matches `outcomes[0]`, return `prices[0]`; if it matches `outcomes[1]`, return `1 − prices[0]`.

2. **Yes/No outcomes** — `outcomes = ["Yes", "No"]`. The question is inspected to see which team is the subject: whichever team name appears first in the question is assumed to be the team whose win corresponds to "Yes". If the YES team appears first, return `prices[0]`; otherwise return `1 − prices[0]`.

---

## Signal 4 — Tennis Ranking Model (ATP / WTA)

> **Currently disabled.** ATP/WTA were removed from `SPORTS_SERIES` on 2026-04-10. The implementation remains in the codebase but no tennis markets are fetched.

**Source:** ESPN rankings API
**Endpoint:** `http://site.api.espn.com/apis/site/v2/sports/tennis/{league}/rankings`
**No API key required.**

For ATP and WTA matches, a log-rank model is used. Player world rankings are fetched and converted to win probabilities:

$$p_1 = \frac{\ln(r_2 + 1)}{\ln(r_1 + 1) + \ln(r_2 + 1)}$$

where $r_1$ and $r_2$ are the world rankings of player 1 and player 2 (lower rank = better). Unranked players default to rank 200.

**Caveat:** ESPN's rankings endpoint returns **current** rankings, not historical ones. This means the tennis model cannot be backtested without look-ahead bias — March rankings are used even when evaluating January matches. For this reason, tennis is **excluded from all backtests**.

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
| `espn:espn_odds` | ESPN sportsbook only (no Polymarket match found) |
| `espn:win_pct+form` | ESPN win-rate + recent form (no Polymarket match, no sportsbook lines) |
| `espn:win_pct` | ESPN season win-rate only (weakest signal) |
| `espn:ranking(#N vs #M)` | Tennis log-rank model, no Polymarket match |
| `ranking(#N vs #M)` | Tennis log-rank model (Polymarket match also required) |

---

## Data Quality and Limitations

| Issue | Detail |
|-------|--------|
| Polymarket matching | Fuzzy word-overlap; low-quality matches (score < 2) are discarded |
| Polymarket fallback | When no Polymarket match is found, the bot falls back to ESPN signals — weaker but still directional |
| Polymarket framing | Yes/No outcome framing is inferred heuristically; edge cases may misidentify the YES team |
| Polymarket liquidity | Prices are used regardless of market volume — thin markets may have stale prices |
| Tennis look-ahead bias | ESPN rankings are current-only; backtests exclude ATP/WTA; tennis trading disabled |
| Kalshi mid as fair value | The mid-price is used as the market's probability estimate, ignoring spread |
| SOS bootstrapping | Opponent strength uses overall win pct as a proxy — does not account for home/away splits or recent form |
| Injury data scope | Applied only to win-rate fallback; Out/Questionable status may lag real-time updates |

---

## Scheduling and ET Date Handling

The bot runs every 3 hours at UTC 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00. Each run uses a **3.0-hour lookahead window**, matching the cron interval exactly.

### Date fetching: US Eastern time

All game and market fetching uses **US Eastern time** (ET) for the calendar date, not UTC. This prevents a UTC midnight boundary issue where the 00:00 UTC run (8 PM ET) would flip to the next calendar day and fetch next-day markets.

US evening games (e.g. 9 PM ET tipoffs) start at 01:00–04:00 UTC the following calendar day. Kalshi tickers and ESPN schedules for these games are dated the **previous** day (US date). To handle this, both Kalshi market fetching and ESPN game fetching use a **two-day window: yesterday and today (ET)**. Duplicates are deduplicated by `(home, away, start_time)`. This ensures late US evening games are visible to overnight runs without double-counting.

### Trade deduplication across runs

Each run reads today's trade log to build a set of already-traded event tickers. Any market whose event ticker appears in that set is skipped, preventing the same game from being traded in multiple consecutive runs.

---

## Relationship to Backtests

Backtests (`BACKTEST_SUMMARY.md`) used the ESPN win-rate model with NBA and NHL data. The current live strategy (Polymarket as primary signal, fade Kalshi) has not been formally backtested — Polymarket historical price data is not readily available. The theoretical basis is cross-market arbitrage: two liquid markets pricing the same binary event should converge at settlement.
