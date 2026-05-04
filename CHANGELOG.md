# Changelog

---

## 2026-05-02

### Added
- **Account balance log** — every run now appends a `(timestamp, balance_usd)` entry to `kalshi_balance_log.json` and rewrites the `## Account Balance` section at the top of `TRADES.md` so cash balance over time is visible at a glance. Tracks cash only; does not include the value of open limit orders or unsettled positions.

### Changed
- **Strategy column rewrite in TRADES.md** — the old `Source` column held raw labels like `espn:win_pct+form`. Replaced with a `Strategy` column rendered via `_strategy_desc()` in `reporting.py` (e.g. "Fade Kalshi → ESPN season win-rate (weakest fallback)"). Trades logged before this change, which lack `model_source`, render as `unknown`.
- **MODEL.md updated** to reflect current parameters: 2pp edge threshold (was 10pp), 3.0h trade horizon (was 3.5h), Kelly sizing instead of the old proportional $10/$15/$20 tiers, and notes on SOS, injury adjustment, and the disabled tennis model.

### Infrastructure
- **Bot migrated from Mac mini to EC2** so it runs 24/7 without depending on the local machine. Cron schedule: `0 */3 * * *` (every 3 hours).
- **`run_daily.sh` adapted for Linux** — removed the macOS Homebrew PATH and the launchd/Keychain SSH-agent block. Git push now relies on the SSH deploy key at `~/.ssh/github_deploy`.
- **Resolve step now updates opponent strength** — `resolve.py` walks resolved trades and feeds `(home, away, winner)` into `OpponentStrengthDB` so SOS ratings adapt to actual outcomes, not just bootstrapped ESPN standings.

---

## 2026-04-22

### Added
- **SOS (Strength of Schedule) adjustment** — `opponent_strength.py` bootstraps team win percentages from ESPN standings once per day and applies a mild correction (`SOS_MULTIPLIER = 0.15`) to win-rate estimates. A strong opponent nudges the probability down; a weak one nudges it up.
- **Injury adjustment** — `injury_data.py` fetches ESPN's public `/injuries` endpoint once per run. Applied only on the win-rate fallback path: −1.5 pp per Out player, −0.5 pp per Questionable player, capped at −5 pp per team. Sportsbook odds and Polymarket already price in injuries.

### Changed
- `TRADE_HORIZON_HOURS` reduced from 3.5 → **3.0** to match the 3-hour cron interval exactly (the 0.5h overlap was no longer needed after the ET date fix).

---

## 2026-04-15

### Fixed
- **Midnight UTC date bug** — the 00:00 UTC cron run (8 PM ET) was calling `datetime.date.today()` which returned the next calendar day, causing the bot to fetch next-day markets. Both `client.py` and `model.py` now use US Eastern time for all date logic.

---

## 2026-04-10

### Changed
- **Sizing switched to fractional Kelly** — replaced the fixed proportional tiers ($10/$15/$20) with quarter-Kelly sizing (`KELLY_FRACTION = 0.25`, `MAX_BET = $20`). Small-edge trades naturally size down; the cap only binds on large edges.
- **Polymarket gate relaxed** — Polymarket is the preferred signal but is no longer required. When no Polymarket match is found the bot falls back to ESPN sportsbook odds, then win-rate/form, rather than skipping the game.

### Removed
- **Tennis disabled** — ATP/WTA removed from `SPORTS_SERIES`. The log-rank model remains in the codebase but no tennis markets are fetched. Reason: ESPN rankings are current-only, creating look-ahead bias in any evaluation, and live tennis results were poor.

---

## 2026-04-09

### Changed
- **`MIN_EDGE_PP` lowered from 10 → 2 pp** — relaxes the entry threshold to catch smaller Polymarket/Kalshi discrepancies. Kelly sizing naturally limits small-edge trades to ~$1.
- **Trade deduplication across runs** — each run now reads today's trade log and skips any market whose event ticker was already traded earlier that day, preventing the same game from being bet in multiple consecutive cron runs.
