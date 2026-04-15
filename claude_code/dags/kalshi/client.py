import base64
import datetime
import time
import uuid
from typing import Optional

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from .config import KALSHI_BASE_URL, SPORTS_SERIES
from .utils import parse_ticker_date


class KalshiClient:
    def __init__(self, key_id: str, key_file: str,
                 base_url: str = KALSHI_BASE_URL):
        self.key_id   = key_id
        self.base_url = base_url
        with open(key_file, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(), password=None, backend=default_backend()
            )

    # ── Auth ─────────────────────────────────────────────────────────────────

    def _sign_pss(self, text: str) -> str:
        sig = self.private_key.sign(
            text.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.DIGEST_LENGTH,
            ),
            hashes.SHA256(),
        )
        return base64.b64encode(sig).decode("utf-8")

    def _auth_headers(self, method: str, path: str) -> dict:
        ts  = str(int(time.time() * 1000))
        msg = ts + method.upper() + path.split("?")[0]
        return {
            "KALSHI-ACCESS-KEY":       self.key_id,
            "KALSHI-ACCESS-SIGNATURE": self._sign_pss(msg),
            "KALSHI-ACCESS-TIMESTAMP": ts,
            "Content-Type":            "application/json",
        }

    # ── HTTP verbs ────────────────────────────────────────────────────────────

    def get(self, path: str, params: dict = None) -> dict:
        r = requests.get(self.base_url + path,
                         headers=self._auth_headers("GET", path),
                         params=params, timeout=15)
        r.raise_for_status()
        return r.json()

    def post(self, path: str, body: dict) -> dict:
        r = requests.post(self.base_url + path,
                          headers=self._auth_headers("POST", path),
                          json=body, timeout=15)
        r.raise_for_status()
        return r.json()

    def delete(self, path: str) -> dict:
        r = requests.delete(self.base_url + path,
                            headers=self._auth_headers("DELETE", path),
                            timeout=15)
        r.raise_for_status()
        return r.json()

    # ── Portfolio ─────────────────────────────────────────────────────────────

    def get_balance_usd(self) -> float:
        return self.get("/trade-api/v2/portfolio/balance")["balance"] / 100.0

    def get_open_orders(self) -> list:
        data = self.get("/trade-api/v2/portfolio/orders",
                        params={"status": "resting"})
        return data.get("orders", [])

    def cancel_order(self, order_id: str) -> dict:
        return self.delete(f"/trade-api/v2/portfolio/orders/{order_id}")

    # ── Markets ───────────────────────────────────────────────────────────────

    def get_todays_game_markets(self) -> list:
        """
        Returns all open Kalshi sports game markets whose ticker date is today
        or yesterday in US Eastern time.

        Kalshi dates its tickers by the ET calendar date of the game.  Using ET
        here (rather than UTC) prevents the midnight-UTC cron run from seeing
        "tomorrow's" markets four hours early, which caused the bot to trade
        next-day games while it was still the previous evening in the US.

        We still include yesterday-ET to cover games whose ticker was issued the
        prior ET calendar day but whose start time falls after UTC midnight
        (e.g. a 9 pm ET game = 01:00 UTC the next UTC day).
        """
        et = datetime.timezone(datetime.timedelta(hours=-4), name="ET")  # EDT; use -5 in winter
        today     = datetime.datetime.now(et).date()
        yesterday = today - datetime.timedelta(days=1)
        valid_dates = {today, yesterday}
        markets = []
        for series_ticker in SPORTS_SERIES:
            cursor = None
            while True:
                params = {"status": "open", "series_ticker": series_ticker,
                          "limit": 200}
                if cursor:
                    params["cursor"] = cursor
                try:
                    data = self.get("/trade-api/v2/markets", params=params)
                except requests.HTTPError:
                    break
                for m in data.get("markets", []):
                    game_date = parse_ticker_date(series_ticker,
                                                  m.get("ticker", ""))
                    if game_date in valid_dates:
                        m["_series"] = series_ticker
                        markets.append(m)
                cursor = data.get("cursor")
                if not cursor:
                    break
        return markets

    # ── Orders ────────────────────────────────────────────────────────────────

    def place_order(self, ticker: str, side: str,
                    price_cents: int, count: int) -> dict:
        """Place a limit buy order. side: 'yes' | 'no'."""
        body = {
            "ticker":          ticker,
            "client_order_id": str(uuid.uuid4()),
            "action":          "buy",
            "side":            side,
            "type":            "limit",
            "count":           count,
        }
        if side == "yes":
            body["yes_price"] = price_cents
        else:
            body["no_price"]  = price_cents
        return self.post("/trade-api/v2/portfolio/orders", body)
