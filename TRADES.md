# Trade Log

All trades placed by `claude_code/kalshi_sports_bot.py`.
Prices are the limit-order ask price (YES bets) or `1 − bid` (NO bets).
Model estimates and Kalshi implied probabilities are percentages for the YES outcome.

> **Note on March 26 trades 2 & 3:** The daily log resets at midnight and was overwritten before model/edge data was saved. Kalshi mid is reconstructed from the settled market's `previous_yes_ask/bid`; model probability and exact fill price were not captured.

> **Strategy change — Apr 2 through Apr 6:** Switched from "fade Kalshi" to "trust Kalshi" with inverse sizing. See backtest notes in `BACKTEST_SUMMARY.md`.

> **Strategy change — Apr 7 onward:** Switching to cross-market arb (fade Kalshi). The model is now Polymarket's implied probability (+ 50% ESPN sportsbook odds when available). The bot only trades when a Polymarket market matches the game **and** the game starts within 3 hours of the run. Edge = `model_prob − kalshi_mid`; when Polymarket prices a side higher than Kalshi, buy that side. Sizing is proportional to the spread: $10 at 10pp, $20 at 20pp+. Runs every 3 hours; up to 10 trades per run.

---

## Account Balance

**Current cash balance:** $34.90 (as of 2026-07-12 06:00 UTC) &nbsp;·&nbsp; **Since first log:** −$86.06

Cash balance only — does not include the value of open limit orders or unsettled positions. Showing the most recent 100 of 591 entries.

| Timestamp (UTC) | Cash Balance |
|-----------------|-------------:|
| 2026-07-12 06:00 | $34.90 |
| 2026-07-12 03:00 | $34.90 |
| 2026-07-12 00:00 | $34.90 |
| 2026-07-11 21:00 | $34.90 |
| 2026-07-11 18:00 | $34.90 |
| 2026-07-11 15:00 | $34.90 |
| 2026-07-11 12:00 | $34.90 |
| 2026-07-11 09:00 | $34.90 |
| 2026-07-11 06:00 | $34.90 |
| 2026-07-11 03:00 | $28.90 |
| 2026-07-11 00:00 | $27.92 |
| 2026-07-10 21:00 | $31.71 |
| 2026-07-10 18:00 | $31.71 |
| 2026-07-10 15:00 | $31.71 |
| 2026-07-10 12:00 | $31.71 |
| 2026-07-10 09:00 | $31.71 |
| 2026-07-10 06:00 | $31.71 |
| 2026-07-10 03:00 | $31.71 |
| 2026-07-10 00:00 | $31.71 |
| 2026-07-09 21:00 | $31.71 |
| 2026-07-09 18:00 | $31.71 |
| 2026-07-09 15:00 | $31.71 |
| 2026-07-09 12:00 | $31.71 |
| 2026-07-09 09:00 | $31.71 |
| 2026-07-09 06:00 | $31.71 |
| 2026-07-09 03:00 | $31.71 |
| 2026-07-09 00:00 | $31.71 |
| 2026-07-08 21:00 | $31.71 |
| 2026-07-08 18:00 | $31.71 |
| 2026-07-08 15:00 | $31.71 |
| 2026-07-08 12:00 | $31.71 |
| 2026-07-08 09:00 | $31.71 |
| 2026-07-08 06:00 | $31.71 |
| 2026-07-08 03:00 | $31.71 |
| 2026-07-08 00:00 | $30.71 |
| 2026-07-07 21:00 | $35.62 |
| 2026-07-07 18:00 | $35.62 |
| 2026-07-07 15:00 | $35.62 |
| 2026-07-07 12:00 | $35.62 |
| 2026-07-07 09:00 | $35.62 |
| 2026-07-07 06:00 | $35.62 |
| 2026-07-07 03:00 | $35.62 |
| 2026-07-07 00:00 | $34.62 |
| 2026-07-06 21:00 | $36.65 |
| 2026-07-06 18:00 | $36.65 |
| 2026-07-06 15:00 | $36.65 |
| 2026-07-06 12:00 | $36.65 |
| 2026-07-06 09:00 | $36.65 |
| 2026-07-06 06:00 | $36.65 |
| 2026-07-06 03:00 | $36.65 |
| 2026-07-06 00:00 | $36.65 |
| 2026-07-05 21:00 | $36.65 |
| 2026-07-05 18:00 | $36.65 |
| 2026-07-05 15:00 | $36.65 |
| 2026-07-05 12:00 | $36.65 |
| 2026-07-05 09:00 | $36.65 |
| 2026-07-05 06:00 | $36.65 |
| 2026-07-05 03:00 | $36.65 |
| 2026-07-05 00:00 | $37.07 |
| 2026-07-04 21:00 | $37.07 |
| 2026-07-04 18:00 | $39.06 |
| 2026-07-04 15:00 | $39.06 |
| 2026-07-04 12:00 | $39.06 |
| 2026-07-04 09:00 | $39.06 |
| 2026-07-04 06:00 | $39.06 |
| 2026-07-04 03:00 | $36.06 |
| 2026-07-04 00:00 | $34.26 |
| 2026-07-03 21:00 | $39.87 |
| 2026-07-03 18:00 | $39.87 |
| 2026-07-03 15:00 | $39.87 |
| 2026-07-03 12:00 | $39.87 |
| 2026-07-03 09:00 | $39.87 |
| 2026-07-03 06:00 | $39.87 |
| 2026-07-03 03:00 | $37.87 |
| 2026-07-03 00:00 | $39.37 |
| 2026-07-02 21:00 | $39.89 |
| 2026-07-02 18:00 | $39.89 |
| 2026-07-02 15:00 | $39.89 |
| 2026-07-02 12:00 | $39.89 |
| 2026-07-02 09:00 | $39.89 |
| 2026-07-02 06:00 | $39.89 |
| 2026-07-02 03:00 | $39.89 |
| 2026-07-02 00:00 | $39.89 |
| 2026-07-01 21:00 | $39.89 |
| 2026-07-01 18:00 | $39.89 |
| 2026-07-01 15:00 | $39.89 |
| 2026-07-01 12:00 | $39.89 |
| 2026-07-01 09:00 | $39.89 |
| 2026-07-01 06:00 | $39.89 |
| 2026-07-01 03:00 | $39.89 |
| 2026-07-01 00:00 | $39.89 |
| 2026-06-30 21:00 | $39.89 |
| 2026-06-30 18:00 | $39.89 |
| 2026-06-30 15:00 | $39.89 |
| 2026-06-30 12:00 | $39.89 |
| 2026-06-30 09:00 | $39.89 |
| 2026-06-30 06:00 | $39.89 |
| 2026-06-30 03:00 | $39.89 |
| 2026-06-30 00:00 | $37.86 |
| 2026-06-29 21:00 | $45.51 |

---

## 2026-07-12

No trades placed today.

---
## 2026-07-11

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Atlanta vs St. Louis Winner? | MLB | BUY YES | $1.20 (3 × 40¢) | 50.6% | 50.6% | 39.5¢ | +11.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.80 |
| 2 | Houston vs Texas Winner? | MLB | BUY YES | $1.35 (3 × 45¢) | 54.9% | 54.9% | 44.0¢ | +10.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.65 |
| 3 | Arizona vs Los Angeles D Winner? | MLB | BUY NO | $0.35 (1 × 35¢) | 61.3% | 61.3% | 65.5¢ | -4.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.65 |

