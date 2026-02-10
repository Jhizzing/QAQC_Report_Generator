# QAQC Report Generator — Testing Walkthrough

> **Date:** 2026-02-10  
> **Branch:** `pre-release`  
> **Testers:** Use this document to follow the recorded demo of every feature.

---

## Feature Coverage

| # | Feature | Video | Screenshot |
|---|---------|:-----:|:----------:|
| 1 | Session Management | ✅ | ✅ |
| 2 | Data Import | ✅ | ✅ |
| 3 | Analysis Setup | ✅ | ✅ |
| 4 | Results Dashboard | ✅ | ✅ |
| 5 | CRM Database | ✅ | ✅ |
| 6 | Settings | ✅ | ✅ |
| 7 | Report Export | ✅ | ✅ |
| 8 | CLI Workflow | — | — |

---

## 1. Session Management

Created a new QAQC session, entered project details (Project Name, Deposit, Commodity), and saved the project.

### Recording

![Session Management Demo](media/session_management_1770554342286.webp)

### Final State

![Session Saved — Dashboard](media/session_saved_dashboard_1770554580131.png)

---

## 2. Data Import

Loaded sample data ("Gold Fire Assay") from the Data Import page. The app auto-detected columns and transitioned directly to Analysis Setup.

### Recording

![Data Import Demo](media/data_import_1770554620830.webp)

### Initial State

![Data Import Page](media/data_import_page_pre_click_1770554775367.png)

---

## 3. Analysis Setup

Selected the "pXRF / Multi-element" analysis type, reviewed Quick Settings and Advanced Settings (QAQC rules for Standards, Blanks, Duplicates), then ran the analysis.

### Recording

![Analysis Setup Demo](media/analysis_setup_1770555039706.webp)

### Results After Running Analysis

![Analysis Results — Statistical Summary](media/analysis_results_final_state_1770555119383.png)

---

## 4. Results Dashboard

Explored the Results Dashboard with interactive tabs for Standards (40), Blanks (10), and Duplicates (20). Overall Pass Rate: **100.0%**.

### Recording

![Results Dashboard Demo](media/results_dashboard_1770555169465.webp)

### Dashboard Overview

![Results Dashboard — Standards Tab](media/results_dashboard_final_view_1770555259826.png)

---

## 5. CRM Database

Browsed the CRM Database (41 Certified Reference Materials), filtered by "OREAS", and expanded OREAS 101 to view certified values (Au: 0.082 g/t ±0.004).

### Recording

![CRM Database Demo](media/crm_database_1770555308404.webp)

### CRM Detail View

![CRM Details — OREAS 101](media/crm_details_view_1770555340895.png)

---

## 6. Settings

Reviewed all application settings: Report Format (PDF/DOCX/XLSX), Figure Resolution (DPI), Report Options (Cover Page, JORC Table 1), and Analysis Defaults (Tolerance, Precision Target, Contamination Multiplier, Failure Threshold). Backend confirmed "Connected".

### Recording

![Settings Page Demo](media/settings_page_1770555368050.webp)

### Settings Overview

![Settings — Analysis Defaults](media/settings_page_overview_1770555395393.png)

---

## 7. Report Export

Navigated to the Report page via "Create Report" on the Dashboard. Selected JORC Report format, filled metadata fields (Author, Company, Laboratory), toggled report options, and generated the report.

### Recording

![Report Export Demo](media/report_export_1770555444900.webp)

### Export Configuration

![Report Export — JORC Report Generation](media/final_report_export_state_1770555802293.png)

---

## 8. CLI Workflow

The command-line interface can be tested with:

```bash
python3 main.py \
  --input test_assay_data.csv \
  --output output_test \
  --infer-mapping \
  --normalize-results \
  --yes \
  --include-plots
```

**Expected outputs** in `output_test/`:
- `*_clean.csv` — Normalised data
- `*.provenance.json` — Processing log
- `qaqc_report_*.pdf` — Generated report
- `plots/` — Visualisations

---

## Known Issues

| Issue | Workaround |
|-------|-----------|
| React hook order error during navigation | Reload the page |
| CLI mapping may not auto-detect all columns | Use `--mapping <file.yaml>` |
