import requests
from src.data.assets import BINANCE_SYMBOLS
from src.data.market.config import load_market_config

ASSET_SYMBOLS = BINANCE_SYMBOLS


def fetch_binance_series(asset: str, days: int):
    config = load_market_config()
    symbol = ASSET_SYMBOLS.get(asset)
    if not symbol:
        return None

    interval = "1d" if days > 1 else "1h"
    limit = max(days, 1)
    url = f"{config.binance_base_url.rstrip('/')}/api/v3/klines"
    response = requests.get(
        url,
        params={"symbol": symbol, "interval": interval, "limit": limit},
        timeout=config.request_timeout_seconds,
    )
    response.raise_for_status()
    payload = response.json()
    if not payload:
        return None

    dates = [row[0] for row in payload]
    prices = [float(row[4]) for row in payload]
    return dates, prices, "binance"