**Total wagered: $2.90**  |  **Net P&L: +$4.10**

---
## 2026-07-10

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | New York Y vs Washington Winner? | MLB | BUY YES | $1.26 (3 × 42¢) | 52.1% | 52.1% | 41.5¢ | +10.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.26 |
| 2 | Boston vs New York M Winner? | MLB | BUY NO | $0.86 (2 × 43¢) | 51.2% | 51.2% | 57.5¢ | -6.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.14 |
| 3 | Seattle vs Tampa Bay Winner? | MLB | BUY YES | $0.53 (1 × 53¢) | 58.6% | 58.6% | 52.5¢ | +6.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.47 |
| 4 | Milwaukee vs Pittsburgh Winner? | MLB | BUY NO | $0.47 (1 × 47¢) | 47.8% | 47.8% | 53.5¢ | -5.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.47 |
| 5 | Cleveland vs Miami Winner? | MLB | BUY YES | $0.53 (1 × 53¢) | 56.1% | 56.1% | 52.5¢ | +3.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.53 |

**Total wagered: $3.65**  |  **Net P&L: −$0.65**

---
## 2026-07-09

No trades placed today.

---
## 2026-07-08

No trades placed today.

---
## 2026-07-07

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Boston vs Chicago WS Winner? | MLB | BUY YES | $1.88 (4 × 47¢) | 58.3% | 58.3% | 46.5¢ | +11.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.88 |
| 2 | Philadelphia vs Cincinnati Winner? | MLB | BUY NO | $1.56 (4 × 39¢) | 50.7% | 50.7% | 61.5¢ | -10.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.56 |
| 3 | Atlanta vs Pittsburgh Winner? | MLB | BUY NO | $0.86 (2 × 43¢) | 49.8% | 49.8% | 57.5¢ | -7.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.86 |
| 4 | Kansas City vs New York M Winner? | MLB | BUY NO | $0.42 (1 × 42¢) | 54.7% | 54.7% | 58.5¢ | -3.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.58 |

**Total wagered: $4.72**  |  **Net P&L: −$3.72**

---
## 2026-07-06

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | New York Y vs Tampa Bay Winner? | MLB | BUY YES | $1.44 (3 × 48¢) | 56.2% | 56.2% | 47.5¢ | +8.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.44 |
| 2 | Houston vs Washington Winner? | MLB | BUY YES | $0.52 (1 × 52¢) | 54.9% | 54.9% | 51.5¢ | +3.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.48 |

**Total wagered: $1.96**  |  **Net P&L: −$0.96**

---
## 2026-07-05

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Philadelphia vs Kansas City Winner? | MLB | BUY NO | $0.41 (1 × 41¢) | 55.2% | 55.2% | 59.5¢ | -4.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.41 |

**Total wagered: $0.41**  |  **Net P&L: −$0.41**

---
## 2026-07-04

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | San Francisco vs Colorado Winner? | MLB | BUY NO | $1.26 (3 × 42¢) | 47.4% | 47.4% | 58.5¢ | -11.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.74 |
| 2 | Toronto vs Seattle Winner? | MLB | BUY NO | $1.38 (3 × 46¢) | 43.8% | 43.8% | 54.5¢ | -10.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.38 |
| 3 | Milwaukee vs Arizona Winner? | MLB | BUY NO | $0.44 (1 × 44¢) | 52.0% | 52.0% | 56.5¢ | -4.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.44 |
| 4 | Detroit vs Texas Winner? | MLB | BUY YES | $1.92 (4 × 48¢) | 58.5% | 58.5% | 47.5¢ | +11.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.92 |

**Total wagered: $5.00**  |  **Net P&L: −$2.00**

---
## 2026-07-03

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Detroit vs Texas Winner? | MLB | BUY YES | $1.02 (2 × 51¢) | 57.7% | 57.7% | 50.5¢ | +7.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.98 |
| 2 | Los Angeles A vs Seattle Winner? | MLB | BUY NO | $1.02 (3 × 34¢) | 59.3% | 59.3% | 66.5¢ | -7.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.02 |
| 3 | San Diego vs Los Angeles D Winner? | MLB | BUY YES | $0.36 (1 × 36¢) | 38.6% | 38.6% | 35.5¢ | +3.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.36 |
| 4 | New York M vs Atlanta Winner? | MLB | BUY NO | $2.55 (5 × 51¢) | 36.7% | 36.7% | 49.5¢ | -12.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.45 |
| 5 | Minnesota vs New York Y Winner? | MLB | BUY NO | $1.02 (3 × 34¢) | 58.3% | 58.3% | 66.5¢ | -8.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.02 |
| 6 | Baltimore vs Cincinnati Winner? | MLB | BUY YES | $1.41 (3 × 47¢) | 54.6% | 54.6% | 46.5¢ | +8.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.41 |
| 7 | Pittsburgh vs Washington Winner? | MLB | BUY NO | $0.42 (1 × 42¢) | 54.9% | 54.9% | 58.5¢ | -3.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.42 |

**Total wagered: $7.80**  |  **Net P&L: −$0.80**

---
## 2026-07-02

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Chicago WS vs Cleveland Winner? | MLB | BUY NO | $0.51 (1 × 51¢) | 46.6% | 46.6% | 49.5¢ | -2.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.49 |

**Total wagered: $0.51**  |  **Net P&L: +$0.49**

---
## 2026-07-01

No trades placed today.

---
## 2026-06-30

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Los Angeles A vs Seattle Winner? | MLB | BUY NO | $1.05 (3 × 35¢) | 58.0% | 58.0% | 65.5¢ | -7.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.05 |
| 2 | Miami vs Colorado Winner? | MLB | BUY NO | $0.42 (1 × 42¢) | 53.5% | 53.5% | 58.5¢ | -5.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.42 |
| 3 | San Diego vs Chicago C Winner? | MLB | BUY YES | $0.41 (1 × 41¢) | 44.4% | 44.4% | 40.5¢ | +3.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.41 |

**Total wagered: $1.88**  |  **Net P&L: −$1.88**

---
## 2026-06-29

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Washington vs Boston Winner? | MLB | BUY YES | $1.95 (5 × 39¢) | 49.8% | 49.8% | 38.5¢ | +11.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.95 |
| 2 | Detroit vs New York Y Winner? | MLB | BUY YES | $1.68 (3 × 56¢) | 63.0% | 63.0% | 55.5¢ | +7.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.68 |
| 3 | Pittsburgh vs Philadelphia Winner? | MLB | BUY NO | $1.53 (3 × 51¢) | 42.5% | 42.5% | 49.5¢ | -7.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.53 |
| 4 | Cincinnati vs Milwaukee Winner? | MLB | BUY YES | $1.14 (2 × 57¢) | 62.5% | 62.5% | 56.5¢ | +6.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.86 |
| 5 | New York M vs Toronto Winner? | MLB | BUY YES | $1.10 (2 × 55¢) | 59.2% | 59.2% | 54.5¢ | +4.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.90 |

**Total wagered: $7.40**  |  **Net P&L: −$3.40**

---
## 2026-06-28

No trades placed today.

---
## 2026-06-27

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Los Angeles D vs San Diego Winner? | MLB | BUY YES | $1.29 (3 × 43¢) | 49.1% | 49.1% | 42.5¢ | +6.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 2 | Miami vs St. Louis Winner? | MLB | BUY YES | $0.98 (2 × 49¢) | 55.0% | 55.0% | 48.5¢ | +6.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 3 | Atlanta vs San Francisco Winner? | MLB | BUY NO | $0.53 (1 × 53¢) | 43.7% | 43.7% | 47.5¢ | -3.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 4 | Colorado vs Minnesota Winner? | MLB | BUY NO | $0.39 (1 × 39¢) | 58.3% | 58.3% | 61.5¢ | -3.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $3.19**

