# Tasks: Vercel FastAPI + React SPA (MVP)

- [x] chore(config): add `[tool.vercel] entrypoint = "src.api:app"` to pyproject.toml
- [x] chore(config): create vercel.json with route rules for FastAPI + SPA
- [x] feat(frontend): scaffold Vite + React + TypeScript project under frontend/
- [x] feat(frontend): add api/client.ts — typed fetch wrapper for FastAPI endpoints
- [x] feat(frontend): add Layout.tsx with navigation (Dashboard, News, Risk, Assistant, Alerts, Newsletter)
- [x] feat(frontend): add Dashboard page — KPI row, price trend chart, news feed, risk graph, alerts panel, trending report placeholder
- [x] feat(frontend): add KpiRow component (from streamlit kpi_row.py reference)
- [x] feat(frontend): add PriceTrendChart component (Recharts)
- [x] feat(frontend): add NewsFeed component (list with tags, source, date)
- [x] feat(frontend): add RiskGraph component (bar chart)
- [x] feat(frontend): add AlertsPanel component (alert list with severity badges)
- [x] feat(frontend): add News page — full news feed with filtering
- [x] feat(frontend): add Risk page — risk breakdown
- [x] feat(frontend): add Alerts page — Coming Soon placeholder
- [x] feat(frontend): add Newsletter page — Coming Soon placeholder
- [x] feat(frontend): add Assistant page — Coming Soon placeholder (no backend endpoint yet)
- [x] feat(frontend): add sidebar filters placeholder notice in Layout
- [x] chore(config): update CORS_ORIGINS in FastAPI to allow Vite dev server
- [x] docs: update Architecture.md with new FastAPI + React architecture
- [x] docs: write ADR-003 for FastAPI + React on Vercel decision
- [x] test: verify 74 tests still pass
- [x] test: verify Vercel deployment builds and serves SPA + API

## Phase 2 — Tracked Issues

- [#98](https://github.com/fworks-tech/hasheyes/issues/98) — Trending Report table component
- [#99](https://github.com/fworks-tech/hasheyes/issues/99) — Sidebar filters (time window, watchlist, source, trend)
- [#100](https://github.com/fworks-tech/hasheyes/issues/100) — Alerts standalone page
- [#101](https://github.com/fworks-tech/hasheyes/issues/101) — Newsletter page with subscribe form
- [#102](https://github.com/fworks-tech/hasheyes/issues/102) — Assistant API endpoint in FastAPI
