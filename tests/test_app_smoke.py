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

    def test_sidebar_nav_changes_rendered_sections(self):
        app_test = AppTest.from_file("app.py")
        app_test.run(timeout=15)
        self.assertEqual(app_test.get("radio")[0].value, "Dashboard")
        self.assertGreater(len(app_test.get("plotly_chart")), 0)

        app_test.get("radio")[0].set_value("Alerts")
        app_test.run(timeout=15)
        self.assertEqual(app_test.get("radio")[0].value, "Alerts")
        self.assertEqual(len(app_test.get("plotly_chart")), 0)
        self.assertTrue(any("Alerts" in item.value for item in app_test.get("markdown")))

    def test_greeting_is_not_hardcoded_to_single_user(self):
        app_test = AppTest.from_file("app.py")
        app_test.run(timeout=15)
        self.assertFalse(any("Richard" in item.value for item in app_test.get("markdown")))


if __name__ == "__main__":
    unittest.main()
