# Trade Log

All trades placed by `claude_code/kalshi_sports_bot.py`.
Prices are the limit-order ask price (YES bets) or `1 − bid` (NO bets).
Model estimates and Kalshi implied probabilities are percentages for the YES outcome.

> **Note on March 26 trades 2 & 3:** The daily log resets at midnight and was overwritten before model/edge data was saved. Kalshi mid is reconstructed from the settled market's `previous_yes_ask/bid`; model probability and exact fill price were not captured.

> **Strategy change — Apr 2 through Apr 6:** Switched from "fade Kalshi" to "trust Kalshi" with inverse sizing. See backtest notes in `BACKTEST_SUMMARY.md`.

> **Strategy change — Apr 7 onward:** Switching to cross-market arb (fade Kalshi). The model is now Polymarket's implied probability (+ 50% ESPN sportsbook odds when available). The bot only trades when a Polymarket market matches the game **and** the game starts within 3 hours of the run. Edge = `model_prob − kalshi_mid`; when Polymarket prices a side higher than Kalshi, buy that side. Sizing is proportional to the spread: $10 at 10pp, $20 at 20pp+. Runs every 3 hours; up to 10 trades per run.

---

## 2026-05-01

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 6: Denver at Minnesota Winner? | NBA | BUY YES | $6.67 (23 × 29¢) | 49.8% | 49.8% | 28.5¢ | +21.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$16.33 |
| 2 | Game 6: Edmonton at Anaheim Winner? | NHL | BUY NO | $3.22 (7 × 46¢) | 46.7% | 46.7% | 54.5¢ | -7.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.78 |
| 3 | Arizona vs Chicago C Winner? | MLB | BUY YES | $1.74 (3 × 58¢) | 60.2% | 60.2% | 57.5¢ | +2.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 4 | Game 6: Cleveland at Toronto Winner? | NBA | BUY YES | $6.84 (19 × 36¢) | 48.9% | 48.9% | 35.5¢ | +13.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 5 | Philadelphia vs Miami Winner? | MLB | BUY NO | $8.00 (16 × 50¢) | 38.5% | 38.5% | 50.5¢ | -12.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 6 | Milwaukee vs Washington Winner? | MLB | BUY YES | $4.20 (10 × 42¢) | 48.7% | 48.7% | 41.5¢ | +7.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 7 | Cincinnati vs Pittsburgh Winner? | MLB | BUY NO | $4.14 (9 × 46¢) | 47.7% | 47.7% | 54.5¢ | -6.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 8 | Game 6: Tampa Bay at Montreal Winner? | NHL | BUY NO | $4.41 (9 × 49¢) | 44.8% | 44.8% | 51.5¢ | -6.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $39.22**

---
## 2026-04-30

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 5: Houston at Los Angeles L Winner? | NBA | BUY NO | $1.60 (4 × 40¢) | 55.7% | 55.7% | 60.5¢ | -4.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.40 |
| 2 | Game 5: Utah at Vegas Winner? | NHL | BUY NO | $1.23 (3 × 41¢) | 56.1% | 56.1% | 59.5¢ | -3.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.23 |
| 3 | Game 6: Boston at Philadelphia Winner? | NBA | BUY YES | $6.08 (19 × 32¢) | 47.8% | 47.8% | 31.5¢ | +16.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$12.92 |
| 4 | Toronto vs Minnesota Winner? | MLB | BUY NO | $3.15 (7 × 45¢) | 48.8% | 48.8% | 55.5¢ | -6.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.85 |
| 5 | Game 6: New York at Atlanta Winner? | NBA | BUY NO | $2.58 (6 × 43¢) | 51.1% | 51.1% | 57.5¢ | -6.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.58 |

**Total wagered: $14.64**  |  **Net P&L: +$15.36**

---
## 2026-04-29

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 5: Portland at San Antonio Winner? | NBA | BUY NO | $3.60 (20 × 18¢) | 64.9% | 64.9% | 82.5¢ | -17.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.60 |
| 2 | Game 5: Anaheim at Edmonton Winner? | NHL | BUY NO | $0.82 (2 × 41¢) | 55.6% | 55.6% | 59.5¢ | -3.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.82 |
| 3 | Game 5: Toronto at Cleveland Winner? | NBA | BUY YES | $6.44 (28 × 23¢) | 40.9% | 40.9% | 22.5¢ | +18.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$6.44 |
| 4 | Game 5: Orlando at Detroit Winner? | NBA | BUY YES | $5.06 (22 × 23¢) | 37.1% | 37.1% | 22.5¢ | +14.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$5.06 |
| 5 | Game 5: Montreal at Tampa Bay Winner? | NHL | BUY NO | $2.87 (7 × 41¢) | 52.9% | 52.9% | 59.5¢ | -6.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.13 |

**Total wagered: $18.79**  |  **Net P&L: −$11.79**

