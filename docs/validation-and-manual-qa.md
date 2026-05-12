# Validation and manual QA

This document describes automated checks and manual smoke tests for the Streamlit app after M4 backlog changes. CI behavior is defined in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml). Release history is tracked in [`CHANGELOG.md`](../CHANGELOG.md).

## Latest validation run

**Date:** 2026-05-12  
**Branch:** `main`  
**Commit:** `5a9a8a9`  
**Environment:** local Windows, Python 3.11, `http://localhost:8501`

### Automated checks

- [x] `py_compile` for `app.py`, `src/**/*.py`, and `pages/**/*.py`
- [x] Streamlit entrypoint import smoke check
- [x] `python -m unittest discover -s tests -p 'test_*.py' -v` (27 tests)
- [x] `ruff check app.py src tests`
- [x] `ruff format --check app.py src tests`

### Manual Streamlit smoke test

- [x] Dashboard, Alerts, and News routes render distinct content with sidebar branding
- [x] Dashboard panels render without traceback, including KPI cards, price trend, trending table, risk graph, alerts snapshot, news snapshot, and assistant input
- [x] Alerts page shows active alerts and configured MVP rules
- [x] News page renders a feed table with source, published, and title columns
- [ ] Risk route verified in browser
- [ ] Newsletter subscribe flow verified in browser
- [ ] Sidebar filter changes verified interactively in browser
- [ ] Assistant response verified against the current watchlist and time window in browser

### Provider spot checks

- [x] Default market path returned live Binance-backed price trend data during the smoke run
- [ ] `MARKET_PROVIDER=coingecko` spot check
- [ ] `OPENAI_API_KEY` live assistant response check
- [ ] Missing-provider fallback spot check with network disabled

## Automated checks

From the repository root with dependencies installed:

```bash
python -m py_compile app.py
python - <<'PY'
import pathlib, py_compile
for path in [pathlib.Path("app.py"), *sorted(pathlib.Path("src").rglob("*.py")), *sorted(pathlib.Path("pages").rglob("*.py"))]:
    py_compile.compile(str(path), doraise=True)
PY
python -c "import importlib; importlib.import_module('app')"
python -m unittest discover -s tests -p 'test_*.py' -v
ruff check app.py src tests
ruff format --check app.py src tests
```

CI on push and pull request to `main`, `master`, and `feat/**`:

- Installs `requirements.txt` on Python 3.11
- Runs `unittest` discovery for all `tests/test_*.py` modules, including a Streamlit `AppTest` smoke run
- Compiles `app.py`, every `src/**/*.py` file, and routed `pages/**/*.py` entrypoints
- Imports the Streamlit entrypoint
- Runs Ruff lint and format checks on `app.py`, `src/`, and `tests/`
- Reports advisory maintainability findings without blocking merges on day one

CI does not start Streamlit or run browser automation.

### Focused test modules

| Test file | Covers |
|---|---|
| `tests/test_app_smoke.py` | Entrypoint import, `src/` compile, and Streamlit `AppTest` smoke run |
| `tests/test_m4_modules.py` | Dashboard query, market fallback, news fallback, alert rules |
| `tests/test_mock_market.py` | Mock market helpers and snapshot line helpers |
| `tests/test_feed_panels.py` | Escaped news rendering in feed panels |
| `tests/test_newsletter_store.py` | Local subscription persistence |
| `tests/test_email_validation.py` | Newsletter email validation |
| `tests/test_assistant.py` | Assistant context and provider fallback |
| `tests/test_source_inventory_note.py` | M4 source inventory doc contract |

## Manual Streamlit smoke test

```bash
streamlit run app.py
```

Optional launcher from the repository root:

```powershell
.\scripts\run-app.ps1
```

```bash
python scripts/run_app.py
```

Open the local URL (default `http://localhost:8501`).

### Navigation

- [ ] Dashboard, Alerts, News, Risk, and Newsletter each show distinct content
- [ ] Global styling and sidebar branding appear on filter-backed pages

### Sidebar filters

- [ ] Changing time window updates KPI values, risk scores, and price series length or source caption
- [ ] Changing watchlist updates trending rows and the primary asset label on the price chart
- [ ] Assistant answers reference the same watchlist and time window shown in the sidebar

### Dashboard

- [ ] KPI cards, price trend, trending table, risk graph, alerts snapshot, news snapshot, and assistant render without traceback

### Alerts

- [ ] Active alerts list renders
- [ ] Configured MVP rules are documented on the page

### News

- [ ] Feed table renders with title and URL columns
- [ ] Disconnecting from feeds or using invalid URLs still leaves fallback content visible

### Newsletter

- [ ] Valid email subscribe persists and shows stub delivery messaging
- [ ] Invalid email shows validation error
- [ ] Saved subscriptions list updates after a successful subscribe

## Provider spot checks

Optional checks with network access:

- [ ] With default settings, market requests fall back to mock data when providers are unreachable
- [ ] With `MARKET_PROVIDER=binance` or `coingecko`, price trend source caption reflects the provider when data returns
- [ ] With `OPENAI_API_KEY` set, assistant returns provider content; without it, fallback text appears

## Related docs

- [README.md](../README.md)
- [CHANGELOG.md](../CHANGELOG.md)
- [Architecture.md](Architecture.md)
- [configuration.md](configuration.md)
- [m4-data-pipelines.md](m4-data-pipelines.md)
