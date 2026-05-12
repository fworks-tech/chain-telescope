import os

from dotenv import load_dotenv
from src.data.market.models import MarketConfig

load_dotenv()


def load_market_config() -> MarketConfig:
    return MarketConfig(
        provider=os.getenv("MARKET_PROVIDER", "auto"),
        binance_base_url=os.getenv("BINANCE_BASE_URL", "https://api.binance.com"),
        coingecko_base_url=os.getenv("COINGECKO_BASE_URL", "https://api.coingecko.com/api/v3"),
        request_timeout_seconds=float(os.getenv("MARKET_REQUEST_TIMEOUT_SECONDS", "10")),
    )
