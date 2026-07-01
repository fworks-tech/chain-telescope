# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Planned follow-ups: scheduled newsletter jobs, outbound delivery providers, and browser-based visual regression in CI.

### Changed

- None.

## [0.2.0] - 2026-05-12

### Added

- Routed Streamlit navigation for Dashboard, Alerts, News, Risk, and Newsletter pages.
- Shared sidebar filters in `src/app_shell.py` for time window and watchlist selection.
- Filter-aware `DashboardSnapshot` assembly in `src/data/dashboard_query.py`.
- Market ingestion adapters with Binance and CoinGecko fallbacks to mock data.
- RSS/Atom news ingestion with normalized feed items and safe fallback content.
- MVP alert rules and local newsletter persistence with stub delivery.
- AI assistant grounding from the shared dashboard snapshot with provider fallbacks.
- Launcher helpers in `scripts/run-app.ps1` and `scripts/run_app.py`.
- Expanded unit and smoke coverage, including Streamlit `AppTest` entrypoint checks.
- Layered CI jobs for tests, compile checks, Ruff lint/format, and advisory maintainability rules.
- Documentation for configuration, M4 pipelines, validation, and manual QA.

### Changed

- Modularized the dashboard into routed pages, views, and snapshot-driven components.
- Hardened feed rendering by escaping untrusted news titles in HTML panels.
- Normalized provider timestamps in market service output for chart consistency.

### Removed

- Legacy single-page sidebar navigation component in favor of `st.navigation` routes.

## [0.1.0] - 2026-05-12

### Added

- Initial Streamlit dashboard baseline in `app.py`.
- README runbook, validation checklists, and `docs/Architecture.md`.
- Python ignore rules for virtual environments, caches, and local env files.

[Unreleased]: https://github.com/fworks-tech/hashhelm/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/fworks-tech/hashhelm/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/fworks-tech/hashhelm/releases/tag/v0.1.0
