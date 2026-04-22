import os

# ── Kalshi API ────────────────────────────────────────────────────────────────
KALSHI_BASE_URL    = "https://api.elections.kalshi.com"
KALSHI_KEY_ID      = os.environ.get("KALSHI_KEY_ID", "")
KALSHI_KEY_FILE    = os.environ.get("KALSHI_KEY_FILE", "")

# ── Trading pause ─────────────────────────────────────────────────────────────
TRADING_PAUSED_UNTIL = "2026-04-14"  # resume on this date (inclusive)

# ── Trading parameters ────────────────────────────────────────────────────────
MAX_TRADES_PER_RUN   = 5
MIN_BALANCE_TO_TRADE = 10.00  # skip all trading if balance is below this
MIN_EDGE_PP          = 2.0    # minimum |kalshi_mid - model_prob| in pp to trade
TRADE_HORIZON_HOURS  = 3.0   # lookahead window per run; matches the 3-hour run interval

# Kelly criterion sizing
KELLY_FRACTION = 0.25   # quarter-Kelly — standard conservative fraction
MAX_BET        = 20.00  # hard cap per trade in dollars

# ── Strength of Schedule (SOS) adjustment ──────────────────────────────────
SOS_MULTIPLIER = 0.15   # how much opponent strength affects win-rate adjustment
                        # 0.0 = disabled (use original win-rate), 0.15 = mild, 1.0 = full effect

# ── Injury adjustment (win-rate fallback only) ──────────────────────────────
INJURY_ADJUSTMENT_PP     = 1.5   # probability points subtracted per "Out" player
INJURY_ADJUSTMENT_MAX_PP = 5.0   # maximum total injury adjustment per team

# ── Data sources ──────────────────────────────────────────────────────────────
ESPN_BASE = "http://site.api.espn.com/apis/site/v2/sports"

# Kalshi series ticker → (ESPN sport path, ESPN league path)
SPORTS_SERIES = {
    "KXNBAGAME": ("basketball", "nba"),
    "KXMLBGAME": ("baseball",   "mlb"),
    "KXNHLGAME": ("hockey",     "nhl"),
}

# ── File paths ────────────────────────────────────────────────────────────────
# Resolved relative to the trading repo root (three levels above this file:
#   dags/kalshi/config.py → dags/kalshi/ → dags/ → claude_code/ → trading/)
_HERE         = os.path.dirname(os.path.abspath(__file__))
TRADING_ROOT  = os.path.abspath(os.path.join(_HERE, "../../.."))

TRADE_LOG_FILE    = os.path.join(TRADING_ROOT, "kalshi_trades.json")
TRADES_MD         = os.path.join(TRADING_ROOT, "TRADES.md")
MODEL_OUTPUTS_DIR = os.path.join(TRADING_ROOT, "model_outputs")
OPPONENT_STRENGTH_FILE = os.path.join(TRADING_ROOT, "opponent_strength.json")

# ── Injury data ────────────────────────────────────────────────────────────
# Uses ESPN's free public API — no API key required.
INJURY_DATA_ENABLED = True
