import unittest
from unittest.mock import patch

from requests.exceptions import RequestException
from src.data.market import service as market_service
from src.data.market.service import fetch_price_trend
from src.data.news import ingestion as news_ingestion
from src.data.news.ingestion import load_news_items


class LoggingTests(unittest.TestCase):
    @patch.object(market_service.logger, "warning")
    @patch(
        "src.data.market.binance.fetch_binance_series",
        side_effect=RequestException("binance down"),
    )
    @patch(
        "src.data.market.coingecko.fetch_coingecko_series",
        side_effect=RequestException("coingecko down"),
    )
    @patch(
        "src.data.market.coinbase.fetch_coinbase_series",
        side_effect=RequestException("coinbase down"),
    )
    def test_logger_warning_on_all_providers_fail(
        self, _mock_cb, _mock_cg, _mock_bn, mock_logger
    ):
        fetch_price_trend("BTC", 30, "30D")
        self.assertGreaterEqual(mock_logger.call_count, 1)

    @patch.object(news_ingestion.logger, "warning")
    @patch("src.data.news.ingestion._feed_urls", return_value=["https://example.com/feed"])
    @patch("src.data.news.ingestion._parse_feed", side_effect=Exception("feed failed"))
    def test_logger_warning_on_news_feed_failure(self, _mock_parse, _mock_urls, mock_logger):
        load_news_items()
        mock_logger.assert_called_once()


if __name__ == "__main__":
    unittest.main()
