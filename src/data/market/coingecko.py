import requests
from src.data.market.config import load_market_config

ASSET_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
}


def fetch_coingecko_series(asset: str, days: int):
    config = load_market_config()
    asset_id = ASSET_IDS.get(asset)
    if not asset_id:
        return None

    url = f"{config.coingecko_base_url.rstrip('/')}/coins/{asset_id}/market_chart"
    response = requests.get(
        url,
        params={"vs_currency": "usd", "days": str(max(days, 1))},
        timeout=config.request_timeout_seconds,
    )
    response.raise_for_status()
    payload = response.json()
    prices = payload.get("prices") or []
    if not prices:
        return None

    dates = [row[0] for row in prices]
    values = [float(row[1]) for row in prices]
    return dates, values, "coingecko"
