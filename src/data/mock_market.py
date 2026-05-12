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
    return pd.DataFrame(
        {
            "Asset": ["BTC", "ETH", "SOL", "BNB", "XRP"],
            "7D Change": ["+6.2%", "+4.1%", "+12.8%", "+2.9%", "-1.4%"],
            "Sentiment": ["Bullish", "Bullish", "Very Bullish", "Neutral", "Mixed"],
            "Risk": ["Medium", "Medium", "High", "Medium", "High"],
        }
    )


def risk_graph_scores():
    return [62, 48, 71, 55]


def risk_graph_labels():
    return ["Market", "Liquidity", "Momentum", "Whale Activity"]


def risk_graph_colors():
    return ["#f79009", "#12b76a", "#f04438", "#3b5bff"]


def kpi_snapshot():
    return [
        {
            "label": "Market Cap Tracked",
            "value": "$2.14T",
            "delta": "+2.8%",
            "color": "#12b76a",
        },
        {
            "label": "24H Volume",
            "value": "$86.3B",
            "delta": "+5.1%",
            "color": "#12b76a",
        },
        {
            "label": "Risk Index",
            "value": "62 / 100",
            "delta": "Elevated",
            "color": "#f79009",
        },
        {
            "label": "Active Alerts",
            "value": "7",
            "delta": "3 triggered today",
            "color": "#3b5bff",
        },
    ]


def alerts_snapshot():
    return ["BTC below 63,500", "ETH RSI crossed 70", "SOL breakout"]


def news_snapshot():
    return [
        "ETF flows rebound",
        "Layer-1 activity rotates to SOL",
        "Exchange reserves decline",
    ]


def kpi_snapshot_lines():
    return [f"{item['label']}: {item['value']} ({item['delta']})" for item in kpi_snapshot()]


def alert_snapshot_lines():
    return list(alerts_snapshot())


def news_snapshot_lines():
    return list(news_snapshot())
