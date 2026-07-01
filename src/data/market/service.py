from datetime import datetime

import pandas as pd
from loguru import logger
from src.data.market import binance, coinbase, coingecko
from src.data.market.config import load_market_config
from src.data.mock_market import TIME_WINDOW_DAYS, price_trend_series


def fetch_price_trend(asset: str, days: int, time_window: str, market_source: str | None = None):
    provider = (market_source or load_market_config().provider).lower()
    if provider == "mock":
        return _mock_series(asset, days, time_window)

    providers = _provider_chain(provider)
    for name in providers:
        try:
            result = _fetch_provider_series(name, asset, days)
            if result:
                dates, prices, source = result
                dates = _normalize_dates(dates)
                trend = pd.Series(prices).rolling(5, min_periods=1).mean()
                return dates, prices, trend, source
        except Exception as exc:
            logger.warning("Provider {} failed for {}: {}", name, asset, exc)
            continue

    return _mock_series(asset, days, time_window)


def _provider_chain(provider: str) -> list[str]:
    if provider == "binance":
        return ["binance"]
    if provider == "coingecko":
        return ["coingecko"]
    if provider == "coinbase":
        return ["coinbase"]
    return ["binance", "coingecko", "coinbase"]


def _fetch_provider_series(provider: str, asset: str, days: int):
    if provider == "binance":
        return binance.fetch_binance_series(asset, days)
    if provider == "coingecko":
        return coingecko.fetch_coingecko_series(asset, days)
    if provider == "coinbase":
        return coinbase.fetch_coinbase_series(asset, days)
    return None


def _mock_series(asset: str, days: int, time_window: str):
    fallback_days = TIME_WINDOW_DAYS.get(time_window, days)
    dates, prices, trend = price_trend_series(
        asset=asset, days=fallback_days, time_window=time_window
    )
    return dates, prices, trend, "mock"


def _normalize_dates(dates):
    normalized = []
    for value in dates:
        if isinstance(value, datetime):
            normalized.append(value)
            continue
        if isinstance(value, (int, float)):
            normalized.append(pd.to_datetime(value, unit="ms").to_pydatetime())
            continue
        normalized.append(pd.to_datetime(value).to_pydatetime())
    return normalized
