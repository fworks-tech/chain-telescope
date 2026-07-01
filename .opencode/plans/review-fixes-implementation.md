# Review Fixes — Implementation Plan

**Branch:** `feat/001-review-fixes` (already created from `staging`)

## Step 1 — Create `src/logging.py`

New file with loguru sink configuration:

```python
import sys
from loguru import logger

def setup_logging():
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="WARNING",
        colorize=True,
    )
```

## Step 2 — Wire into `app.py`

Add after imports:

```python
from src.logging import setup_logging
setup_logging()
```

## Step 3 — Remove Streamlit dependency from data layer

**`src/data/dashboard_query.py`:**
- Remove `import streamlit as st`
- Remove `@st.cache_data(ttl=30)` decorator from `load_dashboard_snapshot`

**Create/update `src/views/__init__.py`:**
```python
import streamlit as st

@st.cache_data(ttl=30)
def cached_dashboard_snapshot(*args, **kwargs):
    from src.data.dashboard_query import load_dashboard_snapshot
    return load_dashboard_snapshot(*args, **kwargs)
```

## Step 4 — Update callers

Replace `from src.data.dashboard_query import load_dashboard_snapshot` with `from src.views import cached_dashboard_snapshot` in:

- `src/views/dashboard_view.py` (line 9) — rename calls from `load_dashboard_snapshot` to `cached_dashboard_snapshot`
- `src/views/alerts_view.py` (line 3) — same rename
- `src/views/news_view.py` (line 2) — same rename
- `src/views/risk_view.py` (line 3) — same rename
- `src/components/assistant.py` (line 7) — update import, rename `_build_context` call

**Exception:** `dashboard_view.py` and `_build_context` in `assistant.py` currently call `load_dashboard_snapshot(...)` — rename to `cached_dashboard_snapshot(...)`.

## Step 5 — Add test files

**`tests/test_caching.py`:**
- `test_snapshot_cached_within_ttl` — mock fetch, call twice, assert same object, assert fetch called once

**`tests/test_retry.py`:**
- `test_binance_retries_on_failure` — mock requests.get to fail twice then succeed, assert 3 calls
- `test_binance_returns_none_no_symbol` — verify None is returned for unknown asset
- `test_coingecko_retries_on_failure` — same pattern
- `test_coinbase_retries_on_failure` — same pattern

**`tests/test_logging.py`:**
- `test_logger_warning_on_market_provider_failure` — mock logger.warning, verify called on provider fail
- `test_logger_warning_on_news_feed_failure` — mock logger.warning, verify called on feed parse fail

## Step 6 — Quality gates

```powershell
python -m ruff check src tests
python -m ruff format --check src tests
python -m unittest discover -s tests -p 'test_*.py' -v
```

## Step 7 — Commit and PR

```powershell
git add -A
git commit -m "fix(data): address review findings — loguru sink, cache wrapper, tests"

# Answer to Finding 4 (retry placement):
#   Per-provider retry kept intentional. 429 handling deferred.
#   See PR description for rationale.

git push origin feat/001-review-fixes
gh pr create --base staging --head feat/001-review-fixes --title "fix(data): address review findings — loguru sink, cache wrapper, tests"
```
