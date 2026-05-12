import math
from datetime import datetime, timedelta

import pandas as pd

TIME_WINDOW_DAYS = {"24H": 1, "7D": 7, "30D": 30, "90D": 90}
ASSET_BASE_PRICES = {
  "BTC": 64000.0,
  "ETH": 3200.0,
  "SOL": 145.0,
  "BNB": 580.0,
  "XRP": 0.62,
}

TRENDING_ROWS = {
  "BTC": ("+6.2%", "Bullish", "Medium"),
  "ETH": ("+4.1%", "Bullish", "Medium"),
  "SOL": ("+12.8%", "Very Bullish", "High"),
  "BNB": ("+2.9%", "Neutral", "Medium"),
  "XRP": ("-1.4%", "Mixed", "High"),
}


def price_trend_series(asset="BTC", days=30, time_window="30D"):
  del time_window
  base = ASSET_BASE_PRICES.get(asset, 1000.0)
  dates = [datetime.today() - timedelta(days=(days - 1 - index)) for index in range(days)]
  prices = [base + 1200 * math.sin(index / 3) + index * (base * 0.0007) for index in range(days)]
  trend = pd.Series(prices).rolling(5, min_periods=1).mean()
  return dates, prices, trend


def trending_report_frame(watchlist=None):
  assets = watchlist or list(TRENDING_ROWS)
  rows = []
  for asset in assets:
    change, sentiment, risk = TRENDING_ROWS.get(asset, ("0.0%", "Neutral", "Medium"))
    rows.append({
      "Asset": asset,
      "7D Change": change,
      "Sentiment": sentiment,
      "Risk": risk,
    })
  return pd.DataFrame(rows)


def risk_graph_scores():
  return [62, 48, 71, 55]


def risk_snapshot(time_window="30D"):
  scores = risk_graph_scores()
  offset = {"24H": -4, "7D": -2, "30D": 0, "90D": 3}.get(time_window, 0)
  return [max(0, min(100, score + offset)) for score in scores]


def risk_graph_labels():
  return ["Market", "Liquidity", "Momentum", "Whale Activity"]


def risk_graph_colors():
  return ["#f79009", "#12b76a", "#f04438", "#3b5bff"]


def kpi_snapshot(time_window="30D", watchlist=None):
  tracked = len(watchlist or ["BTC", "ETH", "SOL"])
  return [
    {"label": "Market Cap Tracked", "value": f"${1.8 + tracked * 0.11:.2f}T", "delta": "+2.8%", "color": "#12b76a"},
    {"label": "24H Volume", "value": f"${70 + tracked * 5.4:.1f}B", "delta": "+5.1%", "color": "#12b76a"},
    {"label": "Risk Index", "value": f"{risk_snapshot(time_window)[0]} / 100", "delta": "Elevated", "color": "#f79009"},
    {"label": "Active Alerts", "value": str(4 + tracked), "delta": "3 triggered today", "color": "#3b5bff"},
  ]


def alerts_snapshot():
  return ["BTC below 63,500", "ETH RSI crossed 70", "SOL breakout"]


def news_snapshot():
  return ["ETF flows rebound", "Layer-1 activity rotates to SOL", "Exchange reserves decline"]


def kpi_snapshot_lines(time_window="30D", watchlist=None):
  return [f"{item['label']}: {item['value']} ({item['delta']})" for item in kpi_snapshot(time_window, watchlist)]


def alert_snapshot_lines():
  return list(alerts_snapshot())


def news_snapshot_lines():
  return list(news_snapshot())
