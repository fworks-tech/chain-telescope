import math
from datetime import datetime, timedelta

import pandas as pd

PRICE_TREND_DAYS = 30


def price_trend_series(days=PRICE_TREND_DAYS):
  dates = [datetime.today() - timedelta(days=i) for i in range(days)][::-1]
  prices = [64000 + 1200 * math.sin(i / 3) + i * 45 for i in range(days)]
  trend = pd.Series(prices).rolling(5, min_periods=1).mean()
  return dates, prices, trend


def trending_report_frame():
  return pd.DataFrame({
    "Asset": ["BTC", "ETH", "SOL", "BNB", "XRP"],
    "7D Change": ["+6.2%", "+4.1%", "+12.8%", "+2.9%", "-1.4%"],
    "Sentiment": ["Bullish", "Bullish", "Very Bullish", "Neutral", "Mixed"],
    "Risk": ["Medium", "Medium", "High", "Medium", "High"],
  })


def risk_graph_scores():
  return [62, 48, 71, 55]


def risk_graph_labels():
  return ["Market", "Liquidity", "Momentum", "Whale Activity"]


def risk_graph_colors():
  return ["#f79009", "#12b76a", "#f04438", "#3b5bff"]