---
## 2026-04-28

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 4: Oklahoma City at Phoenix Winner? | NBA | BUY YES | $8.93 (47 × 19¢) | 44.0% | 44.0% | 18.5¢ | +25.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$8.93 |
| 2 | Game 5: Minnesota at Denver Winner? | NBA | BUY YES | $8.00 (40 × 20¢) | 42.5% | 42.5% | 19.5¢ | +23.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$8.00 |
| 3 | Miami vs Los Angeles D Winner? | MLB | BUY YES | $3.24 (12 × 27¢) | 34.9% | 34.9% | 26.5¢ | +8.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.24 |
| 4 | Game 4: Vegas at Utah Winner? | NHL | BUY NO | $3.60 (8 × 45¢) | 48.0% | 48.0% | 55.5¢ | -7.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.60 |
| 5 | New York Y vs Texas Winner? | MLB | BUY YES | $2.46 (6 × 41¢) | 45.8% | 45.8% | 40.5¢ | +5.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.46 |
| 6 | Game 5: Philadelphia at Boston Winner? | NBA | BUY YES | $6.65 (35 × 19¢) | 39.8% | 39.8% | 18.5¢ | +21.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$28.35 |
| 7 | Washington vs New York M Winner? | MLB | BUY YES | $7.22 (19 × 38¢) | 55.5% | 55.5% | 37.5¢ | +18.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$7.22 |
| 8 | San Francisco vs Philadelphia Winner? | MLB | BUY YES | $7.38 (18 × 41¢) | 57.9% | 57.9% | 40.5¢ | +17.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$7.38 |
| 9 | Detroit vs Atlanta Winner? | MLB | BUY NO | $5.40 (10 × 54¢) | 36.5% | 36.5% | 46.5¢ | -10.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.60 |
| 10 | Game 5: Atlanta at New York Winner? | NBA | BUY NO | $3.41 (11 × 31¢) | 59.6% | 59.6% | 69.5¢ | -9.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.41 |

**Total wagered: $56.29**  |  **Net P&L: −$11.29**

---
## 2026-04-27

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 4: Edmonton at Anaheim Winner? | NHL | BUY NO | $4.14 (9 × 46¢) | 46.7% | 46.7% | 54.5¢ | -7.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.86 |
| 2 | Game 4: Los Angeles L at Houston Winner? | NBA | BUY YES | $1.35 (3 × 45¢) | 47.0% | 47.0% | 44.5¢ | +2.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.35 |
| 3 | Game 4: Detroit at Orlando Winner? | NBA | BUY YES | $2.46 (6 × 41¢) | 45.6% | 45.6% | 40.5¢ | +5.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.54 |
| 4 | Seattle vs Minnesota Winner? | MLB | BUY NO | $2.30 (5 × 46¢) | 49.7% | 49.7% | 54.5¢ | -4.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.70 |
| 5 | Tampa Bay vs Cleveland Winner? | MLB | BUY YES | $2.25 (5 × 45¢) | 48.6% | 48.6% | 44.5¢ | +4.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.75 |
| 6 | St. Louis vs Pittsburgh Winner? | MLB | BUY NO | $2.16 (4 × 54¢) | 43.0% | 43.0% | 46.5¢ | -3.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.16 |

**Total wagered: $14.66**  |  **Net P&L: +$10.34**

---
## 2026-04-26

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 4: Denver at Minnesota Winner? | NBA | BUY YES | $1.96 (4 × 49¢) | 52.1% | 52.1% | 48.5¢ | +3.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.04 |
| 2 | Game 4: Cleveland at Toronto Winner? | NBA | BUY YES | $5.20 (13 × 40¢) | 48.9% | 48.9% | 39.5¢ | +9.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$7.80 |
| 3 | Game 4: San Antonio at Portland Winner? | NBA | BUY NO | $4.55 (13 × 35¢) | 55.8% | 55.8% | 65.5¢ | -9.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.55 |
| 4 | Game 4: Colorado at Los Angeles Winner? | NHL | BUY YES | $3.90 (10 × 39¢) | 45.9% | 45.9% | 38.5¢ | +7.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.90 |
| 5 | Game 4: Boston at Philadelphia Winner? | NBA | BUY YES | $9.45 (35 × 27¢) | 47.0% | 47.0% | 26.5¢ | +20.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$9.45 |
| 6 | Game 4: Tampa Bay at Montreal Winner? | NHL | BUY NO | $4.90 (10 × 49¢) | 43.9% | 43.9% | 51.5¢ | -7.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.90 |

**Total wagered: $29.96**  |  **Net P&L: −$12.96**

---
## 2026-04-25

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Seattle vs St. Louis Winner? | MLB | BUY YES | $6.16 (14 × 44¢) | 62.5% | 62.5% | 43.5¢ | +19.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$6.16 |
| 2 | Game 3: Edmonton at Anaheim Winner? | NHL | BUY NO | $3.08 (7 × 44¢) | 46.7% | 46.7% | 56.5¢ | -9.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.92 |
| 3 | Game 3: San Antonio at Portland Winner? | NBA | BUY NO | $1.20 (3 × 40¢) | 55.8% | 55.8% | 60.5¢ | -4.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.20 |
| 4 | Game 3: Vegas at Utah Winner? | NHL | BUY NO | $0.98 (2 × 49¢) | 48.0% | 48.0% | 51.5¢ | -3.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.02 |
| 5 | Miami vs San Francisco Winner? | MLB | BUY YES | $1.00 (2 × 50¢) | 52.5% | 52.5% | 49.5¢ | +3.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.00 |
| 6 | Game 3: Oklahoma City at Phoenix Winner? | NBA | BUY YES | $10.12 (44 × 23¢) | 44.0% | 44.0% | 22.5¢ | +21.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$10.12 |
| 7 | Game 4: Carolina at Ottawa Winner? | NHL | BUY YES | $1.38 (3 × 46¢) | 48.0% | 48.0% | 45.5¢ | +2.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.38 |
| 8 | San Diego vs Arizona Winner? | MLB | BUY YES | $2.94 (6 × 49¢) | 53.0% | 53.0% | 48.5¢ | +4.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.06 |
| 9 | Game 4: Dallas at Minnesota Winner? | NHL | BUY NO | $1.84 (4 × 46¢) | 51.1% | 51.1% | 54.5¢ | -3.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.84 |
| 10 | Game 4: New York at Atlanta Winner? | NBA | BUY NO | $1.84 (4 × 46¢) | 51.4% | 51.4% | 54.5¢ | -3.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.84 |