---
## 2026-06-26

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Chicago C vs Milwaukee Winner? | MLB | BUY NO | $1.55 (5 × 31¢) | 58.5% | 58.5% | 69.5¢ | -11.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 2 | Cincinnati vs Pittsburgh Winner? | MLB | BUY NO | $1.14 (3 × 38¢) | 56.2% | 56.2% | 62.5¢ | -6.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 3 | Kansas City vs Chicago WS Winner? | MLB | BUY NO | $1.10 (2 × 55¢) | 39.7% | 39.7% | 45.5¢ | -5.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 4 | Philadelphia vs New York M Winner? | MLB | BUY NO | $0.80 (2 × 40¢) | 54.8% | 54.8% | 60.5¢ | -5.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 5 | Seattle vs Cleveland Winner? | MLB | BUY NO | $1.00 (2 × 50¢) | 45.2% | 45.2% | 50.5¢ | -5.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $5.59**

---
## 2026-06-25

No trades placed today.

---
## 2026-06-24

No trades placed today.

---
## 2026-06-23

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Boston vs Colorado Winner? | MLB | BUY YES | $1.38 (3 × 46¢) | 52.4% | 52.4% | 45.5¢ | +6.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 2 | Atlanta vs San Diego Winner? | MLB | BUY NO | $0.50 (1 × 50¢) | 47.6% | 47.6% | 50.5¢ | -2.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 3 | Seattle vs Pittsburgh Winner? | MLB | BUY NO | $1.38 (3 × 46¢) | 47.2% | 47.2% | 54.5¢ | -7.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $3.26**

---
## 2026-06-22

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Milwaukee vs Cincinnati Winner? | MLB | BUY NO | $0.84 (2 × 42¢) | 53.3% | 53.3% | 58.5¢ | -5.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 2 | Los Angeles D vs Minnesota Winner? | MLB | BUY YES | $0.84 (2 × 42¢) | 46.4% | 46.4% | 41.5¢ | +4.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 3 | Cleveland vs Chicago WS Winner? | MLB | BUY YES | $0.50 (1 × 50¢) | 53.2% | 53.2% | 49.5¢ | +3.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 4 | Chicago C vs New York M Winner? | MLB | BUY NO | $0.46 (1 × 46¢) | 51.9% | 51.9% | 54.5¢ | -2.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 5 | Texas vs Miami Winner? | MLB | BUY NO | $0.55 (1 × 55¢) | 43.1% | 43.1% | 45.5¢ | -2.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $3.19**

---
## 2026-06-21

No trades placed today.

---
## 2026-06-20

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Boston vs Seattle Winner? | MLB | BUY YES | $2.55 (5 × 51¢) | 61.6% | 61.6% | 50.5¢ | +11.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 2 | San Diego vs Texas Winner? | MLB | BUY NO | $1.64 (4 × 41¢) | 50.4% | 50.4% | 59.5¢ | -9.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 3 | Minnesota vs Arizona Winner? | MLB | BUY YES | $0.78 (2 × 39¢) | 43.1% | 43.1% | 38.5¢ | +4.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 4 | Cleveland vs Houston Winner? | MLB | BUY NO | $0.46 (1 × 46¢) | 50.3% | 50.3% | 54.5¢ | -4.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 5 | Baltimore vs Los Angeles D Winner? | MLB | BUY NO | $0.33 (1 × 33¢) | 63.6% | 63.6% | 67.5¢ | -3.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 6 | New York M vs Philadelphia Winner? | MLB | BUY NO | $0.74 (2 × 37¢) | 58.8% | 58.8% | 63.5¢ | -4.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $6.50**

---
## 2026-06-19

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Toronto vs Chicago C Winner? | MLB | BUY NO | $0.53 (1 × 53¢) | 44.6% | 44.6% | 47.5¢ | -2.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 2 | Chicago WS vs Detroit Winner? | MLB | BUY NO | $3.15 (9 × 35¢) | 47.4% | 47.4% | 65.5¢ | -18.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 3 | Milwaukee vs Atlanta Winner? | MLB | BUY NO | $2.80 (7 × 40¢) | 45.7% | 45.7% | 60.5¢ | -14.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 4 | Cincinnati vs New York Y Winner? | MLB | BUY NO | $1.45 (5 × 29¢) | 61.6% | 61.6% | 71.5¢ | -9.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 5 | San Francisco vs Miami Winner? | MLB | BUY NO | $1.04 (2 × 52¢) | 42.7% | 42.7% | 48.5¢ | -5.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $8.97**

---
## 2026-06-18

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Minnesota vs Texas Winner? | MLB | BUY YES | $3.76 (8 × 47¢) | 54.5% | 54.5% | 46.5¢ | +8.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.76 |
| 2 | New York M vs Philadelphia Winner? | MLB | BUY YES | $1.59 (3 × 53¢) | 59.7% | 59.7% | 52.5¢ | +7.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.59 |
| 3 | St. Louis vs Kansas City Winner? | MLB | BUY YES | $1.00 (2 × 50¢) | 54.7% | 54.7% | 49.5¢ | +5.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.00 |

**Total wagered: $6.35**  |  **Net P&L: −$6.35**

---
## 2026-06-17

No trades placed today.

---
## 2026-06-16

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Los Angeles A vs Arizona Winner? | MLB | BUY NO | $2.24 (4 × 56¢) | 39.9% | 39.9% | 44.5¢ | -4.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.76 |
| 2 | Detroit vs Houston Winner? | MLB | BUY YES | $2.12 (4 × 53¢) | 57.0% | 57.0% | 52.5¢ | +4.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.12 |
| 3 | Colorado vs Chicago C Winner? | MLB | BUY YES | $1.36 (4 × 34¢) | 37.0% | 37.0% | 33.5¢ | +3.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.36 |
| 4 | Minnesota vs Texas Winner? | MLB | BUY NO | $0.84 (2 × 42¢) | 55.9% | 55.9% | 58.5¢ | -2.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.16 |
| 5 | San Francisco vs Atlanta Winner? | MLB | BUY NO | $3.66 (6 × 61¢) | 33.5% | 33.5% | 39.5¢ | -6.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.66 |
| 6 | Toronto vs Boston Winner? | MLB | BUY NO | $0.96 (2 × 48¢) | 49.9% | 49.9% | 52.5¢ | -2.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.96 |

**Total wagered: $11.18**  |  **Net P&L: −$5.18**

---
## 2026-06-15

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Miami vs Philadelphia Winner? | MLB | BUY NO | $3.33 (9 × 37¢) | 55.7% | 55.7% | 63.5¢ | -7.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.33 |
| 2 | Kansas City vs Washington Winner? | MLB | BUY YES | $2.80 (5 × 56¢) | 60.6% | 60.6% | 55.5¢ | +5.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.20 |
| 3 | San Diego vs St. Louis Winner? | MLB | BUY NO | $1.68 (4 × 42¢) | 54.8% | 54.8% | 58.5¢ | -3.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.68 |

**Total wagered: $7.81**  |  **Net P&L: −$2.81**

