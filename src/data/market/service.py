from datetime import datetime

import pandas as pd

from src.data.market import binance, coingecko
from src.data.market.config import load_market_config
from src.data.mock_market import TIME_WINDOW_DAYS, price_trend_series


def fetch_price_trend(asset: str, days: int, time_window: str):
  config = load_market_config()
  provider = config.provider.lower()
  providers = []
  if provider == "binance":
    providers = ["binance"]
  elif provider == "coingecko":
    providers = ["coingecko"]
  else:
    providers = ["binance", "coingecko"]

  for name in providers:
    try:
      if name == "binance":
        result = binance.fetch_binance_series(asset, days)
      else:
        result = coingecko.fetch_coingecko_series(asset, days)
      if result:
        dates, prices, source = result
        dates = _normalize_dates(dates)
        trend = pd.Series(prices).rolling(5, min_periods=1).mean()
        return dates, prices, trend, source
    except Exception:
      continue

  fallback_days = TIME_WINDOW_DAYS.get(time_window, days)
  dates, prices, trend = price_trend_series(asset=asset, days=fallback_days, time_window=time_window)
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
