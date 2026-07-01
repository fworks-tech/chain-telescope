import requests
from src.data.assets import COINGECKO_IDS
from src.data.market.config import load_market_config
from tenacity import retry, stop_after_attempt, wait_exponential

ASSET_IDS = COINGECKO_IDS


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
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
