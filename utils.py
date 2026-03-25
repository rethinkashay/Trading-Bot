import os
import sys
from dotenv import load_dotenv

from logger import get_logger

logger = get_logger("utils")

VALID_SIDES = ("BUY", "SELL")
VALID_ORDER_TYPES = ("MARKET", "LIMIT")


def get_api_keys() -> tuple[str, str]:
    """Read API keys from environment variables."""
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY", "")
    api_secret = os.getenv("BINANCE_API_SECRET", "")

    if not api_key or not api_secret:
        logger.error("BINANCE_API_KEY and BINANCE_API_SECRET must be set.")
        sys.exit(1)

    return api_key, api_secret


def validate_order(symbol: str, side: str, order_type: str, quantity: float, price: float | None):
    """Basic validation for order params. Raises ValueError with a clear message."""
    if not symbol:
        raise ValueError("Symbol cannot be empty.")

    if side.upper() not in VALID_SIDES:
        raise ValueError(f"Side must be one of {VALID_SIDES}, got '{side}'.")

    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type must be one of {VALID_ORDER_TYPES}, got '{order_type}'.")

    if quantity <= 0:
        raise ValueError(f"Quantity must be positive, got {quantity}.")

    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("A positive price is required for LIMIT orders.")
