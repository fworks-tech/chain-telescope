import math
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from src.data.alerts.rules import evaluate_alert_rules
from src.data.dashboard_query import load_dashboard_snapshot
from src.data.market.service import fetch_price_trend
from src.data.mock_market import ASSET_BASE_PRICES, price_trend_series
from src.data.news.ingestion import load_news_items


class DashboardQueryTests(unittest.TestCase):
    def test_snapshot_filters_trending_by_watchlist(self):
        snapshot = load_dashboard_snapshot("30D", ["SOL", "ETH"])
        self.assertEqual(list(snapshot.trending["Asset"]), ["SOL", "ETH"])

    def test_snapshot_applies_top_losers_trend_filter(self):
        snapshot = load_dashboard_snapshot(
            "30D", ["BTC", "ETH", "SOL", "XRP"], trend_filter="top_losers"
        )
        self.assertEqual(list(snapshot.trending["Asset"]), ["XRP"])
        self.assertEqual(snapshot.trend_filter, "top_losers")

    def test_price_series_pairs_dates_and_prices_chronologically(self):
        days = 30
        dates, prices, _ = price_trend_series(asset="BTC", days=days, time_window="30D")
        base = ASSET_BASE_PRICES["BTC"]
        self.assertEqual(len(dates), len(prices))
        for index, date, price in zip(range(days), dates, prices, strict=True):
            expected = base + 1200 * math.sin(index / 3) + index * (base * 0.0007)
            self.assertAlmostEqual(price, expected)
            self.assertEqual(
                date.date(), (datetime.today() - timedelta(days=(days - 1 - index))).date()
            )
        self.assertLess(dates[0], dates[-1])
        self.assertLess(prices[0], prices[-1])


class MarketServiceTests(unittest.TestCase):
    @patch("src.data.market.coinbase.fetch_coinbase_series", return_value=None)
    @patch("src.data.market.coingecko.fetch_coingecko_series", return_value=None)
    @patch("src.data.market.binance.fetch_binance_series", return_value=None)
    def test_fetch_price_trend_falls_back_to_mock(
        self, _mock_binance, _mock_coingecko, _mock_coinbase
    ):
        _, _, _, source = fetch_price_trend("BTC", 30, "30D")
        self.assertEqual(source, "mock")

    @patch("src.data.market.coinbase.fetch_coinbase_series", return_value=None)
    @patch("src.data.market.coingecko.fetch_coingecko_series", return_value=None)
    @patch("src.data.market.binance.fetch_binance_series", return_value=None)
    def test_fetch_price_trend_mock_source_skips_remote_providers(
        self, _mock_binance, _mock_coingecko, _mock_coinbase
    ):
        _, _, _, source = fetch_price_trend("BTC", 30, "30D", market_source="mock")
        self.assertEqual(source, "mock")
        _mock_binance.assert_not_called()
        _mock_coingecko.assert_not_called()
        _mock_coinbase.assert_not_called()

    @patch(
        "src.data.market.service.binance.fetch_binance_series",
        return_value=([1715683200000, 1715769600000], [62000.0, 62500.0], "binance"),
    )
    def test_fetch_price_trend_normalizes_provider_dates(self, _mock_binance):
        dates, _, _, source = fetch_price_trend("BTC", 2, "24H")
        self.assertEqual(source, "binance")
        self.assertTrue(all(isinstance(date, datetime) for date in dates))


class NewsIngestionTests(unittest.TestCase):
    @patch("src.data.news.ingestion._parse_feed", return_value=[])
    def test_load_news_items_uses_fallback_items(self, _mock_parse):
        items = load_news_items(["BTC"])
        self.assertTrue(items)
        self.assertTrue(items[0].title)


class AlertsRulesTests(unittest.TestCase):
    def test_evaluate_alert_rules_reports_momentum(self):
        alerts = evaluate_alert_rules("30D", ["BTC"], [100.0, 112.0])
        self.assertTrue(any("momentum" in alert for alert in alerts))


if __name__ == "__main__":
    unittest.main()
