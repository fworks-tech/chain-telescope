import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.data.newsletter.store import save_subscription


class NewsletterStoreTests(unittest.TestCase):
    def test_save_subscription_writes_json(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            data_dir = Path(tmp_dir)
            subscriptions_file = data_dir / "newsletter_subscriptions.json"
            subscriptions_file.write_text("[]", encoding="utf-8")
            with patch("src.data.newsletter.store.DATA_DIR", data_dir):
                with patch("src.data.newsletter.store.SUBSCRIPTIONS_FILE", subscriptions_file):
                    record = save_subscription("user@example.com", "Weekly", "Summary")
                    self.assertEqual(record.email, "user@example.com")
                    payload = subscriptions_file.read_text(encoding="utf-8")
                    self.assertIn("user@example.com", payload)