**Total wagered: $30.54**  |  **Net P&L: −$15.54**

---
## 2026-04-24

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 3: Colorado at Los Angeles Winner? | NHL | BUY YES | $2.40 (6 × 40¢) | 45.2% | 45.2% | 39.5¢ | +5.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.40 |
| 2 | Game 3: Boston at Philadelphia Winner? | NBA | BUY YES | $8.58 (33 × 26¢) | 47.2% | 47.2% | 25.5¢ | +21.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$8.58 |
| 3 | Game 3: Los Angeles L at Houston Winner? | NBA | BUY YES | $7.83 (29 × 27¢) | 46.6% | 46.6% | 26.5¢ | +20.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$21.17 |
| 4 | Philadelphia vs Atlanta Winner? | MLB | BUY NO | $12.39 (21 × 59¢) | 23.7% | 23.7% | 41.5¢ | -17.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$8.61 |
| 5 | Colorado vs New York M Winner? | MLB | BUY NO | $6.65 (19 × 35¢) | 50.7% | 50.7% | 65.5¢ | -14.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$12.35 |
| 6 | Detroit vs Cincinnati Winner? | MLB | BUY NO | $5.88 (12 × 49¢) | 40.9% | 40.9% | 51.5¢ | -10.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$6.12 |

**Total wagered: $43.73**  |  **Net P&L: +$37.27**

---
## 2026-04-23

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 2: Phoenix at Oklahoma City Winner? | NBA | BUY YES | $8.19 (91 × 9¢) | 35.4% | 35.4% | 8.5¢ | +26.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$8.19 |
| 2 | Game 2: Anaheim at Edmonton Winner? | NHL | BUY NO | $4.07 (11 × 37¢) | 53.9% | 53.9% | 63.5¢ | -9.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$6.93 |
| 3 | Game 3: Dallas at Minnesota Winner? | NHL | BUY NO | $1.35 (3 × 45¢) | 52.1% | 52.1% | 55.5¢ | -3.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.65 |
| 4 | Game 3: Cleveland at Toronto Winner? | NBA | BUY YES | $3.44 (8 × 43¢) | 49.9% | 49.9% | 42.5¢ | +7.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.56 |
| 5 | Game 3: Carolina at Ottawa Winner? | NHL | BUY NO | $1.44 (3 × 48¢) | 49.3% | 49.3% | 52.5¢ | -3.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.56 |

**Total wagered: $18.49**  |  **Net P&L: +$6.51**

---
## 2026-04-22

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 2: Houston at Los Angeles L Winner? | NBA | BUY YES | $7.48 (22 × 34¢) | 54.5% | 54.5% | 33.5¢ | +21.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$14.52 |
| 2 | Game 2: Los Angeles at Colorado Winner? | NHL | BUY YES | $2.70 (9 × 30¢) | 38.1% | 38.1% | 29.5¢ | +8.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.70 |
| 3 | Chicago WS vs Arizona Winner? | MLB | BUY NO | $4.13 (7 × 59¢) | 34.1% | 34.1% | 41.5¢ | -7.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.13 |
| 4 | Los Angeles D vs San Francisco Winner? | MLB | BUY YES | $0.76 (2 × 38¢) | 40.0% | 40.0% | 37.5¢ | +2.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.24 |
| 5 | San Diego vs Colorado Winner? | MLB | BUY YES | $0.58 (1 × 58¢) | 59.5% | 59.5% | 57.5¢ | +2.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.42 |
| 6 | Game 2: Orlando at Detroit Winner? | NBA | BUY YES | $5.52 (24 × 23¢) | 37.2% | 37.2% | 22.5¢ | +14.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$5.52 |
| 7 | Game 3: Pittsburgh at Philadelphia Winner? | NHL | BUY NO | $1.02 (2 × 51¢) | 47.0% | 47.0% | 49.5¢ | -2.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.98 |

**Total wagered: $22.19**  |  **Net P&L: +$4.81**

---
## 2026-04-21

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 2: Minnesota at Denver Winner? | NBA | BUY YES | $5.04 (18 × 28¢) | 43.6% | 43.6% | 27.5¢ | +16.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$12.96 |
| 2 | Toronto vs Los Angeles A Winner? | MLB | BUY NO | $4.50 (9 × 50¢) | 40.3% | 40.3% | 50.5¢ | -10.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.50 |
| 3 | Game 1: Anaheim at Edmonton Winner? | NHL | BUY NO | $3.33 (9 × 37¢) | 54.5% | 54.5% | 63.5¢ | -9.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.33 |
| 4 | Game 2: Philadelphia at Boston Winner? | NBA | BUY YES | $10.66 (82 × 13¢) | 40.6% | 40.6% | 12.5¢ | +28.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$71.34 |
| 5 | Game 2: Portland at San Antonio Winner? | NBA | BUY NO | $8.16 (51 × 16¢) | 63.6% | 63.6% | 84.5¢ | -20.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$42.84 |
| 6 | Minnesota vs New York M Winner? | MLB | BUY NO | $9.02 (22 × 41¢) | 42.9% | 42.9% | 59.5¢ | -16.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$12.98 |
| 7 | Game 2: Montreal at Tampa Bay Winner? | NHL | BUY NO | $4.56 (12 × 38¢) | 53.7% | 53.7% | 62.5¢ | -8.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.56 |
| 8 | New York Y vs Boston Winner? | MLB | BUY YES | $5.17 (11 × 47¢) | 55.1% | 55.1% | 46.5¢ | +8.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$5.83 |

