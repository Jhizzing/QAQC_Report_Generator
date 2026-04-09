# LogiQore Reporter — v1.0 MVP Build Plan

## Vision

A focused QAQC reporting tool for geologists working with photon gold assay data. The app guides users through a wizard workflow: import data, map columns, confirm CRMs, run analysis, review interactive results, and export a professional Word report.

Build this solid, then iterate.

---

## Target User

Exploration and resource definition geologists who need to validate QAQC data from photon gold analysis (becoming industry standard for operations and resource definition). The user imports assay data including QAQC samples, confirms their CRM standards, reviews analysis results with interactive charts, and exports a report for inclusion in technical reports.

---

## v1.0 Scope — What We're Building

### Stage 1: Data Import & Column Mapping

**Import Screen:**
- Drag-and-drop or file picker for CSV/Excel
- Preview first 20 rows in a table
- Auto-detect common column names (Sample ID, Au_ppm, QC_Type, etc.)

**Column Mapping Dialog (IoGas-style):**
- Left panel: file columns with data type preview (first 5 values shown)
- Right panel: required fields to map to (Sample ID, Assay Value, QC Type, Original Sample ID)
- Drag columns left → right, or use dropdowns
- Smart suggestions: "Au_ppm" auto-maps to Assay Value
- Green ticks when required fields are mapped; can't proceed until minimum set
- "Remember this mapping" option for repeat imports

**QC Type Detection:**
- Auto-classify rows as Standard / Blank / Duplicate / Routine
- User can define naming conventions (e.g., "STD-*" = standard, "BLK-*" = blank)
- Show preview counts: "Found: 450 routine, 23 standards, 18 blanks, 15 duplicate pairs"

### Stage 2: CRM Database & Matching

**CRM Database:**
- Ships with built-in database of common photon gold CRMs (OREAS, Geostats, CDN, etc.)
- YAML/JSON format, versioned with the app
- Each CRM: name, certified value, uncertainty (±), 2SD/3SD ranges, provider, matrix

**CRM Management Interface:**
- Searchable/filterable table of all CRMs
- "Add CRM" form: name, certified value, 1SD, provider, notes
- Edit/delete local CRMs (built-in are read-only)
- Local CRMs stored in user's app data directory (~/.logiqore/)

**CRM Matching Step (Wizard):**
- After import, show detected standard sample names
- Auto-match to CRM database (fuzzy name matching)
- User confirms/corrects via dropdown
- Unmatched standards highlighted — user can add new CRM inline
- No analysis proceeds until CRMs are confirmed

### Stage 3: Analysis & Visualisation

**3a. Standards Analysis**
- **Plot:** XY scatter — X = sample sequence/batch, Y = assay value
  - Horizontal lines: certified value, ±2SD (warning), ±3SD (fail)
  - Points coloured: green (within 2SD), amber (2-3SD), red (outside 3SD)
  - Interactive: hover for sample ID, zoom, pan, filter by CRM
- **Stats:** Mean recovery %, std dev, count within/outside limits

**3b. Blanks Analysis**
- **Plot:** Bar chart — each blank as a bar, Y = assay value
  - Horizontal line at LDL (default 0.03 ppm, configurable)
  - Bars coloured: green (below LDL), red (above LDL)
  - Interactive: hover for sample ID and value
- **Stats:** Number of blanks, number over LDL, contamination rate %

**3c. Duplicates Analysis**
- **Plot:** Scatter — X = original value, Y = duplicate value
  - 1:1 line (perfect agreement)
  - Points coloured by RPD (green <10%, amber 10-20%, red >20%)
  - Interactive: hover for pair IDs and RPD
- **Stats:** Mean RPD, median RPD, number of pairs, number failing threshold

**3d. Summary Table**

| Metric | Value |
|--------|-------|
| Total Samples | — |
| Total QAQC | — |
| Standards (count, %) | — |
| Blanks (count, %) | — |
| Duplicates (count, %) | — |
| Warnings | — |
| Fails | — |
| Overall Status | PASS / FAIL |

### Stage 4: Export & Sharing

**Individual Plot/Table Export:**
- Each plot: copy to clipboard, save as PNG/SVG, download underlying data as CSV
- Summary table: copy to clipboard, export as CSV/Excel
- Plots are interactive Plotly — filter/zoom before exporting

