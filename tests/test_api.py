import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


class ApiHealthTests(unittest.TestCase):
    def test_health_returns_ok(self):
        resp = client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"status": "ok"})


class ApiSnapshotTests(unittest.TestCase):
    @patch("src.data.market.service.fetch_ccxt_series", return_value=None)
    @patch("src.data.news.ingestion._parse_feed", return_value=[])
    def test_snapshot_returns_expected_structure(self, _mock_news, _mock_ccxt):
        resp = client.get("/api/snapshot?window=30D&assets=BTC&source=mock")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("primary_asset", data)
        self.assertIn("price_values", data)
        self.assertIn("kpis", data)
        self.assertIn("alerts", data)

    def test_snapshot_with_multiple_assets(self):
        resp = client.get("/api/snapshot?window=30D&assets=BTC,ETH,SOL")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("BTC", data["watchlist"])


if __name__ == "__main__":
    unittest.main()
