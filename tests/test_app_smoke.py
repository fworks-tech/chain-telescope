import importlib
import pathlib
import unittest

from streamlit.testing.v1 import AppTest


class AppSmokeTests(unittest.TestCase):
    def test_app_imports(self):
        importlib.import_module("app")

    def test_src_modules_compile(self):
        root = pathlib.Path("src")
        for path in root.rglob("*.py"):
            compile(path.read_text(encoding="utf-8"), str(path), "exec")

    def test_dashboard_entry_renders_without_exception(self):
        app_test = AppTest.from_file("app.py")
        app_test.run(timeout=15)
        self.assertEqual(len(app_test.exception), 0)
        self.assertGreater(len(app_test.get("markdown")), 0)


if __name__ == "__main__":
    unittest.main()