---
## 2026-06-14

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 5: New York at San Antonio Winner? | NBA | BUY NO | $2.52 (7 × 36¢) | 57.7% | 57.7% | 64.5¢ | -6.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.48 |

**Total wagered: $2.52**  |  **Net P&L: +$4.48**

---
## 2026-06-13

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | St. Louis vs Minnesota Winner? | MLB | BUY YES | $2.70 (6 × 45¢) | 51.9% | 51.9% | 44.5¢ | +7.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.70 |
| 2 | Chicago C vs San Francisco Winner? | MLB | BUY NO | $1.88 (4 × 47¢) | 48.8% | 48.8% | 53.5¢ | -4.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.12 |
| 3 | Tampa Bay vs Los Angeles A Winner? | MLB | BUY NO | $0.80 (2 × 40¢) | 57.8% | 57.8% | 60.5¢ | -2.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.20 |

**Total wagered: $5.38**  |  **Net P&L: +$0.62**

---
## 2026-06-12

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Atlanta vs New York M Winner? | MLB | BUY NO | $6.58 (14 × 47¢) | 40.4% | 40.4% | 53.5¢ | -13.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$6.58 |
| 2 | Philadelphia vs Milwaukee Winner? | MLB | BUY YES | $4.03 (13 × 31¢) | 40.5% | 40.5% | 30.5¢ | +10.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.03 |
| 3 | Los Angeles D vs Chicago WS Winner? | MLB | BUY NO | $4.51 (11 × 41¢) | 49.6% | 49.6% | 59.5¢ | -9.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$6.49 |
| 4 | Seattle vs Washington Winner? | MLB | BUY YES | $4.40 (10 × 44¢) | 52.9% | 52.9% | 43.5¢ | +9.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.40 |
| 5 | Detroit vs Cleveland Winner? | MLB | BUY NO | $3.78 (7 × 54¢) | 39.5% | 39.5% | 46.5¢ | -7.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.22 |

**Total wagered: $23.30**  |  **Net P&L: −$5.30**

---
## 2026-06-11

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 4: San Antonio at New York Winner? | NBA | BUY YES | $1.41 (3 × 47¢) | 49.6% | 49.6% | 46.5¢ | +3.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.41 |

**Total wagered: $1.41**  |  **Net P&L: −$1.41**

---
## 2026-06-10

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Chicago C vs Colorado Winner? | MLB | BUY YES | $1.64 (4 × 41¢) | 44.7% | 44.7% | 40.5¢ | +4.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.36 |

**Total wagered: $1.64**  |  **Net P&L: +$2.36**

---
## 2026-06-09

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Washington vs San Francisco Winner? | MLB | BUY YES | $3.01 (7 × 43¢) | 50.4% | 50.4% | 42.5¢ | +7.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.99 |
| 2 | Houston vs Los Angeles A Winner? | MLB | BUY NO | $1.38 (3 × 46¢) | 50.4% | 50.4% | 54.5¢ | -4.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 3 | Game 3: San Antonio at New York Winner? | NBA | BUY YES | $0.94 (2 × 47¢) | 49.6% | 49.6% | 46.5¢ | +3.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 4 | St. Louis vs New York M Winner? | MLB | BUY YES | $3.68 (8 × 46¢) | 53.4% | 53.4% | 45.5¢ | +7.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.32 |
| 5 | Arizona vs Miami Winner? | MLB | BUY NO | $3.01 (7 × 43¢) | 50.6% | 50.6% | 57.5¢ | -6.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 6 | Atlanta vs Chicago WS Winner? | MLB | BUY YES | $1.68 (4 × 42¢) | 45.7% | 45.7% | 41.5¢ | +4.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 7 | Los Angeles D vs Pittsburgh Winner? | MLB | BUY NO | $1.96 (4 × 49¢) | 47.6% | 47.6% | 51.5¢ | -3.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 8 | Texas vs Kansas City Winner? | MLB | BUY NO | $1.41 (3 × 47¢) | 49.9% | 49.9% | 53.5¢ | -3.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $17.07**

---
## 2026-06-08

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Boston vs Tampa Bay Winner? | MLB | BUY YES | $6.50 (13 × 50¢) | 63.3% | 63.3% | 49.5¢ | +13.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$6.50 |
| 2 | Philadelphia vs Toronto Winner? | MLB | BUY YES | $4.68 (12 × 39¢) | 51.2% | 51.2% | 38.5¢ | +12.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 3 | Seattle vs Baltimore Winner? | MLB | BUY NO | $1.88 (4 × 47¢) | 49.2% | 49.2% | 53.5¢ | -4.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $13.06**

---
## 2026-06-07

No trades placed today.

---
## 2026-06-06

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 2: New York at San Antonio Winner? | NBA | BUY NO | $2.97 (9 × 33¢) | 58.0% | 58.0% | 67.5¢ | -9.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$6.03 |
| 2 | New York M vs San Diego Winner? | MLB | BUY YES | $3.30 (6 × 55¢) | 61.2% | 61.2% | 54.5¢ | +6.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 3 | Los Angeles A vs Los Angeles D Winner? | MLB | BUY YES | $1.30 (2 × 65¢) | 67.0% | 67.0% | 64.5¢ | +2.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 4 | Cincinnati vs St. Louis Winner? | MLB | BUY NO | $0.43 (1 × 43¢) | 55.4% | 55.4% | 57.5¢ | -2.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $8.00**

---
## 2026-06-05

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Chicago WS vs Philadelphia Winner? | MLB | BUY NO | $3.04 (8 × 38¢) | 53.9% | 53.9% | 62.5¢ | -8.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.04 |
| 2 | Boston vs New York Y Winner? | MLB | BUY YES | $3.99 (7 × 57¢) | 64.0% | 64.0% | 56.5¢ | +7.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 3 | Baltimore vs Toronto Winner? | MLB | BUY NO | $1.29 (3 × 43¢) | 54.1% | 54.1% | 57.5¢ | -3.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 4 | Pittsburgh vs Atlanta Winner? | MLB | BUY NO | $1.74 (3 × 58¢) | 39.2% | 39.2% | 42.5¢ | -3.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 5 | Tampa Bay vs Miami Winner? | MLB | BUY NO | $0.88 (2 × 44¢) | 54.2% | 54.2% | 56.5¢ | -2.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $10.94**

---
## 2026-06-04

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 1: New York at San Antonio Winner? | NBA | BUY NO | $1.85 (5 × 37¢) | 58.0% | 58.0% | 63.5¢ | -5.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.15 |
| 2 | Kansas City vs Minnesota Winner? | MLB | BUY YES | $4.90 (10 × 49¢) | 59.2% | 59.2% | 48.5¢ | +10.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.90 |

**Total wagered: $6.75**  |  **Net P&L: −$1.75**

---
## 2026-06-03

No trades placed today.

---
## 2026-06-02

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Los Angeles D vs Arizona Winner? | MLB | BUY NO | $2.40 (6 × 40¢) | 51.3% | 51.3% | 60.5¢ | -9.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.60 |
| 2 | Colorado vs Los Angeles A Winner? | MLB | BUY NO | $2.16 (6 × 36¢) | 56.3% | 56.3% | 64.5¢ | -8.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.84 |
| 3 | New York M vs Seattle Winner? | MLB | BUY YES | $2.20 (4 × 55¢) | 61.1% | 61.1% | 54.5¢ | +6.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 4 | Toronto vs Atlanta Winner? | MLB | BUY NO | $4.77 (9 × 53¢) | 36.0% | 36.0% | 47.5¢ | -11.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.23 |
| 5 | Cleveland vs New York Y Winner? | MLB | BUY NO | $3.30 (10 × 33¢) | 56.3% | 56.3% | 67.5¢ | -11.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$6.70 |
| 6 | San Diego vs Philadelphia Winner? | MLB | BUY YES | $2.15 (5 × 43¢) | 48.9% | 48.9% | 42.5¢ | +6.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 7 | Baltimore vs Boston Winner? | MLB | BUY NO | $1.35 (3 × 45¢) | 51.9% | 51.9% | 55.5¢ | -3.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $18.33**

