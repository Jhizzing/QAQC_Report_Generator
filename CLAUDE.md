# CLAUDE.md — LogiQore Reporter

> Project context file for Claude Code. Place in the repository root (`QAQC_Report_Generator/CLAUDE.md`).

---

## Project Overview

**LogiQore Reporter** is a QAQC (Quality Assurance / Quality Control) analysis tool for geological laboratory data. It evaluates standards (CRMs), blanks, and duplicates from drilling programs, then generates professional PDF, Excel, and Word reports with statistical analysis and visualizations.

The product ships as:
- **Desktop app** — PyQt6 GUI + CLI, packaged via PyInstaller for Windows/macOS/Linux
- **Web app** — React 19 frontend + FastAPI backend (the primary interface going forward)
- **Marketing website** — separate repo (`logiqore-website`), Next.js on Vercel at logiqore.io

**Owner:** Patrick Thomas Hann (@Jhizzing)
**License:** MIT
**Repo:** `github.com/Jhizzing/QAQC_Report_Generator` (private)
**Website repo:** `github.com/Jhizzing/logiqore-website` (public)

---

## Architecture

```
QAQC_Report_Generator/
├── src/                          # Python backend (core logic)
│   ├── data/                     # Data import, processing, CRM management
│   │   ├── importer.py           # CSV/XLSX import with column mapping
│   │   ├── processor.py          # Sample categorisation, duplicate pairing
│   │   └── crm_manager.py        # Certified Reference Material database
│   ├── analysis/                 # QAQC analysis engines
│   │   └── __init__.py           # Standards, Blanks, Duplicates analysers
│   ├── visualization/            # Matplotlib/Plotly chart generation
│   ├── reporting/                # Excel, PDF, DOCX report generators
│   ├── gui/                      # PyQt6 desktop GUI
│   │   ├── main_window.py
│   │   └── widgets/
│   ├── core/                     # Project persistence (save/load .qaqc)
│   └── utils/
│
├── react_ui/                     # Web UI (primary interface)
│   ├── src/                      # React 19 + TypeScript
│   │   ├── components/           # UI components
│   │   ├── features/             # Feature modules
│   │   ├── stores/               # Zustand state management
│   │   ├── services/             # API client layer
│   │   ├── hooks/                # Custom React hooks
│   │   └── types/                # TypeScript type definitions
│   ├── api/                      # FastAPI backend module
│   │   └── main.py               # API routes
│   ├── start_api.py              # Server entry point (factory pattern)
│   ├── package.json              # Node dependencies
│   └── vite.config.ts            # Build config
│
├── tests/                        # Python test suite (pytest)
├── scripts/                      # Build, packaging, monitoring scripts
├── .github/workflows/            # CI/CD (see below)
├── config.yaml                   # App configuration
├── crm_database.yaml             # CRM database (USGS standards, etc.)
├── logiqore.sh / logiqore.bat    # Cross-platform launcher scripts
├── main.py                       # CLI entry point
└── requirements.txt              # Python dependencies
```

---

## Tech Stack

### Python Backend
- **Python 3.11** — target runtime
- **FastAPI** + **Uvicorn** — web API server (`react_ui/api/`, `react_ui/start_api.py`)
- **Pandas / NumPy / SciPy** — data processing and statistical analysis
- **Matplotlib / Plotly / Seaborn** — chart generation
- **ReportLab** — PDF reports
- **XlsxWriter / OpenPyXL** — Excel reports
- **python-docx** — Word documents
- **PyQt6** — desktop GUI
- **PyInstaller** — packaging to native executables
- **pytest** — testing (`tests/` directory, `pytest.ini` config)

### React Frontend
- **React 19** + **TypeScript 5.9**
- **Vite 7** — build tool
- **Tailwind CSS 3** — styling
- **Zustand** — state management
- **AG Grid** — data tables
- **Plotly.js** (basic-dist-min) — interactive charts
- **Recharts** — additional chart library
- **Vitest** — unit tests
- **Playwright** — E2E tests

### CI/CD (GitHub Actions)
| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `test.yml` | Push/PR to main, pre-release | Python + React tests, coverage gates |
| `security.yml` | Push/PR | npm audit, dependency scanning |
| `build-artifacts.yml` | Push to pre-release | Cross-platform PyInstaller builds |
| `release.yml` | `v*` tags | Full release: React build → PyInstaller → zip → SHA256 → GPG sign → GitHub Release → optional public mirror |

### Deployment
- **Desktop:** PyInstaller executables distributed via GitHub Releases
- **Web UI:** Bundled into release zips; runs locally via `logiqore.sh`/`logiqore.bat`
- **Website:** Vercel auto-deploys from `logiqore-website` repo main branch

---

## Key Development Patterns

### Running Locally

```bash
# Python backend + React (development)
cd react_ui
npm install
npm run dev          # Vite dev server (hot reload)
# In separate terminal:
python start_api.py  # FastAPI on :8000

# Desktop GUI
python launch_gui.py

# CLI
python main.py --input data.csv --output ./output --infer-mapping --yes
```

### Testing

```bash
# Python tests
pytest                           # Full suite (130+ tests)
pytest -m unit                   # Unit tests only
pytest -m e2e                    # End-to-end workflows
pytest --cov=src --cov-fail-under=60  # With coverage gate

# React tests
cd react_ui
npm test                         # Vitest (watch mode)
npm run test:run                 # Single run
npm run test:coverage            # Coverage report
npm run test:e2e                 # Playwright E2E
```

### Building for Release

```bash
# React production build
cd react_ui && npm ci && npm run build  # Output → react_ui/dist/

# PyInstaller executables
python scripts/build_executables.py --target all --clean

# Trigger release: push a version tag
git tag v2.0.0-beta.7 && git push origin v2.0.0-beta.7
```

