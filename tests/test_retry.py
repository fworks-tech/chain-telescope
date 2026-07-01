import unittest
from unittest.mock import Mock, patch

from requests.exceptions import RequestException
from src.data.market.binance import fetch_binance_series
from src.data.market.coinbase import fetch_coinbase_series
from src.data.market.coingecko import fetch_coingecko_series


def _mock_response(data):
    mock = Mock()
    mock.json.return_value = data
    mock.raise_for_status.return_value = None
    mock.status_code = 200
    return mock


class RetryTests(unittest.TestCase):
    @patch("requests.get")
    def test_binance_retries_on_failure(self, mock_get):
        mock_get.side_effect = [
            RequestException("fail"),
            RequestException("fail"),
            _mock_response([[1715683200000, "1", "2", "3", "100.0", "5"]]),
        ]
        result = fetch_binance_series("BTC", 30)
        self.assertIsNotNone(result)
        self.assertEqual(mock_get.call_count, 3)

    @patch("requests.get")
    def test_binance_returns_none_no_symbol(self, mock_get):
        result = fetch_binance_series("UNKNOWN", 30)
        self.assertIsNone(result)
        mock_get.assert_not_called()

    @patch("requests.get")
    def test_coingecko_succeeds_on_second_attempt(self, mock_get):
        mock_get.side_effect = [
            RequestException("fail"),
            _mock_response({"prices": [[1715683200000, 100.0]]}),
        ]
        result = fetch_coingecko_series("BTC", 30)
        self.assertIsNotNone(result)
        self.assertEqual(mock_get.call_count, 2)

    @patch("requests.get")
    def test_coinbase_succeeds_on_second_attempt(self, mock_get):
        mock_get.side_effect = [
            RequestException("fail"),
            _mock_response([[1715683200, 1, 2, 3, 100.0, 5]]),
        ]
        result = fetch_coinbase_series("BTC", 30)
        self.assertIsNotNone(result)
        self.assertEqual(mock_get.call_count, 2)


if __name__ == "__main__":
    unittest.main()