---
## 2026-06-01

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Texas vs St. Louis Winner? | MLB | BUY NO | $4.23 (9 × 47¢) | 41.3% | 41.3% | 53.5¢ | -12.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.23 |
| 2 | San Francisco vs Milwaukee Winner? | MLB | BUY NO | $4.06 (7 × 58¢) | 33.5% | 33.5% | 42.5¢ | -9.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.94 |
| 3 | Detroit vs Tampa Bay Winner? | MLB | BUY YES | $3.66 (6 × 61¢) | 68.8% | 68.8% | 60.5¢ | +8.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 4 | Kansas City vs Cincinnati Winner? | MLB | BUY NO | $2.80 (5 × 56¢) | 37.3% | 37.3% | 44.5¢ | -7.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |
| 5 | Chicago WS vs Minnesota Winner? | MLB | BUY NO | $2.20 (5 × 44¢) | 49.5% | 49.5% | 56.5¢ | -7.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | pending |

**Total wagered: $16.95**

---
## 2026-05-31

No trades placed today.

---
## 2026-05-30

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Philadelphia vs Los Angeles D Winner? | MLB | BUY NO | $2.08 (4 × 52¢) | 39.2% | 39.2% | 48.5¢ | -9.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.92 |
| 2 | San Francisco vs Colorado Winner? | MLB | BUY NO | $1.72 (4 × 43¢) | 49.7% | 49.7% | 57.5¢ | -7.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.28 |
| 3 | Arizona vs Seattle Winner? | MLB | BUY NO | $0.88 (2 × 44¢) | 51.1% | 51.1% | 56.5¢ | -5.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.88 |
| 4 | Kansas City vs Texas Winner? | MLB | BUY YES | $0.54 (1 × 54¢) | 56.7% | 56.7% | 53.5¢ | +3.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.46 |
| 5 | Game 7: San Antonio at Oklahoma City Winner? | NBA | BUY YES | $1.29 (3 × 43¢) | 46.4% | 46.4% | 42.5¢ | +3.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.71 |

**Total wagered: $6.51**  |  **Net P&L: +$5.49**

---
## 2026-05-29

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 6: Oklahoma City at San Antonio Winner? | NBA | BUY NO | $1.23 (3 × 41¢) | 54.9% | 54.9% | 59.5¢ | -4.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.23 |
| 2 | Game 5: Montreal at Carolina Winner? | NHL | BUY YES | $3.10 (10 × 31¢) | 43.5% | 43.5% | 30.5¢ | +13.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.10 |
| 3 | Detroit vs Chicago WS Winner? | MLB | BUY NO | $4.00 (8 × 50¢) | 38.4% | 38.4% | 50.5¢ | -12.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.00 |
| 4 | Boston vs Cleveland Winner? | MLB | BUY YES | $2.75 (5 × 55¢) | 63.2% | 63.2% | 54.5¢ | +8.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.25 |
| 5 | Chicago C vs St. Louis Winner? | MLB | BUY YES | $2.30 (5 × 46¢) | 53.3% | 53.3% | 45.5¢ | +7.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.70 |
| 6 | Los Angeles A vs Tampa Bay Winner? | MLB | BUY YES | $2.40 (4 × 60¢) | 66.3% | 66.3% | 59.5¢ | +6.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.60 |

**Total wagered: $15.78**  |  **Net P&L: +$6.22**

---
## 2026-05-28

No trades placed today.

---
## 2026-05-27

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 5: San Antonio at Oklahoma City Winner? | NBA | BUY YES | $1.26 (3 × 42¢) | 46.4% | 46.4% | 41.5¢ | +4.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.26 |
| 2 | Game 4: Colorado at Vegas Winner? | NHL | BUY NO | $0.51 (1 × 51¢) | 47.1% | 47.1% | 49.5¢ | -2.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.51 |
| 3 | Game 4: Carolina at Montreal Winner? | NHL | BUY YES | $2.58 (6 × 43¢) | 51.6% | 51.6% | 42.5¢ | +9.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.58 |

**Total wagered: $4.35**  |  **Net P&L: −$4.35**

---
## 2026-05-26

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Colorado vs Los Angeles D Winner? | MLB | BUY NO | $1.30 (5 × 26¢) | 68.4% | 68.4% | 74.5¢ | -6.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.30 |
| 2 | Atlanta vs Boston Winner? | MLB | BUY NO | $3.00 (6 × 50¢) | 40.9% | 40.9% | 50.5¢ | -9.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.00 |

**Total wagered: $4.30**  |  **Net P&L: +$1.70**

---
## 2026-05-25

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Tampa Bay vs Baltimore Winner? | MLB | BUY YES | $2.12 (4 × 53¢) | 58.1% | 58.1% | 52.5¢ | +5.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.12 |
| 2 | Chicago C vs Pittsburgh Winner? | MLB | BUY YES | $1.88 (4 × 47¢) | 51.9% | 51.9% | 46.5¢ | +5.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.12 |
| 3 | Cincinnati vs New York M Winner? | MLB | BUY NO | $3.01 (7 × 43¢) | 46.5% | 46.5% | 57.5¢ | -11.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.99 |
| 4 | St. Louis vs Milwaukee Winner? | MLB | BUY YES | $2.38 (7 × 34¢) | 43.6% | 43.6% | 33.5¢ | +10.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.38 |
| 5 | Minnesota vs Chicago WS Winner? | MLB | BUY NO | $1.02 (2 × 51¢) | 45.3% | 45.3% | 49.5¢ | -4.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.98 |
| 6 | Philadelphia vs San Diego Winner? | MLB | BUY YES | $3.43 (7 × 49¢) | 59.9% | 59.9% | 48.5¢ | +11.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.43 |
| 7 | Game 3: Carolina at Montreal Winner? | NHL | BUY YES | $2.20 (5 × 44¢) | 51.6% | 51.6% | 43.5¢ | +8.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.20 |
| 8 | Game 4: New York at Cleveland Winner? | NBA | BUY NO | $2.30 (5 × 46¢) | 46.5% | 46.5% | 54.5¢ | -8.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.30 |
| 9 | Arizona vs San Francisco Winner? | MLB | BUY NO | $1.84 (4 × 46¢) | 48.0% | 48.0% | 54.5¢ | -6.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.16 |
| 10 | Miami vs Toronto Winner? | MLB | BUY NO | $1.23 (3 × 41¢) | 55.0% | 55.0% | 59.5¢ | -4.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.77 |

**Total wagered: $21.41**  |  **Net P&L: −$1.41**

---
## 2026-05-24

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 3: Colorado at Vegas Winner? | NHL | BUY YES | $1.29 (3 × 43¢) | 46.9% | 46.9% | 42.5¢ | +4.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.71 |
| 2 | Game 4: Oklahoma City at San Antonio Winner? | NBA | BUY NO | $0.86 (2 × 43¢) | 54.3% | 54.3% | 57.5¢ | -3.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.86 |

