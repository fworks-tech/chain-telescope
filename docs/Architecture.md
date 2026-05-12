# Architecture

This document describes how the Crypto Market Analyzer is structured today and how it is expected to evolve. For setup and run instructions, see [README.md](../README.md).

## Overview

The application is a Streamlit client with a thin entrypoint in [`app.py`](../app.py), routed pages under [`pages/`](../pages/), and UI modules under [`src/`](../src/). The browser talks to a Streamlit server that reruns the entry script on interaction. There is no separate backend service or job runner in the repository yet.

The product direction in [README.md](../README.md) calls for Python data pipelines, alerts, and newsletter automation. Market and feed ingestion modules are wired through a shared dashboard query layer with mock and remote fallbacks.

## Related documentation

- [configuration.md](configuration.md) — environment variables and secrets
- [m4-data-pipelines.md](m4-data-pipelines.md) — snapshot assembly, ingestion modules, and issue mapping
- [validation-and-manual-qa.md](validation-and-manual-qa.md) — automated checks and manual smoke tests
- [source-inventory-m4.md](source-inventory-m4.md) — M4 source discovery research

## Runtime flow

```mermaid
flowchart LR
  Browser[Browser]
  StreamlitServer[Streamlit server]
  AppPy[app.py]
  Pages[pages]
  QueryLayer[dashboard_query]
  Providers[market_and_news_modules]
  Components[src_components]

  Browser -->|HTTP| StreamlitServer
  StreamlitServer --> AppPy
  AppPy --> Pages
  Pages --> Components
  Components --> QueryLayer
  QueryLayer --> Providers
```

On each run, `app.py` configures the page, applies global styles, and delegates to `st.navigation` routes in `pages/`. Shared sidebar filters come from [`src/app_shell.py`](../src/app_shell.py). Dashboard panels consume a `DashboardSnapshot` from [`src/data/dashboard_query.py`](../src/data/dashboard_query.py).

## Module map

| Path | Role |
|------|------|
| [`app.py`](../app.py) | Streamlit entrypoint and navigation shell |
| [`pages/`](../pages/) | Routed Dashboard, Alerts, News, Risk, and Newsletter pages |
| [`src/app_shell.py`](../src/app_shell.py) | Sidebar branding, time window, and watchlist filters |
| [`src/styles.py`](../src/styles.py) | Global CSS injection |
| [`src/components/dashboard_header.py`](../src/components/dashboard_header.py) | Greeting and UTC snapshot caption |
| [`src/components/kpi_row.py`](../src/components/kpi_row.py) | KPI card row |
| [`src/components/price_trend.py`](../src/components/price_trend.py) | Price trend chart panel |
| [`src/components/trending_report.py`](../src/components/trending_report.py) | Trending report table |
| [`src/components/risk_graph.py`](../src/components/risk_graph.py) | Risk bar chart panel |
| [`src/components/feed_panels.py`](../src/components/feed_panels.py) | Alerts and news snapshot panels |
| [`src/components/assistant.py`](../src/components/assistant.py) | In-app GPT assistant with safe fallbacks |
| [`src/components/newsletter.py`](../src/components/newsletter.py) | Newsletter subscription form and saved subscriptions |
| [`src/data/dashboard_query.py`](../src/data/dashboard_query.py) | Filter-aware dashboard snapshot assembly |
| [`src/data/mock_market.py`](../src/data/mock_market.py) | Mock market series, table, and risk inputs |
| [`src/data/market/`](../src/data/market/) | Market provider adapters and fallback orchestration |
| [`src/data/news/`](../src/data/news/) | Feed ingestion and normalized feed models |
| [`src/data/alerts/rules.py`](../src/data/alerts/rules.py) | MVP threshold rules for alert output |
| [`src/data/newsletter/`](../src/data/newsletter/) | Local subscription persistence and stub delivery |
| [`src/validation/email.py`](../src/validation/email.py) | Newsletter email validation |

Import flow: routed pages import view renderers and shared filters. Views call `load_dashboard_snapshot(time_window, watchlist)` and pass the snapshot into components.

## UI composition

### Sidebar

The sidebar shows branding, a time-window select box, and a watchlist multiselect. Navigation is owned by `st.navigation` in `app.py`, not by a decorative radio group.

### Routed pages

- **Dashboard:** header, KPI cards, price trend, trending report, risk graph, alerts/news snapshots, and assistant chat
- **Alerts:** rule-driven alert output and configured rule documentation
- **News:** normalized feed items with safe fallback
- **Risk:** risk graph for the selected window
- **Newsletter:** subscribe form, local persistence, and stub delivery messaging

