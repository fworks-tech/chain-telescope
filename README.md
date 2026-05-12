# Crypto Market Analyzer

A modern platform for crypto intelligence, built to transform noisy market data into practical decisions.

## Purpose
This project delivers a focused crypto analysis experience with:
- Market monitoring and watchlists
- Alerts and threshold notifications
- News aggregation and signal extraction
- Trending reports
- Risk and volatility graphs
- Email newsletter for subscribers

## Near-Term Product Scope
- Dashboard with key market KPIs
- Live trend charting and risk panels
- Alerts feed and configurable rules
- Curated market-news stream
- Scheduled newsletter generation

## Future Features (Far-Future)
- WhatsApp conversational delivery with same content from the web platform
- Buy/sell execution through partner exchanges

## Tech Direction
- Streamlit UI client for fast iteration
- Python data pipelines for market/news ingestion
- CI automation and agent-driven repository workflows

## Prerequisites
- Python 3.11
- Git
- Optional: VS Code Dev Containers or GitHub Codespaces

## Quick Start

Clone the repository and create a virtual environment from the repository root.

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in the terminal (default: http://localhost:8501).

## Validation

Confirm the app behaves as expected before opening a pull request:

- [ ] `streamlit run app.py` starts without import errors
- [ ] Dashboard, charts, and tables render in the browser
- [ ] Newsletter subscribe shows success for a valid email and an error for invalid input
- [ ] `python -m py_compile app.py` passes (same compile check as CI)

### Current limitations
- Demo and mock data in `app.py`, not live market feeds
- Sidebar navigation labels are not separate routed pages yet
- Several packages in `requirements.txt` are reserved for future pipelines and are not used by `app.py` today

## CI

On push and pull request to `main`, `master`, and `feat/**`, GitHub Actions installs `requirements.txt` and compiles `app.py`. See [`.github/workflows/ci.yml`](.github/workflows/ci.yml). CI does not start Streamlit or run browser tests.

## Project Layout
- `app.py` — Streamlit UI entrypoint
- `requirements.txt` — Python dependencies
- `docs/` — architecture and automation playbooks

## Architecture

System structure, runtime flow, data boundaries, and planned evolution are documented in [`docs/Architecture.md`](docs/Architecture.md).

## Contributing

- Use [conventional commit](https://www.conventionalcommits.org/) messages
- Fill out [`.github/pull_request_template.md`](.github/pull_request_template.md) when opening a pull request
- Do not commit secrets or API keys
- Update README or architecture docs when setup or behavior changes

## Checklists

### First-time setup
- [ ] Clone the repository and `cd` into the root
- [ ] Install Python 3.11
- [ ] Create and activate a virtual environment
- [ ] Upgrade `pip` and install `requirements.txt`

### Run and smoke test
- [ ] Run `streamlit run app.py`
- [ ] Confirm the dashboard loads in the browser
- [ ] Confirm charts and tables render
- [ ] Exercise newsletter subscribe with valid and invalid email
- [ ] Run `python -m py_compile app.py`

### Optional Dev Container
- [ ] Reopen the repository in a Dev Container or Codespaces
- [ ] Confirm dependencies install on container create or update
- [ ] Run `streamlit run app.py` manually from the repository root

### Before opening a PR
- [ ] Choose change type and scope in the pull request template
- [ ] Record validation: local run, CI checks, and manual QA as applicable
- [ ] Use a conventional commit message
- [ ] Update README or docs if setup or behavior changed
- [ ] Confirm no secrets were added
- [ ] Mark the pull request ready for review

### Release / docs gate
- [ ] README explains how to run and validate the app
- [ ] CI is green on the branch
- [ ] Changelog or update notes are prepared when shipping a release

## License

MIT — see [`LICENSE`](LICENSE).