**Total wagered: $2.15**  |  **Net P&L: +$0.85**

---
## 2026-05-23

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Texas vs Los Angeles A Winner? | MLB | BUY NO | $1.20 (3 × 40¢) | 54.2% | 54.2% | 60.5¢ | -6.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.80 |
| 2 | Game 3: Oklahoma City at San Antonio Winner? | NBA | BUY NO | $0.86 (2 × 43¢) | 54.0% | 54.0% | 57.5¢ | -3.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.14 |
| 3 | Game 2: Montreal at Carolina Winner? | NHL | BUY YES | $2.45 (7 × 35¢) | 43.5% | 43.5% | 34.5¢ | +9.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.45 |
| 4 | Game 3: New York at Cleveland Winner? | NBA | BUY YES | $0.45 (1 × 45¢) | 46.5% | 46.5% | 44.5¢ | +2.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.55 |

**Total wagered: $4.96**  |  **Net P&L: +$1.04**

---
## 2026-05-22

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Colorado vs Arizona Winner? | MLB | BUY YES | $0.70 (2 × 35¢) | 37.9% | 37.9% | 34.5¢ | +3.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.70 |
| 2 | Houston vs Chicago C Winner? | MLB | BUY NO | $2.85 (5 × 57¢) | 36.1% | 36.1% | 43.5¢ | -7.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.85 |
| 3 | Cleveland vs Philadelphia Winner? | MLB | BUY NO | $3.12 (8 × 39¢) | 49.1% | 49.1% | 61.5¢ | -12.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.88 |
| 4 | Pittsburgh vs Toronto Winner? | MLB | BUY NO | $2.46 (6 × 41¢) | 50.7% | 50.7% | 59.5¢ | -8.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.46 |
| 5 | Tampa Bay vs New York Y Winner? | MLB | BUY YES | $1.32 (3 × 44¢) | 48.9% | 48.9% | 43.5¢ | +5.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.68 |
| 6 | Minnesota vs Boston Winner? | MLB | BUY YES | $0.86 (2 × 43¢) | 46.5% | 46.5% | 42.5¢ | +4.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.14 |
| 7 | New York M vs Miami Winner? | MLB | BUY NO | $1.04 (2 × 52¢) | 45.2% | 45.2% | 48.5¢ | -3.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.96 |

**Total wagered: $12.35**  |  **Net P&L: +$2.65**

---
## 2026-05-21

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 2: San Antonio at Oklahoma City Winner? | NBA | BUY YES | $3.20 (10 × 32¢) | 44.1% | 44.1% | 31.5¢ | +12.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.20 |
| 2 | Game 2: Cleveland at New York Winner? | NBA | BUY NO | $2.52 (7 × 36¢) | 54.5% | 54.5% | 64.5¢ | -10.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.52 |
| 3 | Game 1: Montreal at Carolina Winner? | NHL | BUY YES | $2.10 (6 × 35¢) | 43.5% | 43.5% | 34.5¢ | +9.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.90 |

**Total wagered: $7.82**  |  **Net P&L: −$1.82**

---
## 2026-05-20

No trades placed today.

---
## 2026-05-19

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 1: San Antonio at Oklahoma City Winner? | NBA | BUY YES | $2.48 (8 × 31¢) | 44.1% | 44.1% | 30.5¢ | +13.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$5.52 |
| 2 | Los Angeles D vs San Diego Winner? | MLB | BUY YES | $2.20 (5 × 44¢) | 52.7% | 52.7% | 43.5¢ | +9.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.80 |
| 3 | Chicago WS vs Seattle Winner? | MLB | BUY NO | $1.64 (4 × 41¢) | 51.3% | 51.3% | 59.5¢ | -8.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.64 |
| 4 | Texas vs Colorado Winner? | MLB | BUY NO | $1.29 (3 × 43¢) | 50.9% | 50.9% | 57.5¢ | -6.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.71 |
| 5 | Game 1: Cleveland at New York Winner? | NBA | BUY NO | $3.84 (12 × 32¢) | 54.1% | 54.1% | 68.5¢ | -14.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.84 |
| 6 | Pittsburgh vs St. Louis Winner? | MLB | BUY YES | $2.08 (4 × 52¢) | 57.6% | 57.6% | 51.5¢ | +6.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.92 |

**Total wagered: $13.53**  |  **Net P&L: +$6.47**

---
## 2026-05-18

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | New York M vs Washington Winner? | MLB | BUY YES | $3.76 (8 × 47¢) | 58.5% | 58.5% | 46.5¢ | +12.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.76 |
| 2 | Cleveland vs Detroit Winner? | MLB | BUY NO | $3.01 (7 × 43¢) | 47.3% | 47.3% | 57.5¢ | -10.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.99 |
| 3 | Atlanta vs Miami Winner? | MLB | BUY NO | $3.00 (6 × 50¢) | 42.1% | 42.1% | 50.5¢ | -8.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.00 |
| 4 | Baltimore vs Tampa Bay Winner? | MLB | BUY YES | $2.90 (5 × 58¢) | 64.9% | 64.9% | 57.5¢ | +7.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.10 |
| 5 | Boston vs Kansas City Winner? | MLB | BUY YES | $2.00 (4 × 50¢) | 55.8% | 55.8% | 49.5¢ | +6.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.00 |

**Total wagered: $14.67**  |  **Net P&L: −$2.67**

---
## 2026-05-17

No trades placed today.

---
## 2026-05-16

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Los Angeles D vs Los Angeles A Winner? | MLB | BUY NO | $3.96 (11 × 36¢) | 41.3% | 41.3% | 64.5¢ | -23.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.96 |
| 2 | Game 6: San Antonio at Minnesota Winner? | NBA | BUY NO | $2.31 (7 × 33¢) | 52.8% | 52.8% | 67.5¢ | -14.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.31 |
| 3 | Kansas City vs St. Louis Winner? | MLB | BUY YES | $2.55 (5 × 51¢) | 61.9% | 61.9% | 50.5¢ | +11.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.45 |
| 4 | San Diego vs Seattle Winner? | MLB | BUY NO | $0.46 (1 × 46¢) | 50.1% | 50.1% | 54.5¢ | -4.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.54 |
| 5 | Arizona vs Colorado Winner? | MLB | BUY YES | $0.48 (1 × 48¢) | 50.2% | 50.2% | 47.5¢ | +2.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.48 |
| 6 | Game 6: Buffalo at Montreal Winner? | NHL | BUY NO | $1.56 (4 × 39¢) | 55.0% | 55.0% | 61.5¢ | -6.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.44 |

**Total wagered: $11.32**  |  **Net P&L: −$1.32**

---
## 2026-05-15

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | New York Y vs New York M Winner? | MLB | BUY NO | $13.86 (33 × 42¢) | 41.1% | 14.1% | 58.5¢ | -44.4 pp | Fade Kalshi → Polymarket | ❌ LOSS −$13.86 |
| 2 | Miami vs Tampa Bay Winner? | MLB | BUY YES | $4.24 (8 × 53¢) | 64.1% | 64.1% | 52.5¢ | +11.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.76 |
| 3 | Baltimore vs Washington Winner? | MLB | BUY YES | $3.15 (7 × 45¢) | 55.0% | 55.0% | 44.5¢ | +10.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.85 |
| 4 | Boston vs Atlanta Winner? | MLB | BUY NO | $4.13 (7 × 59¢) | 31.6% | 31.6% | 41.5¢ | -9.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.87 |
| 5 | Game 6: Detroit at Cleveland Winner? | NBA | BUY YES | $2.80 (7 × 40¢) | 49.2% | 49.2% | 39.5¢ | +9.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.20 |

