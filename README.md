# Binance Futures Testnet – Simple Trading Bot

A minimal CLI trading bot for Binance Futures Testnet, built with Python 3.

## Setup

1. **Clone / copy** the project files.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your Binance Testnet API keys** as environment variables:
   ```bash
   # Windows (PowerShell)
   $env:BINANCE_API_KEY = "your_testnet_api_key"
   $env:BINANCE_API_SECRET = "your_testnet_api_secret"

   # Linux / macOS
   export BINANCE_API_KEY="your_testnet_api_key"
   export BINANCE_API_SECRET="your_testnet_api_secret"
   ```
   Get your testnet keys at: https://testnet.binancefuture.com

## Usage

```bash
# Show account balances
python main.py account

# Place a MARKET BUY order
python main.py order BTCUSDT BUY MARKET --quantity 0.001

# Place a LIMIT SELL order
python main.py order BTCUSDT SELL LIMIT --quantity 0.001 --price 80000

# List open orders
python main.py open-orders BTCUSDT

# Help
python main.py --help
python main.py order --help
```

## Files

```
trading-bot/
├── main.py           # CLI entry point (Typer commands)
├── binance_client.py # Binance API calls (sign + HTTP)
├── utils.py          # Input validation + key loading
├── logger.py         # Logging to bot.log + console
└── requirements.txt  # Dependencies
```

## Logs

All activity is logged to `bot.log` in the project folder.

## Notes

- MARKET orders execute immediately at current price (no `--price` needed).
- LIMIT orders require `--price`.
- All orders are placed on the **testnet** — no real money involved.
