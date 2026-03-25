import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests

from logger import get_logger

logger = get_logger("binance_client")

BASE_URL = "https://testnet.binancefuture.com"


def _sign(params: dict, secret: str) -> str:
    query_string = urlencode(params)
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()  # noqa: E501


def _headers(api_key: str) -> dict:
    return {"X-MBX-APIKEY": api_key}


def get_account_info(api_key: str, api_secret: str) -> dict:
    """Fetch account info to verify connectivity."""
    endpoint = "/fapi/v2/account"
    params = {"timestamp": int(time.time() * 1000)}
    params["signature"] = _sign(params, api_secret)

    url = BASE_URL + endpoint
    resp = requests.get(url, headers=_headers(api_key), params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def place_order(
    api_key: str,
    api_secret: str,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
) -> dict:
    """Place a MARKET or LIMIT futures order on Binance Testnet."""
    endpoint = "/fapi/v1/order"

    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
        "timestamp": int(time.time() * 1000),
    }

    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    params["signature"] = _sign(params, api_secret)

    url = BASE_URL + endpoint
    logger.debug("Placing order: %s", params)

    resp = requests.post(url, headers=_headers(api_key), params=params, timeout=10)

    if not resp.ok:
        error_msg = resp.json().get("msg", resp.text)
        logger.error("Binance API error: %s", error_msg)
        raise RuntimeError(f"Binance API error: {error_msg}")

    return resp.json()


def get_open_orders(api_key: str, api_secret: str, symbol: str) -> list:
    """Get all open orders for a symbol."""
    endpoint = "/fapi/v1/openOrders"
    params = {
        "symbol": symbol.upper(),
        "timestamp": int(time.time() * 1000),
    }
    params["signature"] = _sign(params, api_secret)

    url = BASE_URL + endpoint
    resp = requests.get(url, headers=_headers(api_key), params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()