**Total wagered: $28.18**  |  **Net P&L: +$0.82**

---
## 2026-05-14

No trades placed today.

---
## 2026-05-13

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 5: Minnesota at Colorado Winner? | NHL | BUY YES | $2.04 (6 × 34¢) | 41.3% | 41.3% | 33.5¢ | +7.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.04 |
| 2 | Game 5: Cleveland at Detroit Winner? | NBA | BUY NO | $1.17 (3 × 39¢) | 56.9% | 56.9% | 61.5¢ | -4.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.83 |

**Total wagered: $3.21**  |  **Net P&L: −$0.21**

---
## 2026-05-12

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 4: Oklahoma City at Los Angeles L Winner? | NBA | BUY NO | $1.98 (11 × 18¢) | 50.5% | 50.5% | 82.5¢ | -32.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.98 |
| 2 | Seattle vs Houston Winner? | MLB | BUY NO | $0.43 (1 × 43¢) | 51.1% | 51.1% | 57.5¢ | -6.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.43 |
| 3 | Game 5: Minnesota at San Antonio Winner? | NBA | BUY NO | $4.62 (21 × 22¢) | 60.4% | 60.4% | 78.5¢ | -18.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.62 |
| 4 | Detroit vs New York M Winner? | MLB | BUY NO | $3.87 (9 × 43¢) | 45.9% | 45.9% | 57.5¢ | -11.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.87 |
| 5 | Colorado vs Pittsburgh Winner? | MLB | BUY NO | $2.61 (9 × 29¢) | 62.4% | 62.4% | 71.5¢ | -9.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.61 |
| 6 | Philadelphia vs Boston Winner? | MLB | BUY NO | $2.64 (6 × 44¢) | 48.2% | 48.2% | 56.5¢ | -8.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.64 |
| 7 | Kansas City vs Chicago WS Winner? | MLB | BUY NO | $2.82 (6 × 47¢) | 45.4% | 45.4% | 53.5¢ | -8.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.18 |

**Total wagered: $18.97**  |  **Net P&L: −$12.97**

---
## 2026-05-11

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Tampa Bay vs Toronto Winner? | MLB | BUY NO | $1.88 (4 × 47¢) | 44.1% | 44.1% | 53.5¢ | -9.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.12 |
| 2 | Game 4: Detroit at Cleveland Winner? | NBA | BUY YES | $1.64 (4 × 41¢) | 49.2% | 49.2% | 40.5¢ | +8.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.64 |
| 3 | Game 4: Colorado at Minnesota Winner? | NHL | BUY YES | $0.44 (1 × 44¢) | 47.1% | 47.1% | 43.5¢ | +3.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.44 |
| 4 | New York Y vs Baltimore Winner? | MLB | BUY NO | $0.42 (1 × 42¢) | 56.3% | 56.3% | 58.5¢ | -2.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.58 |

**Total wagered: $4.38**  |  **Net P&L: +$0.62**

---
## 2026-05-10

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 3: Oklahoma City at Los Angeles L Winner? | NBA | BUY NO | $5.75 (23 × 25¢) | 50.5% | 50.5% | 75.5¢ | -25.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$5.75 |
| 2 | Game 3: Colorado at Minnesota Winner? | NHL | BUY YES | $0.90 (2 × 45¢) | 48.1% | 48.1% | 44.5¢ | +3.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.10 |
| 3 | Game 4: New York at Philadelphia Winner? | NBA | BUY YES | $0.47 (1 × 47¢) | 49.5% | 49.5% | 46.5¢ | +3.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.47 |
| 4 | Game 4: San Antonio at Minnesota Winner? | NBA | BUY NO | $2.88 (8 × 36¢) | 52.5% | 52.5% | 64.5¢ | -12.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$5.12 |

**Total wagered: $10.00**  |  **Net P&L: +$0.00**

---
## 2026-05-09

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | New York M vs Arizona Winner? | MLB | BUY NO | $4.70 (10 × 47¢) | 39.1% | 39.1% | 53.5¢ | -14.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.70 |
| 2 | Game 3: San Antonio at Minnesota Winner? | NBA | BUY NO | $3.40 (10 × 34¢) | 52.8% | 52.8% | 66.5¢ | -13.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.40 |
| 3 | Pittsburgh vs San Francisco Winner? | MLB | BUY NO | $2.00 (4 × 50¢) | 44.8% | 44.8% | 50.5¢ | -5.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.00 |
| 4 | Chicago C vs Texas Winner? | MLB | BUY NO | $1.10 (2 × 55¢) | 41.9% | 41.9% | 45.5¢ | -3.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$0.90 |
| 5 | Game 3: Vegas at Anaheim Winner? | NHL | BUY NO | $0.50 (1 × 50¢) | 48.0% | 48.0% | 50.5¢ | -2.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.50 |
| 6 | Game 3: Detroit at Cleveland Winner? | NBA | BUY YES | $3.12 (8 × 39¢) | 49.4% | 49.4% | 38.5¢ | +10.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.12 |
| 7 | Game 4: Carolina at Philadelphia Winner? | NHL | BUY YES | $3.24 (9 × 36¢) | 47.4% | 47.4% | 35.5¢ | +11.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.24 |

**Total wagered: $18.06**  |  **Net P&L: −$16.06**

---
## 2026-05-08

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 2: Los Angeles L at Oklahoma City Winner? | NBA | BUY NO | $6.50 (50 × 13¢) | 59.8% | 59.8% | 87.5¢ | -27.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$6.50 |
| 2 | St. Louis vs San Diego Winner? | MLB | BUY YES | $1.23 (3 × 41¢) | 44.2% | 44.2% | 40.5¢ | +3.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.77 |
| 3 | Colorado vs Philadelphia Winner? | MLB | BUY NO | $3.06 (9 × 34¢) | 56.9% | 56.9% | 66.5¢ | -9.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$5.94 |
| 4 | Seattle vs Chicago WS Winner? | MLB | BUY NO | $2.70 (6 × 45¢) | 47.5% | 47.5% | 55.5¢ | -8.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.70 |
| 5 | Houston vs Cincinnati Winner? | MLB | BUY NO | $2.75 (5 × 55¢) | 38.6% | 38.6% | 45.5¢ | -6.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.75 |
| 6 | Game 3: New York at Philadelphia Winner? | NBA | BUY NO | $2.20 (5 × 44¢) | 50.0% | 50.0% | 56.5¢ | -6.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$2.80 |
| 7 | Detroit vs Kansas City Winner? | MLB | BUY NO | $1.32 (3 × 44¢) | 52.0% | 52.0% | 56.5¢ | -4.5 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.32 |

**Total wagered: $19.76**  |  **Net P&L: −$2.76**

