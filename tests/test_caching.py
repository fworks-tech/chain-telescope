import unittest
from unittest.mock import patch

from src.views import cached_dashboard_snapshot


class CachingTests(unittest.TestCase):
    @patch("src.data.market.binance.fetch_binance_series")
    @patch("src.data.news.ingestion._parse_feed", return_value=[])
    def test_snapshot_cached_returns_consistent_data(self, _mock_news, mock_fetch):
        mock_fetch.return_value = (
            [1715683200000],
            [100.0],
            "binance",
        )
        snap1 = cached_dashboard_snapshot("30D", ["BTC"], market_source="binance")
        snap2 = cached_dashboard_snapshot("30D", ["BTC"], market_source="binance")
        self.assertEqual(snap1.primary_asset, snap2.primary_asset)
        self.assertEqual(snap1.price_values, snap2.price_values)

    @patch("src.data.market.binance.fetch_binance_series")
    @patch("src.data.news.ingestion._parse_feed", return_value=[])
    def test_different_time_window_produces_different_snapshot(self, _mock_news, mock_fetch):
        mock_fetch.side_effect = [
            ([1715683200000], [100.0], "binance"),
            ([1715683200000], [200.0], "binance"),
        ]
        snap1 = cached_dashboard_snapshot("90D", ["BTC"], market_source="binance")
        snap2 = cached_dashboard_snapshot("24H", ["BTC"], market_source="binance")
        self.assertEqual(snap1.primary_asset, snap2.primary_asset)
        self.assertNotEqual(snap1.time_window, snap2.time_window)


if __name__ == "__main__":
    unittest.main()
