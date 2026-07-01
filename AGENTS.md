# ChainTelescope — Agent Guide

## Quick start
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Quality gates (run in order)
1. **Lint** — `ruff check app.py src tests`
2. **Format check** — `ruff format --check app.py src tests`
3. **Compile check** — `python -m py_compile app.py` + all `src/**/*.py` + `pages/**/*.py`
4. **Test** — `python -m unittest discover -s tests -p 'test_*.py' -v`

CI runs these in parallel jobs (`test`, `build`, `lint`). A `maintainability` job runs advisory rules (`C901,ERA001,ARG001`) but does not block.

## Project structure
- `app.py` — Streamlit entrypoint, `st.navigation` shell
- `pages/` — thin stubs delegating to `src/views/`
- `src/views/` — actual view renderers composing `src/components/`
- `src/components/` — 10 modules: assistant, chart_theme, dashboard_header, feed_panels, kpi_row, newsletter, price_trend, risk_graph, trending_report
- `src/app_shell.py` — sidebar filter engine (time window, watchlist, market source, trend filter)
- `src/styles.py` — global CSS injection
- `src/data/` — dashboard query, market providers (binance/coingecko/coinbase), news, alerts, mock
- `src/data/assets.py` — 100+ asset symbols with CoinGecko/Coinbase/Binance ID mappings
- `src/validation/email.py` — email validation (`@` and `.` check)
- `src/logging.py` — structured loguru sink configuration
- `src/views/__init__.py` — cached dashboard snapshot wrapper (`@st.cache_data(ttl=30)`)
- `tests/` — unittest files (no pytest)
- `notebooks/` — Jupyter notebooks for EDA, strategies, reports
- `docs/` — architecture, configuration, deployment, operations, development guide
- `scripts/pr-skill.py` — PR automation tool (create/validate/summary)

## Ruff conventions
- `pyproject.toml` config: line-length=100, target-version=py311, double quotes, space indentation
- Rules: `E,F,I,UP,B` (ignore `E501`)
- Run on: `app.py src tests`

## Testing quirks
- Uses **unittest** only (no pytest). Do not add pytest fixtures or decorators.
- Streamlit `AppTest` smoke tests in `test_app_smoke.py` render the full UI.
- Market/news data falls back to mock when remote providers are unavailable — no live API keys needed.
- Doc-contract test: `python -m unittest tests/test_source_inventory_note.py`
- New test files: `test_caching.py`, `test_retry.py`, `test_logging.py` (43 total, was 35)

## Config & secrets
- Loading order: Streamlit secrets (`.streamlit/secrets.toml`) → env vars → defaults
- `.env`, `.streamlit/secrets.toml` are gitignored — never commit them
- OpenAI assistant vars: `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `OPENAI_TIMEOUT_SECONDS`
- Market source: `MARKET_PROVIDER` env var or sidebar filter (`auto`/`binance`/`coingecko`/`coinbase`/`mock`)
- Auto fallback chain: Binance → CoinGecko → Coinbase → mock
- Provider base URLs: `BINANCE_BASE_URL`, `COINGECKO_BASE_URL`, `MARKET_REQUEST_TIMEOUT_SECONDS`
- News feeds: `NEWS_FEED_URLS` (default CoinDesk + Cointelegraph RSS)
- Newsletter: `NEWSLETTER_PROVIDER` (stub by default), `NEWSLETTER_DATA_DIR`, `NEWSLETTER_API_KEY`
- Subscriptions stored in `data/newsletter_subscriptions.json`
- See `docs/configuration.md` for all options

## Workflow conventions
- **Conventional commits** required
- PR template at `.github/pull_request_template.md` — fill all sections
- Update `CHANGELOG.md` for user-visible changes
- Dev container at `.devcontainer/devcontainer.json` (universal:2 image; run `streamlit run app.py` manually)
- PR automation: `python scripts/pr-skill.py create|validate|summary`

## Known gotchas
- No typechecking in CI (mypy not configured)
- No pre-commit hooks
- `src/data/` is source code; runtime data goes to `data/` (gitignored)
- Sidebar has 4 controls: Time Window, Watchlist, Market Source, Trend Filter
- `app.py` uses `st.navigation` → `pages/`; the modular architecture is fully wired
- Notebooks import from `src/` — run from repo root with `sys.path` setup
- **Repo name is ChainTelescope** — evolved from HashHelm
