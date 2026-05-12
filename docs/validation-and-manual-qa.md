# Validation and manual QA

This document describes automated checks and manual smoke tests for the Streamlit app after M4 backlog changes. CI behavior is defined in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).

## Automated checks

From the repository root with dependencies installed:

```bash
python -m py_compile app.py
python -m py_compile src/data/dashboard_query.py
python -c "import importlib; importlib.import_module('app')"
python -m unittest discover -s tests -p 'test_*.py' -v
```

CI on push and pull request to `main`, `master`, and `feat/**`:

- Installs `requirements.txt` on Python 3.11
- Compiles `app.py` and every `src/**/*.py` file
- Imports the Streamlit entrypoint
- Runs all `tests/test_*.py` modules

CI does not start Streamlit or run browser automation.

### Focused test modules

| Test file | Covers |
|---|---|
| `tests/test_app_smoke.py` | Entrypoint import and `src/` compile |
| `tests/test_m4_modules.py` | Dashboard query, market fallback, news fallback, alert rules |
| `tests/test_newsletter_store.py` | Local subscription persistence |
| `tests/test_assistant.py` | Assistant context and provider fallback |
| `tests/test_source_inventory_note.py` | M4 source inventory doc contract |

## Manual Streamlit smoke test

```bash
streamlit run app.py
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
- [Architecture.md](Architecture.md)
- [configuration.md](configuration.md)
- [m4-data-pipelines.md](m4-data-pipelines.md)