Styling uses injected CSS for cards and panels; layout uses Streamlit columns.

## Filter-to-data flow

1. Sidebar widgets in `src/app_shell.py` return `time_window` and `watchlist`.
2. `load_dashboard_snapshot()` maps the time window to a day count and selects the primary watchlist asset for the price chart.
3. Market adapters in `src/data/market/` attempt remote providers, then fall back to mock series in `src/data/mock_market.py`.
4. News ingestion in `src/data/news/` loads RSS/Atom feeds or fallback items and filters by watchlist tags/titles when possible.
5. Alert rules in `src/data/alerts/rules.py` evaluate threshold conditions over the selected price series.
6. Components and the assistant consume the same snapshot so visible panels and fallback chat context stay aligned.

See [m4-data-pipelines.md](m4-data-pipelines.md) for module-level detail.

## Data today vs planned

| Area | Today | Planned |
|------|-------|---------|
| Market KPIs | Filter-aware mock values with optional provider-backed price series | Cached live market metrics and broader KPI coverage |
| Price trend | Binance/CoinGecko adapters with mock fallback | Cached OHLCV per watchlist asset and multi-asset overlays |
| Trending report | Watchlist-filtered mock table | Computed rankings and sentiment from pipeline output |
| Risk graph | Window-adjusted mock scores | Derived risk model inputs and history |
| Alerts and news | Rule-driven alerts plus ingested or fallback feed items | Broader rules engine and richer investor/developer signals |
| Assistant | Optional OpenAI-compatible chat over dashboard snapshot context | Tool use and retrieval over ingested datasets |
| Newsletter | Local persistence with stub delivery | Scheduled generation and outbound delivery |
| Sidebar filters | Drive dashboard snapshots and page queries | Additional query dimensions as ingestion matures |

Assistant, market, feed, and newsletter settings are optional. Full variable lists and defaults are in [configuration.md](configuration.md).

When provider values are absent or remote calls fail, the app falls back to mock or cached-safe output instead of hard failure.

M4 source discovery for market, feed, investor, and developer inputs is documented in [`docs/source-inventory-m4.md`](source-inventory-m4.md).

## Dependencies

| Package | Role today | Role planned |
|---------|------------|--------------|
| `streamlit` | UI shell, widgets, layout | Same |
| `pandas` | Trending table and rolling mean on price series | Pipeline transforms and report tables |
| `plotly` | Price trend and risk charts | Same |
| `requests` | Assistant and market provider HTTP calls | HTTP market and news sources |
| `feedparser` | RSS/Atom ingestion with fallback | Expanded feed ingestion |
| `schedule` | Not used in `app.py` | Periodic jobs (reports, newsletter) |
| `pydantic` | Market and feed models | Validated config and API models |
| `python-dotenv` | Local provider and newsletter configuration | Local and deployment secrets |

CI and local setup install the full [`requirements.txt`](../requirements.txt).

## Repository boundaries

| Path | Role |
|------|------|
| [`app.py`](../app.py) | Production UI entrypoint |
| [`pages/`](../pages/) | Streamlit routed pages |
| [`src/`](../src/) | Streamlit UI modules, query layer, ingestion helpers, and validation |
| [`requirements.txt`](../requirements.txt) | Python dependencies |
| [`docs/`](../docs/) | Architecture, configuration, validation, and automation playbooks |

## Automation

- **CI** ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)): on push and pull request to `main`, `master`, and `feat/**`, installs dependencies on Python 3.11, compiles `app.py` and `src/**/*.py`, imports the Streamlit entrypoint, and runs unit tests. It does not start Streamlit or run browser tests.
- **Dev Container** ([`.devcontainer/devcontainer.json`](../.devcontainer/devcontainer.json)): installs dependencies via `updateContentCommand` on create and update. Streamlit is not started automatically; run `streamlit run app.py` from the repository root after the container is ready.

Manual and automated validation steps are listed in [validation-and-manual-qa.md](validation-and-manual-qa.md).

## Evolution

Near-term architecture aligned with [README.md](../README.md) product scope:

- Expand provider coverage and caching for market and feed ingestion
- Add richer alert scoring and investor/developer signal inputs
- Add scheduled workers for newsletter generation and alert evaluation, using packages already listed in `requirements.txt`
- Keep active code at the repo root, under `src/`, under `pages/`, and under `docs/`
