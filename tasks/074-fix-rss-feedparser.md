# Tasks: #74 — Replace feedparser with httpx + xml.etree.ElementTree

- [ ] chore(deps): remove feedparser from requirements.txt
- [ ] fix(news): replace feedparser.parse with httpx + xml.etree.ElementTree in ingestion.py
- [ ] docs: update Architecture.md feedparser reference
- [ ] docs: update 001-stack-recommendations.md feedparser reference
- [ ] docs: update source-inventory-m4.md feedparser references
- [ ] test: update test_source_inventory_note.py regex for new parser name
- [ ] test: run full test suite to confirm nothing is broken