**Word Document Template:**
- One-click "Generate Report"
- Template structure:
  - Header: project name, date, analyst, lab
  - Standards section: plot + stats table + empty text box for comments
  - Blanks section: plot + stats table + empty text box for comments
  - Duplicates section: plot + stats table + empty text box for comments
  - Summary table
  - Conclusions section: empty text box for user analysis
- Plots embedded as high-res images
- User fills in commentary in Word after generation

---

## What's NOT in v1.0

- PDF report generation (Word is enough)
- Excel report generation (keep existing code but don't wire to new UI)
- CUSUM charts, Bland-Altman plots, Thompson-Howarth plots, histograms
- Multi-element support (gold only)
- Historical trend analysis across multiple batches
- Auto-update mechanism
- Tauri desktop packaging (ship as web app first, package later)
- Multi-user / authentication
- Database backend (files only)

---

## Build Phases

### Phase 1: Service Layer Foundation (Week 1-2)
- [x] Create `src/services/` with DataService, AnalysisService, CRMService, ReportService, SettingsService
- [x] Decouple SettingsManager from PyQt6 → JSON file backend
- [x] Delete PyQt6 GUI (`src/gui/`)
- [x] Delete TypeScript analysis engines
- [x] Move FastAPI backend to top-level `api/`
- [x] Clean up requirements.txt (remove PyQt6, pyinstaller, etc.)
- [ ] Wire FastAPI endpoints to service layer
- [ ] Seed CRM database with photon gold CRMs (OREAS, Geostats, CDN, AMIS)

### Phase 2: Import & Column Mapping (Week 2-3)
- [ ] API: file upload endpoint, parse CSV/Excel, return preview + suggested mapping
- [ ] API: column mapping confirmation endpoint
- [ ] API: QC type detection endpoint
- [ ] React: file upload with drag-and-drop
- [ ] React: IoGas-style column mapping dialog
- [ ] React: QC type preview with counts

### Phase 3: CRM Matching (Week 3-4)
- [ ] API: CRM CRUD endpoints (list, search, add, edit)
- [ ] API: auto-match standards to CRMs endpoint
- [ ] React: CRM browser with search and filter
- [ ] React: CRM add/edit form
- [ ] React: standard-to-CRM confirmation step

### Phase 4: Analysis & Interactive Charts (Week 4-6)
- [ ] API: run analysis endpoint (returns structured results for Plotly)
- [ ] React + Plotly: standards XY chart with ±2SD/±3SD lines
- [ ] React + Plotly: blanks bar chart with LDL line
- [ ] React + Plotly: duplicates scatter with 1:1 line
- [ ] React: summary statistics table
- [ ] React: filtering and interaction (hover, zoom, pan)

### Phase 5: Export (Week 6-7)
- [ ] React: copy-to-clipboard for plots and tables
- [ ] React: PNG/SVG download for individual plots
- [ ] API: Word document generation endpoint
- [ ] Python: DOCX template with embedded plots and commentary sections
- [ ] React: report generation UI with metadata form

### Phase 6: Polish & Ship (Week 7-8)
- [ ] LogiQore dark slate + amber gold theme in Tailwind
- [ ] Loading states, error handling, edge cases
- [ ] End-to-end testing with real photon gold data
- [ ] Tauri integration for desktop packaging (stretch goal)

---

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Drop PyQt6 | React + FastAPI | React UI already has better wizard workflow; single UI to maintain |
| Delete TS analysis engines | Python only | No duplication; Python is source of truth for all computation |
| JSON settings | SettingsService | No Qt dependency; works in API and CLI contexts |
| Plotly over matplotlib (UI) | Plotly.js in React | Interactive charts: zoom, hover, filter — critical for geologists reviewing data |
| Keep matplotlib (reports) | python-docx embeds | Static high-res images in Word docs still need matplotlib |
| Word over PDF | python-docx | Geologists need to add commentary; Word is editable, PDF is not |
| Tauri over Electron | Deferred | Ship as web app first; Tauri packaging is a stretch goal for v1.0 |

---

## v1.1 Ideas (Post-Release)

- Multi-element support (Cu, Fe, As, etc.)
- PDF report generation
- Excel report export
- CUSUM and Bland-Altman charts
- Historical trend analysis
- Tauri desktop packaging
- Auto-update
- Template management (save/load report templates)
- Batch comparison tools
