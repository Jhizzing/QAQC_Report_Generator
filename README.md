# LogiQore Reporter

**QAQC analysis and reporting for geoscience assay data.**

LogiQore Reporter automates the validation and reporting of QAQC results from drilling and assay datasets. It evaluates standards (CRMs), blanks, and duplicates with interactive visualisations and professional report generation — ready for inclusion in JORC-compliant reporting.

> **v1.0 target:** Photon gold assay QAQC — import data, map columns, match CRMs, run analysis, export interactive plots and a Word report template.

---

## Architecture

```
┌──────────────────────────────────────┐
│          React UI (Tauri)            │
│  Wizard: Import → Configure →        │
│  Analyse → Review → Export           │
└──────────────┬───────────────────────┘
               │ HTTP
┌──────────────▼───────────────────────┐
│          FastAPI Backend             │
│  /api/data  /api/analyze             │
│  /api/crm   /api/report             │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│        Service Layer                 │
│  DataService   AnalysisService       │
│  CRMService    ReportService         │
│  SettingsService                     │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│         Core Engine                  │
│  Analyzers · Visualisation ·         │
│  Report Generators                   │
└──────────────────────────────────────┘
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19, TypeScript, Vite, Tailwind CSS, Plotly.js |
| **Backend** | Python 3.11+, FastAPI, Uvicorn |
| **Core Engine** | pandas, numpy, scipy, matplotlib |
| **Reports** | python-docx (Word), xlsxwriter (Excel) |
| **Desktop** | Tauri (planned — Rust-based, ~8MB binary) |
| **Data** | YAML/JSON CRM database, CSV/XLSX import |

---

## Project Structure

```
├── api/                  # FastAPI backend
│   ├── main.py           # API server and endpoints
│   ├── exceptions.py     # Custom exception classes
│   └── tests/            # API integration tests
├── src/                  # Python source
│   ├── services/         # Service layer (business logic)
│   │   ├── data_service.py
│   │   ├── analysis_service.py
│   │   ├── crm_service.py
│   │   ├── report_service.py
│   │   └── settings_service.py
│   ├── analysis/         # Core QAQC analyzers
│   ├── data/             # Data import, models, CRM manager
│   ├── reporting/        # Report generators (DOCX, Excel, PDF)
│   ├── visualization/    # Plot generation (matplotlib)
│   ├── core/             # Settings, project manager
│   └── utils/            # Error handling, runtime paths
├── react_ui/             # React frontend
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── features/     # Feature modules (import, analysis, etc.)
│   │   ├── stores/       # Zustand state management
│   │   ├── api/          # API client
│   │   └── types/        # TypeScript types
│   └── vite.config.ts
├── data/                 # CRM database and sample data
│   ├── crm_database.yaml
│   ├── industry_crms.csv
│   └── input/
├── tests/                # Python test suite
├── docs/                 # Documentation
└── config/               # App configuration
```

---

## Quick Start

### Backend

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run API server
uvicorn api.main:app --reload --port 8000
```

### Frontend

```bash
cd react_ui
npm install
npm run dev
```

The React dev server runs on `http://localhost:5173` and proxies API calls to `http://localhost:8000`.

---

## v1.0 Workflow

1. **Import** — Drag-and-drop CSV/Excel with photon gold assay data
2. **Map Columns** — IoGas-style column mapping dialog with auto-detection
3. **Confirm CRMs** — Match detected standards to CRM database, add custom CRMs
4. **Analyse** — Standards (XY + 2/3 SD lines), Blanks (bar chart + LDL), Duplicates (scatter + 1:1 line)
5. **Review** — Interactive Plotly charts, filterable summary table
6. **Export** — Copy individual plots, download Word report template with commentary sections

See [PLANNING.md](PLANNING.md) for the full build plan.

---

## Development

### Running Tests

```bash
# Python tests
pytest

# React tests
cd react_ui && npm test
```

### CLI (legacy)

```bash
python main.py --input data/input/sample_data.csv --output output --infer-mapping --auto-crm
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

Copyright (c) 2024 LogiQore
