# Trade Log

All trades placed by `claude_code/kalshi_sports_bot.py`.
Prices are the limit-order ask price (YES bets) or `1 − bid` (NO bets).
Model estimates and Kalshi implied probabilities are percentages for the YES outcome.

> **Note on March 26 trades 2 & 3:** The daily log resets at midnight and was overwritten before model/edge data was saved. Kalshi mid is reconstructed from the settled market's `previous_yes_ask/bid`; model probability and exact fill price were not captured.

---

## 2026-03-30

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Will Alex Molcan win the Molcan vs Clarke : Qualification Final match? | ATP | BUY NO | $9.90 (33 × 30¢) | 50.0% | 50.0% | 71.0¢ | -21.0 pp | espn:ranking(#200 vs #200) | pending |
| 2 | Washington at Los Angeles L Winner? | NBA | BUY YES | $9.99 (111 × 9¢) | 22.1% | 25.8% | 8.5¢ | +17.3 pp | polymarket(75%)+win_pct(25%) | pending |
| 3 | Will Rei Sakamoto win the Trungelliti vs Sakamoto : Qualification Final match? | ATP | BUY YES | $9.88 (38 × 26¢) | 47.4% | 37.3% | 25.5¢ | +11.8 pp | polymarket(75%)+ranking(#200 vs #117)(25%) | pending |

**Total wagered: $29.77**

---
## 2026-03-29

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Source | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|--------|
| 1 | Will Timofey Skatov win the Pellegrino vs Skatov : Qualification Round 1 match? | ATP | BUY NO | $9.99 (333 × 3¢) | 47.8% | 81.7% | 98.0¢ | -16.3 pp | polymarket(75%)+ranking(#200 vs #128)(25%) | pending |
| 2 | Houston at New Orleans Winner? | NBA | BUY YES | $9.90 (30 × 33¢) | 39.6% | 48.5% | 32.5¢ | +16.0 pp | polymarket(75%)+win_pct(25%) | pending |
| 3 | Will Rei Sakamoto win the Jamji vs Sakamoto : Qualification Round 1 match? | ATP | BUY NO | $9.99 (333 × 3¢) | 50.0% | 85.4% | 98.0¢ | -12.6 pp | polymarket(75%)+ranking(#200 vs #200)(25%) | pending |
| 4 | Will Joel Schwaerzler win the Haita vs Schwaerzler : Qualification Round 1 match? | ATP | BUY NO | $9.96 (166 × 6¢) | 50.0% | 83.9% | 95.0¢ | -11.1 pp | polymarket(75%)+ranking(#200 vs #200)(25%) | pending |

**Total wagered: $39.84**

---
## 2026-03-28

> **Polymarket mismatch — trade 1:** Polymarket matched "Philadelphia 76ers" to an MLS soccer market (*Charlotte FC vs. Philadelphia Union — will it end in a draw?*) due to overlapping city names. The blended model probability (67.9%) is inflated by this bad match. The raw ESPN-only estimate was 46.6%, which still clears the 10pp threshold on its own (edge ≈ +15pp). The trade direction is unchanged but the stated edge is overstated. A sport-filtering fix is needed in `PolymarketSource`.

| # | Market | Sport | Bet | Amount | ESPN | Model (blended) | Kalshi Mid | Edge | Result |
|---|--------|-------|-----|--------|------|-----------------|-----------|------|--------|
| 1 | Philadelphia at Charlotte Winner? | NBA | BUY YES (76ers win) | $9.92 (31 × 32¢) | 46.6% | 67.9% ⚠️ | 31.5¢ | +36.4 pp* | pending |

*Edge overstated due to Polymarket sport mismatch; ESPN-only edge ≈ +15.1 pp.

**Total wagered: $9.92**

---

## 2026-03-27

The original four MLB trades (placed with the early-season 0-record clamp bug) were **cancelled** and replaced with the four trades below. The model now requires ≥5 games before computing a win-rate; teams with fewer games are skipped.

> **Note on trade 2 (ATP):** The live bot still includes ATP tennis. Like WTA, ESPN's rankings are current-only — this trade carries the same look-ahead bias caveat as the March 26 WTA trade.

| # | Market | Sport | Bet | Amount | Model | Kalshi Mid | Edge | Result |
|---|--------|-------|-----|--------|-------|-----------|------|--------|
| 1 | Houston at Memphis Winner? | NBA | BUY YES (Memphis wins) | $9.88 (76 × 13¢) | 39.8% | 12.5¢ | +27.3 pp | pending |
| 2 | Zverev vs Sinner (Semifinal) | ATP | BUY YES (Zverev wins) | $9.92 (62 × 16¢) | 40.6% | 15.0¢ | +25.6 pp | pending |
| 3 | Chicago at Oklahoma City Winner? | NBA | BUY NO (OKC loses) | $9.96 (166 × 6¢) | 70.0% | 94.5¢ | −24.5 pp | pending |
| 4 | Utah at Denver Winner? | NBA | BUY YES (Utah wins) | $9.96 (166 × 6¢) | 27.6% | 5.5¢ | +22.1 pp | pending |

**Total wagered: $39.72**

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
