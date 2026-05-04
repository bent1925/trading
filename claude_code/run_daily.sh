#!/bin/bash
# Wrapper called by cron. Sets up the environment then runs the daily bot.
# Logs are written to ../logs/run_daily.log (relative to this script).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TRADING_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$TRADING_ROOT/logs/run_daily.log"

mkdir -p "$TRADING_ROOT/logs"

# Redirect all output to the log file (append)
exec >> "$LOG_FILE" 2>&1
echo ""
echo "========================================"
echo "  run_daily.sh started: $(date)"
echo "========================================"

# ── Python path ──────────────────────────────────────────────────────────────
export PATH="/usr/local/bin:/usr/bin:/bin"

# ── Activate virtual environment ─────────────────────────────────────────────
VENV="$HOME/.venv"
if [ -f "$VENV/bin/activate" ]; then
    # shellcheck disable=SC1091
    source "$VENV/bin/activate"
else
    echo "WARNING: virtualenv not found at $VENV — using system Python"
fi

# ── Kalshi credentials ───────────────────────────────────────────────────────
# Load from .env if it exists (format: KEY=value, one per line)
ENV_FILE="$TRADING_ROOT/.env"
if [ -f "$ENV_FILE" ]; then
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
fi

# Verify credentials are set
if [ -z "${KALSHI_KEY_ID:-}" ] || [ -z "${KALSHI_KEY_FILE:-}" ]; then
    echo "ERROR: KALSHI_KEY_ID and KALSHI_KEY_FILE must be set in $ENV_FILE"
    exit 1
fi

# ── Run the bot ───────────────────────────────────────────────────────────────
python3 "$SCRIPT_DIR/run_daily.py"

echo "  run_daily.sh finished: $(date)"
