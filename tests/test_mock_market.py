import unittest

from src.data.mock_market import (
    PRICE_TREND_DAYS,
    alert_snapshot_lines,
    alerts_snapshot,
    kpi_snapshot,
    kpi_snapshot_lines,
    news_snapshot,
    news_snapshot_lines,
    price_trend_series,
    risk_graph_colors,
    risk_graph_labels,
    risk_graph_scores,
    trending_report_frame,
)


class MockMarketTests(unittest.TestCase):
    def test_price_trend_series_lengths(self):
        dates, prices, trend = price_trend_series()
        self.assertEqual(len(dates), PRICE_TREND_DAYS)
        self.assertEqual(len(prices), PRICE_TREND_DAYS)
        self.assertEqual(len(trend), PRICE_TREND_DAYS)

    def test_trending_report_frame_has_expected_assets(self):
        frame = trending_report_frame()
        self.assertEqual(list(frame["Asset"]), ["BTC", "ETH", "SOL", "BNB", "XRP"])

    def test_risk_graph_inputs_align(self):
        scores = risk_graph_scores()
        labels = risk_graph_labels()
        colors = risk_graph_colors()
        self.assertEqual(len(scores), len(labels))
        self.assertEqual(len(scores), len(colors))

    def test_snapshot_line_helpers_match_snapshots(self):
        self.assertEqual(
            kpi_snapshot_lines(),
            [f"{item['label']}: {item['value']} ({item['delta']})" for item in kpi_snapshot()],
        )
        self.assertEqual(alert_snapshot_lines(), list(alerts_snapshot()))
        self.assertEqual(news_snapshot_lines(), list(news_snapshot()))


if __name__ == "__main__":
    unittest.main()
