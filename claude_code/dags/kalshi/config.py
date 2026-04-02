import datetime
import os

# ── Kalshi API ────────────────────────────────────────────────────────────────
KALSHI_BASE_URL    = "https://api.elections.kalshi.com"
KALSHI_KEY_ID      = os.environ.get("KALSHI_KEY_ID", "")
KALSHI_KEY_FILE    = os.environ.get("KALSHI_KEY_FILE", "")

# ── Trading parameters ────────────────────────────────────────────────────────
MAX_TRADES_PER_DAY = 4
BUDGET_USD         = 10.00   # dollars per trade
MIN_EDGE_PP        = 10.0    # minimum |model_prob - kalshi_mid| in pp to trade

# ── Strategy override ─────────────────────────────────────────────────────────
# When set, the bot bets WITH Kalshi's implied probability rather than the
# independent model through this date (inclusive). Set to None to always use
# the model-first ("fade Kalshi") strategy.
TRUST_KALSHI_UNTIL = datetime.date(2026, 4, 9)

# ── Data sources ──────────────────────────────────────────────────────────────
ESPN_BASE = "http://site.api.espn.com/apis/site/v2/sports"

# Kalshi series ticker → (ESPN sport path, ESPN league path)
SPORTS_SERIES = {
    "KXNBAGAME":  ("basketball", "nba"),
    "KXMLBGAME":  ("baseball",   "mlb"),
    "KXNHLGAME":  ("hockey",     "nhl"),
    "KXWTAMATCH": ("tennis",     "wta"),
    "KXATPMATCH": ("tennis",     "atp"),
}

# ── File paths ────────────────────────────────────────────────────────────────
# Resolved relative to the trading repo root (three levels above this file:
#   dags/kalshi/config.py → dags/kalshi/ → dags/ → claude_code/ → trading/)
_HERE         = os.path.dirname(os.path.abspath(__file__))
TRADING_ROOT  = os.path.abspath(os.path.join(_HERE, "../../.."))

TRADE_LOG_FILE    = os.path.join(TRADING_ROOT, "kalshi_trades.json")
TRADES_MD         = os.path.join(TRADING_ROOT, "TRADES.md")
MODEL_OUTPUTS_DIR = os.path.join(TRADING_ROOT, "model_outputs")