**Total wagered: $50.44**  |  **Net P&L: +$133.56**

---
## 2026-04-20

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 1: Portland at San Antonio Winner? | NBA | BUY NO | $6.12 (36 × 17¢) | 63.6% | 63.6% | 83.5¢ | -19.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$6.12 |
| 2 | Game 1: Utah at Vegas Winner? | NHL | BUY NO | $1.64 (4 × 41¢) | 55.5% | 55.5% | 59.5¢ | -4.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.64 |
| 3 | Game 2: Toronto at Cleveland Winner? | NBA | BUY YES | $9.02 (41 × 22¢) | 42.9% | 42.9% | 21.5¢ | +21.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$9.02 |
| 4 | Philadelphia vs Chicago C Winner? | MLB | BUY NO | $8.67 (17 × 51¢) | 36.0% | 36.0% | 49.5¢ | -13.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$8.33 |
| 5 | Game 2: Atlanta at New York Winner? | NBA | BUY NO | $5.58 (18 × 31¢) | 57.5% | 57.5% | 69.5¢ | -12.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$12.42 |
| 6 | Houston vs Cleveland Winner? | MLB | BUY NO | $8.25 (15 × 55¢) | 34.1% | 34.1% | 45.5¢ | -11.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$8.25 |
| 7 | St. Louis vs Miami Winner? | MLB | BUY YES | $4.60 (10 × 46¢) | 53.7% | 53.7% | 45.5¢ | +8.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.60 |

**Total wagered: $43.88**  |  **Net P&L: −$8.88**

---
## 2026-04-19

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Houston at Los Angeles L Winner? | NBA | BUY YES | $6.16 (14 × 44¢) | 54.5% | 54.5% | 43.5¢ | +11.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$7.84 |
| 2 | Game 1: Philadelphia at Boston Winner? | NBA | BUY YES | $11.44 (88 × 13¢) | 40.6% | 40.6% | 12.5¢ | +28.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$11.44 |
| 3 | Game 1: Phoenix at Oklahoma City Winner? | NBA | BUY YES | $10.00 (100 × 10¢) | 37.3% | 37.3% | 9.5¢ | +27.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$10.00 |
| 4 | Game 1: Los Angeles at Colorado Winner? | NHL | BUY YES | $3.90 (13 × 30¢) | 38.1% | 38.1% | 29.5¢ | +8.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.90 |
| 5 | Game 1: Orlando at Detroit Winner? | NBA | BUY YES | $5.98 (26 × 23¢) | 38.9% | 38.9% | 22.5¢ | +16.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$20.02 |
| 6 | Game 1: Montreal at Tampa Bay Winner? | NHL | BUY NO | $3.80 (10 × 38¢) | 53.7% | 53.7% | 62.5¢ | -8.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$6.20 |
| 7 | Game 1: Boston at Buffalo Winner? | NHL | BUY NO | $1.23 (3 × 41¢) | 56.3% | 56.3% | 59.5¢ | -3.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.23 |

**Total wagered: $42.51**  |  **Net P&L: +$7.49**

---
## 2026-04-18

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Los Angeles D vs Colorado Winner? | MLB | BUY NO | $4.05 (15 × 27¢) | 63.9% | 63.9% | 73.5¢ | -9.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.05 |
| 2 | San Diego vs Los Angeles A Winner? | MLB | BUY YES | $4.60 (10 × 46¢) | 53.8% | 53.8% | 45.5¢ | +8.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.60 |
| 3 | St. Louis vs Houston Winner? | MLB | BUY YES | $4.23 (9 × 47¢) | 54.1% | 54.1% | 46.5¢ | +7.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.77 |
| 4 | Texas vs Seattle Winner? | MLB | BUY YES | $4.14 (9 × 46¢) | 52.8% | 52.8% | 45.5¢ | +7.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.86 |
| 5 | Toronto vs Arizona Winner? | MLB | BUY NO | $5.13 (9 × 57¢) | 36.2% | 36.2% | 43.5¢ | -7.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.87 |
| 6 | Toronto at Cleveland Winner? | NBA | BUY YES | $9.84 (41 × 24¢) | 42.9% | 42.9% | 23.5¢ | +19.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$9.84 |
| 7 | Minnesota at Denver Winner? | NBA | BUY YES | $7.54 (26 × 29¢) | 43.6% | 43.6% | 28.5¢ | +15.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$7.54 |
| 8 | Atlanta at New York Winner? | NBA | BUY NO | $5.44 (17 × 32¢) | 57.5% | 57.5% | 68.5¢ | -11.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$5.44 |
| 9 | Game 1: Philadelphia at Pittsburgh Winner? | NHL | BUY NO | $1.72 (4 × 43¢) | 54.3% | 54.3% | 57.5¢ | -3.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.28 |

**Total wagered: $46.69**  |  **Net P&L: −$15.69**

