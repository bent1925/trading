# Trade Log

All trades placed by `claude_code/kalshi_sports_bot.py`.
Prices are the limit-order ask price (YES bets) or `1 − bid` (NO bets).
Model estimates and Kalshi implied probabilities are percentages for the YES outcome.

> **Note on March 26 trades 2 & 3:** The daily log resets at midnight and was overwritten before model/edge data was saved. Kalshi mid is reconstructed from the settled market's `previous_yes_ask/bid`; model probability and exact fill price were not captured.

> **Strategy change — Apr 2 through Apr 6:** Switched from "fade Kalshi" to "trust Kalshi" with inverse sizing. See backtest notes in `BACKTEST_SUMMARY.md`.

> **Strategy change — Apr 7 onward:** Switching to cross-market arb (fade Kalshi). The model is now Polymarket's implied probability (+ 50% ESPN sportsbook odds when available). The bot only trades when a Polymarket market matches the game **and** the game starts within 3 hours of the run. Edge = `model_prob − kalshi_mid`; when Polymarket prices a side higher than Kalshi, buy that side. Sizing is proportional to the spread: $10 at 10pp, $20 at 20pp+. Runs every 3 hours; up to 10 trades per run.

---

## 2026-04-14

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Los Angeles at Seattle Winner? | NHL | BUY YES | $1.56 (4 × 39¢) | 50.9% | 50.9% | 38.5¢ | +12.4 pp | espn:win_pct | ❌ LOSS −$1.56 |
| 2 | Buffalo at Chicago Winner? | NHL | BUY YES | $0.72 (2 × 36¢) | 42.4% | 42.4% | 35.5¢ | +6.9 pp | espn:win_pct | ❌ LOSS −$0.72 |
| 3 | Winnipeg at Vegas Winner? | NHL | BUY YES | $0.76 (2 × 38¢) | 43.1% | 43.1% | 37.5¢ | +5.6 pp | espn:win_pct | ❌ LOSS −$0.76 |

**Total wagered: $3.04**  |  **Net P&L: −$3.04**

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
