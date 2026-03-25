"""
Binance Futures Testnet – Simple Trading Bot CLI
Usage examples:
  python main.py account
  python main.py order BTCUSDT BUY MARKET --quantity 0.001
  python main.py order BTCUSDT SELL LIMIT --quantity 0.001 --price 80000
  python main.py open-orders BTCUSDT
"""

import typer

import binance_client as bc
from logger import get_logger
from utils import get_api_keys, validate_order

app = typer.Typer(help="Simple Binance Futures Testnet trading bot.")
logger = get_logger("main")


@app.command()
def account():
    """Show basic account info (balances)."""
    api_key, api_secret = get_api_keys()
    try:
        info = bc.get_account_info(api_key, api_secret)
        typer.echo(f"\nTotal Wallet Balance : {info.get('totalWalletBalance')} USDT")
        typer.echo(f"Available Balance    : {info.get('availableBalance')} USDT")
        typer.echo(f"Unrealised PnL       : {info.get('totalUnrealizedProfit')} USDT\n")
        logger.info("Account info fetched successfully.")
    except Exception as e:
        logger.error("Failed to fetch account info: %s", e)
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def order(
    symbol: str = typer.Argument(..., help="Trading pair, e.g. BTCUSDT"),
    side: str = typer.Argument(..., help="BUY or SELL"),
    order_type: str = typer.Argument(..., help="MARKET or LIMIT"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="Quantity to trade"),
    price: float = typer.Option(None, "--price", "-p", help="Price (required for LIMIT orders)"),
):
    """Place a MARKET or LIMIT order."""
    try:
        validate_order(symbol, side, order_type, quantity, price)
    except ValueError as e:
        typer.echo(f"Validation error: {e}", err=True)
        raise typer.Exit(code=1)

    api_key, api_secret = get_api_keys()

    typer.echo(f"\nPlacing {order_type.upper()} {side.upper()} order for {quantity} {symbol.upper()}...")

    try:
        result = bc.place_order(api_key, api_secret, symbol, side, order_type, quantity, price)
        typer.echo(f"  Order ID   : {result.get('orderId')}")
        typer.echo(f"  Status     : {result.get('status')}")
        typer.echo(f"  Symbol     : {result.get('symbol')}")
        typer.echo(f"  Side       : {result.get('side')}")
        typer.echo(f"  Type       : {result.get('type')}")
        typer.echo(f"  Quantity   : {result.get('origQty')}")
        if result.get("price") and result["price"] != "0":
            typer.echo(f"  Price      : {result.get('price')}")
        typer.echo()
        logger.info("Order placed: %s", result)
    except RuntimeError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command(name="open-orders")
def open_orders(
    symbol: str = typer.Argument(..., help="Trading pair, e.g. BTCUSDT"),
):
    """List all open orders for a symbol."""
    api_key, api_secret = get_api_keys()
    try:
        orders = bc.get_open_orders(api_key, api_secret, symbol)
        if not orders:
            typer.echo(f"No open orders for {symbol.upper()}.")
            return
        typer.echo(f"\nOpen orders for {symbol.upper()}:")
        for o in orders:
            typer.echo(
                f"  [{o.get('orderId')}] {o.get('side')} {o.get('type')} "
                f"qty={o.get('origQty')} price={o.get('price')} status={o.get('status')}"
            )
        typer.echo()
        logger.info("Fetched %d open order(s) for %s.", len(orders), symbol)
    except Exception as e:
        logger.error("Failed to fetch open orders: %s", e)
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
