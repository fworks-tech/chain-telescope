import requests
from src.data.assets import COINBASE_PRODUCTS
from src.data.market.config import load_market_config

PRODUCT_IDS = COINBASE_PRODUCTS

def fetch_coinbase_series(asset: str, days: int):
    config = load_market_config()
    product = PRODUCT_IDS.get(asset)
    if not product:
        return None

    granularity = 86400 if days > 1 else 3600
    limit = max(days, 1)
    url = f"https://api.exchange.coinbase.com/products/{product}/candles"
    response = requests.get(
        url,
        params={"granularity": granularity},
        timeout=config.request_timeout_seconds,
    )
    response.raise_for_status()
    payload = response.json()
    if not payload:
        return None

    rows = sorted(payload, key=lambda row: row[0])[-limit:]
    dates = [row[0] * 1000 for row in rows]
    prices = [float(row[4]) for row in rows]
    return dates, prices, "coinbase"
