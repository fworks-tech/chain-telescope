import importlib
import pathlib
import unittest


class AppSmokeTests(unittest.TestCase):
  def test_app_imports(self):
    importlib.import_module("app")

  def test_src_modules_compile(self):
    root = pathlib.Path("src")
    for path in root.rglob("*.py"):
      compile(path.read_text(encoding="utf-8"), str(path), "exec")


if __name__ == "__main__":
  unittest.main()
