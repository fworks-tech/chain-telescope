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
    self.assertIn("| #14 | Wire sidebar filters to dashboard data queries", content)
    self.assertIn("| #15 | Implement market ingestion adapter", content)
    self.assertIn("| #16 | Implement news/feed ingestion normalization", content)
    self.assertIn("| #17 | Build alert rules over normalized market", content)
    self.assertIn("| #18 | Implement newsletter persistence/delivery", content)

  def test_newsapi_name_is_consistent(self):
    content = SOURCE_NOTE.read_text(encoding="utf-8")
    self.assertIn("NewsAPI (free tier)", content)
    self.assertNotIn("News API aggregator", content)

  def test_architecture_doc_links_to_source_note(self):
    content = ARCH_DOC.read_text(encoding="utf-8")
    self.assertIn("[`docs/source-inventory-m4.md`](source-inventory-m4.md)", content)


if __name__ == "__main__":
  unittest.main()
