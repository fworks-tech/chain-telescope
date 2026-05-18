# Jupyter Crypto Wizard

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

Optional launcher from the repository root:

```powershell
.\scripts\run-app.ps1
```

```bash
python scripts/run_app.py
```

## Validation

Confirm the app behaves as expected before opening a pull request. The full automated and manual checklist lives in [`docs/validation-and-manual-qa.md`](docs/validation-and-manual-qa.md).

- [ ] `streamlit run app.py` starts without import errors
- [ ] Dashboard, Alerts, News, Risk, and Newsletter routes render in the browser
- [ ] Newsletter subscribe shows success for a valid email and an error for invalid input
- [ ] `python -m unittest discover -s tests -p 'test_*.py'` passes
- [ ] `ruff check app.py src tests` and `ruff format --check app.py src tests` pass when Ruff is installed locally
- [ ] `python -m unittest tests/test_source_inventory_note.py` passes for the M4 source inventory note contract

### M4 source inventory note

The planning note in [`docs/source-inventory-m4.md`](docs/source-inventory-m4.md) is guarded by local doc-contract tests:

```bash
python -m unittest tests/test_source_inventory_note.py
```

## AI Assistant (MVP)

The dashboard includes an **AI Assistant** panel for short, context-grounded Q&A about the current watchlist, time window, KPI snapshot, alerts, news snapshot, and trending highlights.

### Provider configuration

Use environment variables or Streamlit secrets (`.streamlit/secrets.toml`); do not commit keys.

- `OPENAI_API_KEY` (required for live model calls)
- `OPENAI_BASE_URL` (optional, default `https://api.openai.com/v1`)
- `OPENAI_MODEL` (optional, default `gpt-4o-mini`)
- `OPENAI_TIMEOUT_SECONDS` (optional, default `15`)

If credentials are missing, rate-limited, or provider calls fail, the assistant returns a safe local fallback summary instead of crashing.

### Provider and interface choice (current)

- **Interface now:** Python/Streamlit in-app chat panel (MVP).
- **Messenger channels (WhatsApp/Telegram):** out of scope for this issue and planned as a later delivery surface.
- **Provider strategy:** OpenAI-compatible endpoint so teams can compare providers by model quality, latency, and cost without changing UI flow. Use `OPENAI_BASE_URL` + `OPENAI_MODEL` for A/B comparisons.

### Product boundaries

- Assistant responses are informational, not financial advice
- No autonomous trading or exchange execution
- If context is missing, the assistant says so instead of inventing claims

### Follow-up mapping

- Source discovery follow-through: #22 and [`docs/source-inventory-m4.md`](docs/source-inventory-m4.md)
- Suggested next issues: chat persistence/history storage, retrieval/tool use against ingested datasets, and source citation rendering

### Assistant validation

- `python -m py_compile app.py src/components/assistant.py tests/test_assistant.py`
- `python -m unittest tests/test_assistant.py`

### Current limitations
- Market and feed providers fall back to mock or cached-safe output when remote configuration is unset or requests fail
- Newsletter delivery uses local persistence with a stub provider unless `NEWSLETTER_PROVIDER` and related secrets are configured
- Scheduled outbound jobs are not running in the repository yet

Optional environment variables and Streamlit secrets are documented in [`docs/configuration.md`](docs/configuration.md).

## CI

On push and pull request to `main`, `master`, and `feat/**`, GitHub Actions runs layered quality gates in [`.github/workflows/ci.yml`](.github/workflows/ci.yml):

| Job | What it enforces |
|-----|------------------|
| `test` | `python -m unittest discover -s tests -p 'test_*.py'` (validation, mock data helpers, assistant wiring, doc contracts, and a Streamlit `AppTest` smoke run) |
| `build` | `py_compile` on `app.py`, every `src/**/*.py` module, and routed `pages/**/*.py` entrypoints, plus a Streamlit entrypoint import smoke check |
| `lint` | Ruff lint and format checks on `app.py`, `src/`, and `tests/` (baseline in [`pyproject.toml`](pyproject.toml)) |
| `maintainability` | Advisory Ruff complexity and hygiene rules (`C901`, `ERA001`, `ARG001`); reports findings without blocking merges on day one |

Local equivalents after installing dependencies and Ruff (`python -m pip install ruff`):

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python - <<'PY'
import pathlib, py_compile
for path in [pathlib.Path("app.py"), *sorted(pathlib.Path("src").rglob("*.py")), *sorted(pathlib.Path("pages").rglob("*.py"))]:
    py_compile.compile(str(path), doraise=True)
PY
ruff check app.py src tests
ruff format --check app.py src tests
```

CI does not start a browser or run Playwright screenshot comparisons yet. See the **Visual regression** note in [`docs/Architecture.md`](docs/Architecture.md) for the deferred pilot path.

## Project Layout
- `app.py` — Streamlit UI entrypoint and navigation shell
- `pages/` — routed Dashboard, Alerts, News, Risk, and Newsletter pages
- `src/` — UI components, query layer, ingestion helpers, and validation
- `requirements.txt` — Python dependencies
- `docs/` — architecture, configuration, validation, and automation playbooks
- `CHANGELOG.md` — release history and milestone notes

## Documentation

- [`CHANGELOG.md`](CHANGELOG.md) — release history
- [`docs/Architecture.md`](docs/Architecture.md) — system structure and runtime flow
- [`docs/configuration.md`](docs/configuration.md) — environment variables and secrets
- [`docs/m4-data-pipelines.md`](docs/m4-data-pipelines.md) — dashboard snapshots, ingestion, alerts, and newsletter modules
- [`docs/validation-and-manual-qa.md`](docs/validation-and-manual-qa.md) — automated checks and manual smoke tests
- [`docs/source-inventory-m4.md`](docs/source-inventory-m4.md) — M4 source discovery research
- [`docs/agent-skills.md`](docs/agent-skills.md) — agent automation playbook

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
- [ ] `CHANGELOG.md` is updated when shipping a release

## License

MIT — see [`LICENSE`](LICENSE).

<!-- fworks-readme-footer v1 -->
## Links

- Repository: https://github.com/fworks-tech/Jupyter-Crypto-Wizard
- Portfolio: https://fworks.tech
<!-- /fworks-readme-footer v1 -->