---
## 2026-04-17

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Los Angeles at Calgary Winner? | NHL | BUY NO | $5.20 (13 × 40¢) | 51.6% | 51.6% | 60.5¢ | -8.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$7.80 |
| 2 | Vancouver at Edmonton Winner? | NHL | BUY YES | $3.64 (14 × 26¢) | 33.5% | 33.5% | 25.5¢ | +8.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.64 |
| 3 | New York M vs Chicago C Winner? | MLB | BUY NO | $2.36 (4 × 59¢) | 38.4% | 38.4% | 41.5¢ | -3.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.64 |
| 4 | San Francisco vs Washington Winner? | MLB | BUY YES | $11.61 (27 × 43¢) | 60.2% | 60.2% | 42.5¢ | +17.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$11.61 |
| 5 | Charlotte at Orlando Winner? | NBA | BUY YES | $8.40 (20 × 42¢) | 54.6% | 54.6% | 41.5¢ | +13.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$11.60 |
| 6 | Detroit vs Boston Winner? | MLB | BUY YES | $4.70 (10 × 47¢) | 53.5% | 53.5% | 46.5¢ | +7.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.70 |
| 7 | Atlanta vs Philadelphia Winner? | MLB | BUY NO | $2.08 (4 × 52¢) | 45.3% | 45.3% | 48.5¢ | -3.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.92 |

**Total wagered: $37.99**  |  **Net P&L: +$3.01**

---
## 2026-04-16

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Seattle at Vegas Winner? | NHL | BUY NO | $7.54 (29 × 26¢) | 58.7% | 58.7% | 74.5¢ | -15.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$7.54 |
| 2 | St. Louis at Utah Winner? | NHL | BUY YES | $7.82 (17 × 46¢) | 56.4% | 56.4% | 45.5¢ | +10.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$7.82 |
| 3 | Anaheim at Nashville Winner? | NHL | BUY YES | $4.70 (10 × 47¢) | 52.9% | 52.9% | 46.5¢ | +6.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.70 |
| 4 | San Jose at Winnipeg Winner? | NHL | BUY NO | $3.78 (9 × 42¢) | 53.3% | 53.3% | 59.0¢ | -5.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$5.22 |

**Total wagered: $23.84**  |  **Net P&L: −$14.84**

---
## 2026-04-15

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Detroit at Florida Winner? | NHL | BUY YES | $6.56 (16 × 41¢) | 50.7% | 50.7% | 40.5¢ | +10.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$9.44 |
| 2 | Dallas at Buffalo Winner? | NHL | BUY NO | $6.60 (15 × 44¢) | 46.9% | 46.9% | 56.5¢ | -9.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$6.60 |
| 3 | Toronto at Ottawa Winner? | NHL | BUY YES | $2.52 (7 × 36¢) | 39.7% | 39.7% | 35.5¢ | +4.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.52 |
| 4 | New York R at Tampa Bay Winner? | NHL | BUY YES | $2.44 (4 × 61¢) | 63.3% | 63.3% | 60.5¢ | +2.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.44 |

**Total wagered: $18.12**  |  **Net P&L: −$2.12**

---
## 2026-04-14

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Los Angeles at Seattle Winner? | NHL | BUY YES | $1.56 (4 × 39¢) | 50.9% | 50.9% | 38.5¢ | +12.4 pp | espn:win_pct | ❌ LOSS −$1.56 |
| 2 | Buffalo at Chicago Winner? | NHL | BUY YES | $0.72 (2 × 36¢) | 42.4% | 42.4% | 35.5¢ | +6.9 pp | espn:win_pct | ❌ LOSS −$0.72 |
| 3 | Winnipeg at Vegas Winner? | NHL | BUY YES | $0.76 (2 × 38¢) | 43.1% | 43.1% | 37.5¢ | +5.6 pp | espn:win_pct | ❌ LOSS −$0.76 |
| 4 | Montreal at Philadelphia Winner? | NHL | BUY YES | $10.20 (34 × 30¢) | 51.4% | 51.4% | 29.5¢ | +21.9 pp | espn:win_pct | pending |
| 5 | Miami at Charlotte Winner? | NBA | BUY YES | $6.82 (22 × 31¢) | 45.4% | 45.4% | 30.5¢ | +14.9 pp | espn:win_pct | pending |
| 6 | Anaheim at Minnesota Winner? | NHL | BUY YES | $7.92 (18 × 44¢) | 57.5% | 57.5% | 43.5¢ | +14.0 pp | espn:win_pct | pending |
| 7 | San Francisco vs Cincinnati Winner? | MLB | BUY NO | $8.32 (16 × 52¢) | 36.0% | 36.0% | 48.5¢ | -12.5 pp | espn:win_pct | pending |
| 8 | Carolina at New York I Winner? | NHL | BUY NO | $5.74 (14 × 41¢) | 48.6% | 48.6% | 59.5¢ | -10.9 pp | espn:win_pct | pending |

**Total wagered: $42.04**

---
## 2026-04-13

No trades placed today.

---
## 2026-04-12

No trades placed today.

---
## 2026-04-11

No trades placed today.

---
## 2026-04-10

No trades placed today.

---
## 2026-04-09

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Memphis at Denver Winner? | NBA | BUY YES | $9.99 (333 × 3¢) | 28.9% | 28.9% | 2.5¢ | +26.4 pp | espn:win_pct | ❌ LOSS −$9.99 |
| 2 | Dallas at Phoenix Winner? | NBA | BUY NO | $9.00 (60 × 15¢) | 67.2% | 67.2% | 85.5¢ | -18.3 pp | espn:win_pct | ❌ LOSS −$9.00 |

**Total wagered: $18.99**  |  **Net P&L: −$18.99**

