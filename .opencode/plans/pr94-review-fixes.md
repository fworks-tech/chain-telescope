# PR #94 Review Findings — Implementation Plan

**Branch:** Create `feat/094-review-fixes` from `feat/002-ccxt-exchange` (or from `main` after merge)

## Findings organized by priority

### [blocking] 1. CORS `allow_origins=["*"]`

**File:** `src/api.py:8-13`

**Fix:** Make CORS origins configurable via env var:

```python
import os
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8501").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Why:** `["*"]` permits any website to call the API. For self-hosted VPS behind Nginx it's acceptable, but for production with public access it exposes snapshot data, alerts, subscriptions. Making it env-var-configurable means it's locked down by default for the Next.js frontend but easy to open for development.

---

### [suggestion] 2. POST endpoint uses Query params instead of Body

**File:** `src/api.py:107-118`

**Fix:** Change `Query(...)` to `Body(...)`:

```python
from fastapi import Body

@app.post("/api/newsletter/subscribe")
def subscribe(
    email: str = Body(..., embed=True),
    frequency: str = Body("Weekly"),
    format: str = Body("Summary"),
):
```

**Why:** POST endpoints conventionally accept JSON bodies, not query parameters. Clients sending `Content-Type: application/json` with `{"email": "..."}` will fail with the current implementation.

---

### [suggestion] 3. No global exception handler

**File:** `src/api.py`

**Fix:** Add global exception handler that returns JSON 500 instead of traceback:

```python
from fastapi.responses import JSONResponse
from loguru import logger

@app.exception_handler(Exception)
async def global_handler(request, exc):
    logger.warning("API error on {}: {}", request.url.path, exc)
    return JSONResponse(status_code=500, content={"error": "Internal server error"})
```

**Why:** Without this, unhandled exceptions return FastAPI's default HTML error page with full traceback, which leaks internal paths and code structure to API consumers.

---

### [suggestion] 4. `_provider_chain` duplicates `EXCHANGE_NAMES`

**File:** `src/data/market/service.py:31-38`

**Fix:** Refactor to use `EXCHANGE_NAMES` as the single source of truth:

```python
def _provider_chain(provider: str) -> list[str]:
    if provider in EXCHANGE_NAMES:
        return [provider]
    return list(EXCHANGE_NAMES)
```

**Why:** Adding a new exchange currently requires updates in two places (`EXCHANGE_NAMES` tuple and `_provider_chain` if/elif chain). This eliminates the duplication.

---

### [question] 5. Import datetime inside function body

**File:** `src/data/market/ccxt_adapter.py:37`

**Fix:** Move `import datetime` to module level:

```python
import datetime

import ccxt
from tenacity import retry, stop_after_attempt, wait_exponential
```

**Why:** Top-level imports are the Python convention. No benefit to deferring a stdlib import inside a function.

---

### [suggestion] 6. No limit parameter on `/api/news`

**File:** `src/api.py:75-92`

**Fix:** Add `?limit` query parameter:

```python
@app.get("/api/news")
def news(
    watchlist: str = Query("BTC"),
    limit: int = Query(10, description="Max items to return"),
):
    from src.data.news.ingestion import load_news_items
    items = load_news_items(watchlist=[a.strip() for a in watchlist.split(",") if a.strip()])
    items = items[:max(limit, 1)]
    return [...]
```

**Why:** Without a limit, the endpoint returns ALL news items (potentially 40+ from both RSS feeds). For a dashboard widget, 5-10 items is sufficient.

---

### [suggestion] 7. 5/8 API endpoints untested

**File:** `tests/test_api.py`

**Add tests for:**

```python
class ApiPriceTrendTests(unittest.TestCase):
    @patch("src.data.market.service.fetch_ccxt_series")
    def test_price_trend_returns_expected_structure(self, mock_ccxt):
        mock_ccxt.return_value = ([datetime(2024, 1, 1)], [100.0], "binance")
        resp = client.get("/api/price-trend?asset=BTC&days=30")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("prices", data)
        self.assertIn("asset", data)
        self.assertEqual(data["source"], "binance")

class ApiNewsTests(unittest.TestCase):
    @patch("src.data.news.ingestion._parse_feed", return_value=[])
    def test_news_returns_fallback_items(self, _mock_parse):
        resp = client.get("/api/news?watchlist=BTC")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)

class ApiAlertsTests(unittest.TestCase):
    @patch("src.data.market.service.fetch_ccxt_series", return_value=None)
    def test_alerts_returns_structure(self, _mock_ccxt):
        resp = client.get("/api/alerts?window=30D&assets=BTC")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("alerts", resp.json())

class ApiNewsletterTests(unittest.TestCase):
    def test_subscribe_rejects_invalid_email(self):
        resp = client.post("/api/newsletter/subscribe?email=invalid")
        self.assertEqual(resp.status_code, 422)  # FastAPI validation error
```

**Total new tests:** ~8

---

## Implementation order

| Step | What | Files | Est. time |
|------|------|-------|-----------|
| 1 | CORS origins → env var | `src/api.py` | 5min |
| 2 | POST subscribe → Body() | `src/api.py` | 5min |
| 3 | Global exception handler | `src/api.py` | 5min |
| 4 | Import datetime → top level | `src/data/market/ccxt_adapter.py` | 1min |
| 5 | Refactor _provider_chain | `src/data/market/service.py` | 5min |
| 6 | Add limit to /api/news | `src/api.py` | 5min |
| 7 | Add 8 new API tests | `tests/test_api.py` | 15min |
| 8 | Quality gates | lint + format + 66 tests | 2min |

**Total:** ~40 minutes

## Verification

```powershell
python -m ruff check app.py src tests
python -m ruff format --check app.py src tests
python -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: 66 tests pass (was 58, +8 new API tests).