### Project Conventions
- Python: type hints on all functions, black formatting, flake8 linting
- React: strict TypeScript, ESLint, functional components with hooks
- Tests: pytest markers (`@pytest.mark.unit`, `@pytest.mark.e2e`, etc.)
- Commits: conventional commits (`feat:`, `fix:`, `ci:`, `docs:`, `security:`)
- Git branches: `main` (stable), `pre-release` (staging), `feature/*` (dev)

---

## Domain Knowledge: QAQC in Geology

Understanding the core domain helps write better code:

- **Standards (CRMs):** Known-value reference materials inserted into sample batches. We compute Z-scores and bias against certified values. Tolerances vary by element and analytical method (ICP-MS vs pXRF etc.).
- **Blanks:** Empty samples inserted to detect contamination. Checked against detection limits (DL). Carry-over detection flags elevated blanks after high-grade samples.
- **Duplicates:** Repeated analyses of the same sample. Evaluated using RPD (Relative Percent Difference), correlation coefficients, and nugget variance ratio.
- **Analytical methods:** ICP-MS, ICP-OES, pXRF, Fire Assay, AAS — each has different expected precision and accuracy.
- **Elements:** Major elements (Cu, Pb, Zn, Fe, S) have stricter tolerances (5-10%) than trace elements (Au, As, Ni, Co) at 10-20%.
- **CRM database:** `crm_database.yaml` stores certified values for USGS standards (AGV-1, BCR-1, etc.)

---

## Current Status and Priorities

### What's Done
- Full CLI + GUI desktop app with all QAQC analysis features
- React web UI with interactive Plotly charts, AG Grid tables, Zustand state
- FastAPI backend serving both API routes and React static files
- Cross-platform release pipeline (3 OS builds, checksums, GPG signing)
- Website at logiqore.io pulling releases dynamically from GitHub API

### What's In Progress / Next
- Code signing and notarization for desktop executables
- React bundle size further optimisation
- Public mirror repository setup (`PUBLIC_RELEASE_REPO`)
- User onboarding flow in the React UI
- Additional analytical method presets

---

## Important Files Quick Reference

| File | Purpose |
|------|---------|
| `main.py` | CLI entry point (28KB, feature-rich) |
| `react_ui/start_api.py` | FastAPI server factory (serves React + API) |
| `react_ui/api/main.py` | API route definitions |
| `config.yaml` | Application configuration (thresholds, paths) |
| `crm_database.yaml` | CRM certified values database |
| `pytest.ini` | Test configuration and markers |
| `scripts/build_executables.py` | PyInstaller build script |
| `.github/workflows/release.yml` | Release pipeline (306 lines) |
| `logiqore.sh` / `logiqore.bat` | Cross-platform launcher scripts |

---

## Recommended Claude Code Setup

### MCP Servers to Install

```json
// .mcp.json (in repo root)
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<your-pat>"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

**Why these:**
- **GitHub MCP** — manage issues, PRs, Actions runs, and releases directly from Claude Code. Essential for your tag-driven release workflow.
- **Filesystem MCP** — enhanced file operations across your multi-directory project structure.

### Recommended Hooks

```json
// .claude/settings.json
{
  "hooks": {
    "PreCommit": [
      {
        "type": "command",
        "command": "cd react_ui && npm run type-check && npm run lint"
      }
    ]
  }
}
```

### Custom Slash Commands

Create these in `.claude/commands/` for recurring workflows:

**`.claude/commands/test-all.md`**
```
Run the full test suite for both Python and React:
1. Run `pytest -v --tb=short` for Python tests
2. Run `cd react_ui && npm run test:run` for React tests
3. Summarise pass/fail counts for both
```

**`.claude/commands/release-check.md`**
```
Pre-release validation checklist:
1. Run Python tests: `pytest -v`
2. Run React type-check: `cd react_ui && npm run type-check`
3. Run React build: `cd react_ui && npm run build`
4. Verify dist/index.html exists
5. Check git status is clean
6. Report any issues found
```

**`.claude/commands/qaqc-context.md`**
```
Read and summarise the following files to understand current project state:
- CHANGELOG.md
- PRE_RELEASE_STATUS.md
- DEVELOPMENT_ROADMAP.md
Then list the most recent 5 commits on main.
```

### Useful Plugins

Search the Claude Code plugin registry for these:
- **python-development** — FastAPI patterns, pytest best practices, async patterns
- **react-modern** — React 19, Vite, Tailwind CSS, TypeScript strict mode
- **Context7** — injects current framework docs (React 19, Tailwind CSS, FastAPI) into context

### GitHub Actions Integration

You can add Claude Code as a PR reviewer:

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          command: "Review this PR for bugs, security issues, and consistency with the existing codebase patterns."
```

---

## Working with This Codebase — Tips for Claude

1. **Always check `config.yaml` and `crm_database.yaml`** when working on analysis logic — they define thresholds and reference values.
2. **The React UI is the primary interface** going forward. The PyQt6 GUI is maintained but not the priority.
3. **`start_api.py` uses a factory pattern** (`create_app()`) — this is intentional for Uvicorn compatibility.
4. **Release workflow is tag-driven** — push a `v*` tag to trigger. Don't modify release.yml without testing via a beta tag first.
5. **The website auto-updates** — it fetches release data from the GitHub API with 30-minute ISR cache. No manual website changes needed for new releases.
6. **Test markers matter** — use `@pytest.mark.unit`, `@pytest.mark.e2e`, etc. so CI can run subsets.
7. **Coverage gate is 60%** on scoped Python modules — don't let it drop.
8. **React uses `plotly.js-basic-dist-min`** (not full plotly) to keep bundle size reasonable.