---
## 2026-05-07

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 2: Minnesota at San Antonio Winner? | NBA | BUY NO | $5.06 (22 × 23¢) | 60.9% | 60.9% | 77.5¢ | -16.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$5.06 |
| 2 | Game 2: Anaheim at Vegas Winner? | NHL | BUY NO | $1.23 (3 × 41¢) | 56.1% | 56.1% | 59.5¢ | -3.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.77 |
| 3 | Tampa Bay vs Boston Winner? | MLB | BUY YES | $3.50 (7 × 50¢) | 58.2% | 58.2% | 49.5¢ | +8.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.50 |
| 4 | Game 3: Carolina at Philadelphia Winner? | NHL | BUY YES | $2.80 (7 × 40¢) | 47.4% | 47.4% | 39.5¢ | +7.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.80 |
| 5 | Game 2: Cleveland at Detroit Winner? | NBA | BUY NO | $0.80 (2 × 40¢) | 57.6% | 57.6% | 60.5¢ | -2.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.80 |

**Total wagered: $13.39**  |  **Net P&L: −$3.39**

---
## 2026-05-06

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 1: Los Angeles L at Oklahoma City Winner? | NBA | BUY NO | $7.50 (50 × 15¢) | 58.9% | 58.9% | 85.5¢ | -26.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$7.50 |
| 2 | Pittsburgh vs Arizona Winner? | MLB | BUY YES | $2.25 (5 × 45¢) | 50.3% | 50.3% | 44.5¢ | +5.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.25 |
| 3 | Game 2: Philadelphia at New York Winner? | NBA | BUY YES | $6.30 (30 × 21¢) | 40.7% | 40.7% | 20.5¢ | +20.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$6.30 |

**Total wagered: $16.05**  |  **Net P&L: −$16.05**

---
## 2026-05-05

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 1: Minnesota at San Antonio Winner? | NBA | BUY NO | $4.37 (19 × 23¢) | 62.1% | 62.1% | 77.5¢ | -15.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$14.63 |
| 2 | Atlanta vs Seattle Winner? | MLB | BUY NO | $5.40 (12 × 45¢) | 41.9% | 41.9% | 55.5¢ | -13.6 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$5.40 |
| 3 | Chicago WS vs Los Angeles A Winner? | MLB | BUY NO | $3.78 (9 × 42¢) | 48.5% | 48.5% | 58.5¢ | -10.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$5.22 |
| 4 | Los Angeles D vs Houston Winner? | MLB | BUY NO | $2.16 (6 × 36¢) | 57.8% | 57.8% | 64.5¢ | -6.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$2.16 |
| 5 | Game 1: Anaheim at Vegas Winner? | NHL | BUY NO | $1.95 (5 × 39¢) | 55.6% | 55.6% | 61.5¢ | -5.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.95 |
| 6 | Texas vs New York Y Winner? | MLB | BUY NO | $7.56 (14 × 54¢) | 33.8% | 33.8% | 46.5¢ | -12.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$6.44 |
| 7 | Minnesota vs Washington Winner? | MLB | BUY YES | $3.00 (6 × 50¢) | 55.4% | 55.4% | 49.5¢ | +5.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.00 |
| 8 | Game 2: Minnesota at Colorado Winner? | NHL | BUY YES | $1.44 (4 × 36¢) | 39.6% | 39.6% | 35.5¢ | +4.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.44 |
| 9 | Game 1: Cleveland at Detroit Winner? | NBA | BUY NO | $0.82 (2 × 41¢) | 57.3% | 57.3% | 59.5¢ | -2.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$0.82 |

**Total wagered: $30.48**  |  **Net P&L: +$11.52**

---
## 2026-05-04

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | New York M vs Colorado Winner? | MLB | BUY NO | $8.80 (20 × 44¢) | 40.3% | 40.3% | 56.5¢ | -16.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$8.80 |
| 2 | Boston vs Detroit Winner? | MLB | BUY YES | $8.64 (18 × 48¢) | 62.8% | 62.8% | 47.5¢ | +15.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$8.64 |
| 3 | Game 1: Philadelphia at New York Winner? | NBA | BUY YES | $5.10 (17 × 30¢) | 41.5% | 41.5% | 29.5¢ | +12.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$5.10 |
| 4 | Game 2: Philadelphia at Carolina Winner? | NHL | BUY YES | $4.03 (13 × 31¢) | 40.0% | 40.0% | 30.5¢ | +9.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.03 |
| 5 | Toronto vs Tampa Bay Winner? | MLB | BUY NO | $5.94 (11 × 54¢) | 37.5% | 37.5% | 46.5¢ | -8.9 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$5.06 |

**Total wagered: $32.51**  |  **Net P&L: −$21.51**

---
## 2026-05-03

No trades placed today.

---
## 2026-05-02

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | New York M vs Los Angeles A Winner? | MLB | BUY NO | $6.37 (13 × 49¢) | 39.2% | 39.2% | 51.5¢ | -12.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$6.37 |
| 2 | Los Angeles D vs St. Louis Winner? | MLB | BUY YES | $4.40 (11 × 40¢) | 49.9% | 49.9% | 39.5¢ | +10.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$6.60 |
| 3 | Game 6: Los Angeles L at Houston Winner? | NBA | BUY YES | $3.28 (8 × 41¢) | 47.9% | 47.9% | 40.5¢ | +7.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$4.72 |
| 4 | Chicago WS vs San Diego Winner? | MLB | BUY YES | $3.48 (6 × 58¢) | 63.6% | 63.6% | 57.5¢ | +6.1 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$3.48 |
| 5 | Atlanta vs Colorado Winner? | MLB | BUY YES | $1.52 (4 × 38¢) | 41.5% | 41.5% | 37.5¢ | +4.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$1.52 |
| 6 | Game 1: Philadelphia at Carolina Winner? | NHL | BUY YES | $4.16 (13 × 32¢) | 40.5% | 40.5% | 31.5¢ | +9.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.16 |

**Total wagered: $23.21**  |  **Net P&L: −$4.21**

---
## 2026-05-01

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Strategy | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|----------|--------|
| 1 | Game 6: Denver at Minnesota Winner? | NBA | BUY YES | $6.67 (23 × 29¢) | 49.8% | 49.8% | 28.5¢ | +21.3 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$16.33 |
| 2 | Game 6: Edmonton at Anaheim Winner? | NHL | BUY NO | $3.22 (7 × 46¢) | 46.7% | 46.7% | 54.5¢ | -7.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$3.78 |
| 3 | Arizona vs Chicago C Winner? | MLB | BUY YES | $1.74 (3 × 58¢) | 60.2% | 60.2% | 57.5¢ | +2.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$1.26 |
| 4 | Game 6: Cleveland at Toronto Winner? | NBA | BUY YES | $6.84 (19 × 36¢) | 48.9% | 48.9% | 35.5¢ | +13.4 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ✅ WIN +$12.16 |
| 5 | Philadelphia vs Miami Winner? | MLB | BUY NO | $8.00 (16 × 50¢) | 38.5% | 38.5% | 50.5¢ | -12.0 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$8.00 |
| 6 | Milwaukee vs Washington Winner? | MLB | BUY YES | $4.20 (10 × 42¢) | 48.7% | 48.7% | 41.5¢ | +7.2 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.20 |
| 7 | Cincinnati vs Pittsburgh Winner? | MLB | BUY NO | $4.14 (9 × 46¢) | 47.7% | 47.7% | 54.5¢ | -6.8 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.14 |
| 8 | Game 6: Tampa Bay at Montreal Winner? | NHL | BUY NO | $4.41 (9 × 49¢) | 44.8% | 44.8% | 51.5¢ | -6.7 pp | Fade Kalshi → ESPN season win-rate (weakest fallback) | ❌ LOSS −$4.41 |

**Total wagered: $39.22**  |  **Net P&L: +$12.78**

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
