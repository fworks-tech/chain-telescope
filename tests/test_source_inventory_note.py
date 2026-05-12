import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_NOTE = REPO_ROOT / "docs" / "source-inventory-m4.md"
ARCH_DOC = REPO_ROOT / "docs" / "Architecture.md"


class SourceInventoryNoteTests(unittest.TestCase):
  def test_note_exists_and_has_required_sections(self):
    content = SOURCE_NOTE.read_text(encoding="utf-8")
    self.assertIn("## 1) Crypto market data", content)
    self.assertIn("## 2) News and RSS/feed sources", content)
    self.assertIn("## 3) Investors and capital markets signals", content)
    self.assertIn("## 4) Core developers and protocol communities", content)
    self.assertIn("## 5) Cross-cutting strategy", content)

  def test_issue_mapping_matches_14_to_18_scope(self):
    content = SOURCE_NOTE.read_text(encoding="utf-8")
    self.assertIn(
      "| #14 — wire sidebar filters to dashboard data | Keep market/feed providers queryable by selected watchlist/time-window filters so panel data can be filtered consistently |",
      content
    )
    self.assertIn(
      "| #15 — market data ingestion module | Implement market ingestion adapter with Binance default + CoinGecko fallback and graceful degradation when provider config is unset |",
      content
    )
    self.assertIn(
      "| #16 — news feed ingestion module | Implement news/feed ingestion normalization around RSS/Atom (`feedparser` schema + dedupe + timestamps) with NewsAPI fallback |",
      content
    )
    self.assertIn(
      "| #17 — alerts rules engine (MVP) | Build alert rules over normalized market + high-confidence investor/developer signals, including per-signal confidence metadata |",
      content
    )
    self.assertIn(
      "| #18 — newsletter persistence and delivery (MVP) | Implement newsletter persistence/delivery using normalized feed + market deltas, with cached fallback content and environment-based secrets |",
      content
    )

  def test_newsapi_name_is_consistent(self):
    content = SOURCE_NOTE.read_text(encoding="utf-8")
    self.assertIn("| NewsAPI / GDELT APIs | API |", content)
    self.assertIn("| Alerts/news feed | RSS/Atom via `feedparser` (crypto + official blogs + macro) | NewsAPI (free tier) |", content)
    self.assertNotIn("News API aggregator", content)
    self.assertNotIn("News API (free tier)", content)
    self.assertNotIn("NewsApi", content)
    self.assertNotIn("newsapi", content)

  def test_architecture_doc_links_to_source_note(self):
    content = ARCH_DOC.read_text(encoding="utf-8")
    self.assertIn("[`docs/source-inventory-m4.md`](source-inventory-m4.md)", content)
    self.assertTrue(SOURCE_NOTE.exists())


if __name__ == "__main__":
  unittest.main()
