# Tasks: #74 — Replace feedparser with httpx + xml.etree.ElementTree

- [x] chore(deps): remove feedparser from requirements.txt
- [x] fix(news): replace feedparser.parse with httpx + xml.etree.ElementTree in ingestion.py
- [x] docs: update Architecture.md feedparser reference
- [x] docs: update 001-stack-recommendations.md feedparser reference
- [x] docs: update source-inventory-m4.md feedparser references
- [x] test: update test_source_inventory_note.py regex for new parser name
- [x] test: run full test suite to confirm nothing is broken