---
## 2026-04-08

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Will Andrey Rublev win the Rublev vs Bergs : Round Of 32 match? | ATP | BUY NO | $12.00 (40 × 30¢) | 58.3% | 58.3% | 70.5¢ | -12.2 pp | espn:ranking(#47 vs #15) | ✅ WIN +$28.00 |
| 2 | Will Arthur Rinderknech win the Fonseca vs Rinderknech : Round Of 32 match? | ATP | BUY YES | $20.00 (80 × 25¢) | 52.7% | 52.7% | 24.5¢ | +28.2 pp | espn:ranking(#27 vs #40) | ❌ LOSS −$20.00 |
| 3 | Will Tomas Martin Etcheverry win the Etcheverry vs Atmane : Round Of 32 match? | ATP | BUY NO | $18.56 (64 × 29¢) | 52.7% | 52.7% | 71.5¢ | -18.8 pp | espn:ranking(#45 vs #30) | ❌ LOSS −$18.56 |
| 4 | Will Tomas Machac win the Cerundolo vs Machac : Round Of 32 match? | ATP | BUY YES | $16.20 (60 × 27¢) | 42.9% | 42.9% | 26.5¢ | +16.4 pp | espn:ranking(#53 vs #19) | ✅ WIN +$43.80 |
| 5 | Will Casper Ruud win the Moutet vs Ruud : Round Of 32 match? | ATP | BUY NO | $14.84 (53 × 28¢) | 57.5% | 57.5% | 72.5¢ | -15.0 pp | espn:ranking(#12 vs #31) | ❌ LOSS −$14.84 |
| 6 | Will Alexander Zverev win the Garin vs Zverev : Round Of 32 match? | ATP | BUY NO | $11.16 (93 × 12¢) | 77.2% | 77.2% | 88.5¢ | -11.3 pp | espn:ranking(#3 vs #109) | ❌ LOSS −$11.16 |
| 7 | Will Jelena Ostapenko win the Ostapenko vs Eala : Round Of 16 match? | WTA | BUY NO | $10.50 (30 × 35¢) | 54.8% | 54.8% | 65.5¢ | -10.7 pp | espn:ranking(#46 vs #23) | ❌ LOSS −$10.50 |
| 8 | Will Panna Udvardy win the Kalinina vs Udvardy : Round Of 32 match? | WTA | BUY YES | $19.78 (86 × 23¢) | 52.9% | 52.9% | 22.5¢ | +30.4 pp | espn:ranking(#71 vs #120) | ❌ LOSS −$19.78 |
| 9 | Will Tomas Martin Etcheverry win the Etcheverry vs Atmane : Round Of 32 match? | ATP | BUY NO | $18.56 (64 × 29¢) | 52.7% | 52.7% | 71.5¢ | -18.8 pp | espn:ranking(#45 vs #30) | ❌ LOSS −$11.60 |
| 10 | Will Tomas Machac win the Cerundolo vs Machac : Round Of 32 match? | ATP | BUY YES | $17.16 (66 × 26¢) | 42.9% | 42.9% | 25.5¢ | +17.4 pp | espn:ranking(#53 vs #19) | ✅ WIN +$48.84 |
| 11 | Will Casper Ruud win the Moutet vs Ruud : Round Of 32 match? | ATP | BUY NO | $15.93 (59 × 27¢) | 57.5% | 57.5% | 73.5¢ | -16.0 pp | espn:ranking(#12 vs #31) | ❌ LOSS −$15.93 |
| 12 | Will Sloane Stephens win the Andreeva vs Stephens : Round Of 16 match? | WTA | BUY YES | $20.00 (250 × 8¢) | 31.1% | 31.1% | 7.5¢ | +23.6 pp | espn:ranking(#200 vs #10) | ❌ LOSS −$20.00 |
| 13 | Will Dalma Galfi win the Galfi vs Cirstea : Round Of 16 match? | WTA | BUY YES | $18.72 (78 × 24¢) | 42.3% | 42.3% | 23.5¢ | +18.8 pp | espn:ranking(#29 vs #103) | ❌ LOSS −$18.72 |
| 14 | Will Dalma Galfi win the Galfi vs Cirstea : Round Of 16 match? | WTA | BUY YES | $9.66 (42 × 23¢) | 42.3% | 42.3% | 22.5¢ | +19.8 pp | espn:ranking(#29 vs #103) | ❌ LOSS −$9.66 |
| 15 | Milwaukee at Detroit Winner? | NBA | BUY YES | $10.00 (200 × 5¢) | 31.2% | 31.2% | 4.5¢ | +26.7 pp | espn:win_pct | ❌ LOSS −$10.00 |
| 16 | Minnesota at Orlando Winner? | NBA | BUY NO | $9.90 (45 × 22¢) | 51.8% | 51.8% | 78.5¢ | -26.7 pp | espn:win_pct | ❌ LOSS −$9.90 |
| 17 | Washington at Toronto Winner? | NHL | BUY NO | $5.04 (12 × 42¢) | 48.7% | 48.7% | 59.0¢ | -10.3 pp | espn:win_pct | ❌ LOSS −$5.04 |

**Total wagered: $248.01**  |  **Net P&L: −$75.05**

---
## 2026-04-07

No trades placed today.

---
## 2026-04-06

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Philadelphia at San Antonio Winner? | NBA | BUY YES | $3.85 (5 × 77¢) | 61.8% | 51.8% | 76.5¢ | +24.7 pp | polymarket(75%)+win_pct(25%) | ✅ WIN +$1.15 |
| 2 | Will Dalma Galfi win the Parks vs Galfi : Round Of 32 match? | WTA | BUY YES | $9.12 (12 × 76¢) | 49.5% | 64.9% | 75.5¢ | +10.6 pp | polymarket(75%)+ranking(#103 vs #93)(25%) | ✅ WIN +$2.88 |
| 3 | Philadelphia at San Antonio Winner? | NBA | BUY NO | $19.92 (83 × 24¢) | 61.8% | 48.5% | 76.5¢ | -28.0 pp | polymarket | ❌ LOSS −$19.92 |

**Total wagered: $32.89**  |  **Net P&L: −$15.89**

---
## 2026-04-05

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Houston at Golden State Winner? | NBA | BUY YES | $9.76 (16 × 61¢) | 53.1% | 41.0% | 60.5¢ | -19.5 pp | polymarket(75%)+win_pct(25%) | ✅ WIN +$6.24 |
| 2 | Will Mariano Navone win the Navone vs Merida : Final match? | ATP | BUY YES | $9.24 (12 × 77¢) | 54.5% | 61.2% | 76.5¢ | -15.3 pp | polymarket(75%)+ranking(#136 vs #60)(25%) | ✅ WIN +$2.76 |
| 3 | Will Alexandre Muller win the Arnaldi vs Muller : Qualification Final match? | ATP | BUY YES | $9.90 (11 × 90¢) | 50.7% | 77.2% | 89.0¢ | -11.8 pp | polymarket(75%)+ranking(#94 vs #107)(25%) | ✅ WIN +$1.10 |
| 4 | Will Donna Vekic win the Monnet vs Vekic : Qualification Round 1 match? | WTA | BUY YES | $9.90 (10 × 99¢) | 52.7% | 87.7% | 98.0¢ | -10.3 pp | polymarket(75%)+ranking(#115 vs #200)(25%) | ✅ WIN +$0.10 |

**Total wagered: $38.80**  |  **Net P&L: +$10.20**

---
## 2026-04-04

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Detroit at New York R Winner? | NHL | BUY YES | $9.68 (22 × 44¢) | 47.7% | 12.1% | 43.5¢ | -31.4 pp | polymarket(75%)+win_pct(25%) | ✅ WIN +$12.32 |
| 2 | Will Marco Trungelliti win the Darderi vs Trungelliti : Semifinal match? | ATP | BUY YES | $9.54 (18 × 53¢) | 38.6% | 31.8% | 52.5¢ | -20.7 pp | polymarket(75%)+ranking(#117 vs #19)(25%) | ✅ WIN +$8.46 |
| 3 | Will Cristian Garin win the Garin vs De Jong : Qualification match? | ATP | BUY YES | $9.90 (10 × 99¢) | 50.0% | 86.6% | 98.5¢ | -11.9 pp | polymarket(75%)+ranking(#99 vs #100)(25%) | — (unfilled) |
| 4 | Boston at Tampa Bay Winner? | NHL | BUY YES | $9.45 (15 × 63¢) | 55.9% | 51.5% | 62.0¢ | -10.5 pp | polymarket(75%)+win_pct(25%) | ✅ WIN +$5.55 |

**Total wagered: $38.57**  |  **Net P&L: +$26.33**

---
## 2026-04-03

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Chicago at New York Winner? | NBA | BUY YES | $9.20 (10 × 92¢) | 66.5% | 16.9% | 91.5¢ | -74.7 pp | polymarket(75%)+win_pct(25%) | ✅ WIN +$0.80 |

**Total wagered: $9.20**  |  **Net P&L: +$0.80**

---
## 2026-04-02

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Los Angeles L at Oklahoma City Winner? | NBA | BUY YES | $9.24 (12 × 77¢) | 58.6% | 24.0% | 76.0¢ | -52.0 pp | polymarket(75%)+win_pct(25%) | ✅ WIN +$2.76 |

**Total wagered: $9.24**  |  **Net P&L: +$2.76**

---
## 2026-04-01

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | San Antonio at Golden State Winner? | NBA | BUY NO | $9.96 (83 × 12¢) | 57.3% | 40.8% | 88.5¢ | -47.7 pp | polymarket(75%)+win_pct(25%) | ❌ LOSS −$9.96 |
| 2 | Philadelphia at Washington Winner? | NBA | BUY YES | $10.00 (125 × 8¢) | 33.3% | 29.7% | 7.5¢ | +22.2 pp | polymarket(75%)+win_pct(25%) | ❌ LOSS −$10.00 |
| 3 | San Francisco vs San Diego Winner? | MLB | BUY NO | $9.89 (23 × 43¢) | 37.3% | 40.5% | 58.0¢ | -17.5 pp | polymarket(75%)+win_pct(25%) | ❌ LOSS −$9.89 |
| 4 | Los Angeles A vs Chicago C Winner? | MLB | BUY YES | $9.84 (24 × 41¢) | 51.6% | 54.9% | 40.0¢ | +14.9 pp | polymarket(75%)+win_pct(25%) | ❌ LOSS −$9.84 |

**Total wagered: $39.69**  |  **Net P&L: −$39.69**

---
## 2026-03-31

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | New Jersey at New York R Winner? | NHL | BUY NO | $9.72 (18 × 54¢) | 50.3% | 12.8% | 46.5¢ | -33.7 pp | polymarket(75%)+win_pct(25%) | ❌ LOSS −$9.72 |
| 2 | Cleveland at Los Angeles L Winner? | NBA | BUY YES | $9.52 (17 × 56¢) | 55.0% | 66.3% | 55.5¢ | +10.8 pp | polymarket(75%)+win_pct(25%) | ✅ WIN +$7.48 |

**Total wagered: $19.24**  |  **Net P&L: −$2.24**

---
## 2026-03-30

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Will Alex Molcan win the Molcan vs Clarke : Qualification Final match? | ATP | BUY NO | $9.90 (33 × 30¢) | 50.0% | 50.0% | 71.0¢ | -21.0 pp | espn:ranking(#200 vs #200) | ❌ LOSS −$9.90 |
| 2 | Washington at Los Angeles L Winner? | NBA | BUY YES | $9.99 (111 × 9¢) | 22.1% | 25.8% | 8.5¢ | +17.3 pp | polymarket(75%)+win_pct(25%) | ❌ LOSS −$9.99 |
| 3 | Will Rei Sakamoto win the Trungelliti vs Sakamoto : Qualification Final match? | ATP | BUY YES | $9.88 (38 × 26¢) | 47.4% | 37.3% | 25.5¢ | +11.8 pp | polymarket(75%)+ranking(#200 vs #117)(25%) | ❌ LOSS −$9.88 |

**Total wagered: $29.77**  |  **Net P&L: −$29.77**

---
## 2026-03-29

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Will Timofey Skatov win the Pellegrino vs Skatov : Qualification Round 1 match? | ATP | BUY NO | $9.99 (333 × 3¢) | 47.8% | 81.7% | 98.0¢ | -16.3 pp | polymarket(75%)+ranking(#200 vs #128)(25%) | ❌ LOSS −$9.99 |
| 2 | Houston at New Orleans Winner? | NBA | BUY YES | $9.90 (30 × 33¢) | 39.6% | 48.5% | 32.5¢ | +16.0 pp | polymarket(75%)+win_pct(25%) | ❌ LOSS −$9.90 |
| 3 | Will Rei Sakamoto win the Jamji vs Sakamoto : Qualification Round 1 match? | ATP | BUY NO | $9.99 (333 × 3¢) | 50.0% | 85.4% | 98.0¢ | -12.6 pp | polymarket(75%)+ranking(#200 vs #200)(25%) | ❌ LOSS −$9.99 |
| 4 | Will Joel Schwaerzler win the Haita vs Schwaerzler : Qualification Round 1 match? | ATP | BUY NO | $9.96 (166 × 6¢) | 50.0% | 83.9% | 95.0¢ | -11.1 pp | polymarket(75%)+ranking(#200 vs #200)(25%) | ❌ LOSS −$9.96 |

**Total wagered: $39.84**  |  **Net P&L: −$39.84**

---
## 2026-03-28

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Philadelphia at Charlotte Winner? |  | BUY YES | $9.92 (31 × 32¢) | 46.6% | 67.9% | 31.5¢ | +36.4 pp | polymarket(75%)+win_pct(25%) | ✅ WIN +$21.08 |

**Total wagered: $9.92**  |  **Net P&L: +$21.08**

---
## 2026-03-27

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Houston at Memphis Winner? |  | BUY YES | $9.88 (76 × 13¢) | — | 39.8% | 12.5¢ | +27.3 pp | — | ❌ LOSS −$9.88 |
| 2 | Will Alexander Zverev win the Zverev vs Sinner : Semifinal match? |  | BUY YES | $9.92 (62 × 16¢) | — | 40.6% | 15.0¢ | +25.6 pp | — | ❌ LOSS −$9.92 |
| 3 | Chicago at Oklahoma City Winner? |  | BUY NO | $9.96 (166 × 6¢) | — | 70.0% | 94.5¢ | -24.5 pp | — | ❌ LOSS −$9.96 |
| 4 | Utah at Denver Winner? |  | BUY YES | $9.96 (166 × 6¢) | — | 27.6% | 5.5¢ | +22.1 pp | — | ❌ LOSS −$9.96 |

**Total wagered: $39.72**  |  **Net P&L: −$39.72**

---
## 2026-03-26

| # | Market | Sport | Bet | Amount | Model | Kalshi Mid | Edge | Result |
|---|--------|-------|-----|--------|-------|-----------|------|--------|
| 1 | Sacramento at Orlando Winner? | NBA | BUY YES (Sacramento wins) | $10.00 (100 × 10¢) | 29% | 9.5¢ | +19.5 pp | ❌ NO — Sacramento lost |
| 2 | Seattle at Tampa Bay Winner? | NHL | BUY NO (Tampa Bay loses) | ~$10.00 | — ¹ | 71.5¢ | — ¹ | ✅ NO — Tampa Bay lost |
| 3 | Gauff vs Muchova (WTA Semifinal) | WTA | BUY NO (Muchova loses) | ~$10.00 | — ¹ | 48.5¢ | — ¹ | ✅ NO — Gauff won |

**Total wagered: ~$30.00**

¹ Model probability and edge not captured — daily log was overwritten at midnight before these could be recorded.

---

## Notes

- **Fill status:** Orders are placed as limit orders. The bot logs `filled = 0` at placement time — actual fills depend on the Kalshi orderbook and may be partial or zero.
- **Early-season MLB (March 27, original):** The original four trades were canceled — their edges were artifacts of the 0-record clamp bug (teams with <5 games got 5%/95% model probabilities). Fixed with a `w + l >= 5` guard.
- **ATP/WTA tennis:** ESPN only exposes current rankings, not historical ones. Tennis trades carry look-ahead bias and backtest results exclude them (see `BACKTEST_SUMMARY.md`). The live bot still includes tennis markets.
- **Log persistence:** Fixed March 27 — `kalshi_trades.json` now stores all days under separate date keys and no longer resets at midnight. March 26 trade details for trades 2 & 3 are partially reconstructed from Kalshi's settled market API.
