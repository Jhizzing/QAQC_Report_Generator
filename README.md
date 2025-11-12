# QAQC Analysis Automation Application

**Status: ✅ PRODUCTION READY** - Complete QAQC analysis system with comprehensive testing and validation.

This application provides automated QAQC (Quality Assurance / Quality Control) analysis for laboratory data, evaluating standards, blanks, and duplicates with professional reporting and visualization capabilities.

---

## 1. Objective
The program automates the validation and reporting of QAQC results from drilling datasets. It ensures consistent evaluation of laboratory performance, sample precision, and data quality through reproducible calculations and visualizations.

## 1.1 Current Status
- **✅ Phase 1 Complete**: Data import, mapping, and normalization
- **✅ Phase 2 Complete**: Analysis engine, visualization, and reporting
- **✅ CRM System**: Certified Reference Material integration
- **✅ Testing**: 101 tests passing with comprehensive coverage
- **✅ Mock Data Validation**: Successfully tested with realistic datasets
- **✅ Production Ready**: Full CLI interface with professional output
- **✅ GUI Complete**: Fully functional PyQt6 GUI with data import, analysis, and visualization

### Key Achievements
- **Data Processing**: Robust CSV/XLSX import with intelligent column mapping
- **QAQC Analysis**: Standards, blanks, and duplicates analysis with CRM integration
- **Visualization**: Professional plots (control charts, scatter plots, histograms)
- **Reporting**: Excel and PDF reports with executive summaries
- **Quality Assurance**: Comprehensive error handling and data validation

---

## 2. Functional Overview
### Key Capabilities
- Import and clean QAQC data from drilling programs.
- Identify and evaluate **standards, blanks, and duplicates**.
- Compute analytical and sampling precision metrics (bias, RPD, nugget ratio, etc.).
- Generate summary statistics, control charts, and compliance tables.
- Produce a fully formatted **PDF and Excel report**.

---

## 3. Workflow Summary

### Step 1: Data Import
- Supported input formats: CSV, XLSX, or ODBC connection to acQuire or Datamine exports.
- User maps input columns to required fields (SampleID, Type, Result, etc.).
- Units, qualifiers (`<DL`, `>DL`), and methods are normalized.

### Step 2: Data Cleaning and Pairing
- Parse and clean qualifiers.
- Match duplicates (Primary–Duplicate pairs) using IDs or nearest sampling intervals.
- Link standards and blanks to laboratory batches.
- Validate completeness (each batch must include expected QAQC types).

### Step 3: Calculations
#### Standards (CRMs)
- Compute Z-scores and bias.
- Apply Shewhart or Westgard rules.
- Summarize pass/fail statistics per CRM, batch, and lab.

#### Blanks
- Check absolute and threshold-based exceedances (e.g., >3×DL).
- Flag carry-over (elevated blanks after high-grade samples).

#### Duplicates
- Calculate mean, absolute difference, % difference (RPD), and % variance.
- Compute correlation (Pearson r) and regression slope/intercept.
- Estimate nugget variance ratio:
  \( Nugget\ Ratio = 0.5 * Var(CK - OR) / Var(OR) \)

### Step 4: Visualization
- **Standards:** Control charts with ±2SD, ±3SD bands.
- **Blanks:** Histograms, sequential plots with fail thresholds.
- **Duplicates:**
  - OR vs CK scatter with 1:1 line.
  - RPD vs mean (precision plot).
  - Bland–Altman plot for agreement.

### Step 5: Reporting
- Generate a **summary report (PDF)** and a detailed **Excel workbook**.
- Include:
  - Overview tables (per analyte and batch)
  - Charts for CRMs, blanks, and duplicates
  - Pass/fail summaries and rerun recommendations

---

## 3.1 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/Jhizzing/QAQC_Report_Generator.git
cd QAQC_Report_Generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage
```bash
# Basic analysis with auto-mapping and CRM selection
python main.py --input data/assays.csv --output results --infer-mapping --normalize-results --yes --auto-crm --include-plots

# Full analysis with specific CRM
python main.py --input data/assays.csv --output results --crm-name "NIST SRM 2709a" --include-plots --output-format both

# Process directory with Excel output only
python main.py --input data/ --output results --infer-mapping --normalize-results --yes --output-format excel
```

### Example Output
- **Excel Report**: Multi-sheet workbook with analysis results
- **PDF Report**: Executive summary with recommendations
- **Plots**: Control charts, scatter plots, histograms
- **Cleaned Data**: Normalized CSV with provenance logs

## 4. Technology Stack

### Lane A – Desktop (Offline MVP)
- **Language:** Python 3.11+
- **Libraries:** `pandas`, `numpy`, `scipy`, `matplotlib`, `plotly`, `xlsxwriter`, `reportlab`, `jinja2`
- **GUI:** PySide6 or Tkinter (`ttkbootstrap` for theming)
- **Data storage:** Local CSV/XLSX or SQLite
- **Packaging:** `pyinstaller` → standalone .exe

### Lane B – Web (Multi-user, scalable)
- **Backend:** FastAPI, PostgreSQL, SQLModel/SQLAlchemy
- **Frontend:** React + TypeScript + Plotly.js or ECharts
- **Reports:** HTML templating (Jinja2) → PDF (WeasyPrint)
- **Deployment:** Docker / Docker Compose or Kubernetes
- **Auth:** Azure AD / Auth0 / Role-based permissions

---

## 5. Data Model
- **Samples:** `SampleID, HoleID, From, To, Type, Result, Lab, Method`
- **Standards:** `CRM_ID, CertifiedValue, SD_cert, Lot, BatchID`
- **Duplicates:** `PrimaryID, DuplicateID, OR, CK, Difference, RPD`
- **Blanks:** `SampleID, Result, Threshold, Pass/Fail`
- **Settings:** tolerances, DLs, cut-offs, and report metadata.

---

## 6. Outputs
**Excel:** Detailed results per QAQC type, pivot summaries, and embedded charts.
**PDF:** Executive summary with plots and interpretation-ready tables.
**CSV/JSON:** Exportable machine-readable data for audit.

---

## 7. Analysis Metrics
| QAQC Type | Key Calculations | Output Metrics |
|------------|------------------|----------------|
| Standards | Z-score, Bias | % within ±2SD, drift trend, batch pass/fail |
| Blanks | Threshold exceedance | % below DL, carry-over flag |
| Duplicates | RPD, % variance, regression, nugget ratio | Precision plots, correlation, nugget ratio |

---

## 8. Statistical Concepts
- **% Difference (RPD):** Useful for relative precision but exaggerates low grades.
- **Absolute Difference:** Preferred for nugget analysis and true grade variability.
- **Nugget Ratio:** Quantifies short-scale variability and analytical error.

---

## 9. Development Roadmap
1. **Phase 1:** Core calculations + Excel reporting (desktop prototype)
2. **Phase 2:** GUI interface + PDF reports
3. **Phase 3:** Web-based deployment (multi-user, dashboards)
4. **Phase 4:** Integrations (acQuire API, automated notifications, lab imports)

---

## 10. Suggested Enhancements
- Top-cut recommender (MAD or log-QQ method)
- Batch rerun suggestions
- Multi-lab comparison (Youden plots)
- Geology integration (compare QAQC by lithology/alteration)
- Configurable thresholds and project templates

---

## 11. File Structure Example
```
/project
  /input
    assays.csv
    qaqc_register.csv
    crm_catalogue.xlsx
  /output
    QAQC_Report_2025-10-18.pdf
    QAQC_Results_2025-10-18.xlsx
    plots/
      standards_control_[CRM].png
      blanks_histogram.png
      duplicates_scatter.png
  config.yaml
```

---

## 12. Summary
This QAQC automation system streamlines assay data validation, reducing manual effort and ensuring consistent, transparent reporting. The proposed stack allows flexibility between a site-deployable desktop tool and a scalable web platform, both producing robust, auditable QAQC results ready for inclusion in JORC-compliant reporting.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Required Python packages: `pandas`, `numpy`, `scipy`, `matplotlib`, `plotly`, `xlsxwriter`, `reportlab`, `jinja2`

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd qaqc-report-generator
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp env.example .env
# Edit .env with your configuration
```

### Usage

Run the QAQC analysis application:

```bash
python main.py
```

## Project Structure

```
├── src/                 # Source code
│   ├── data/           # Data processing modules
│   ├── analysis/       # QAQC analysis calculations
│   ├── visualization/  # Plot generation
│   ├── reporting/      # Report generation
│   └── gui/           # User interface
├── tests/              # Test files
├── docs/               # Documentation
├── config/             # Configuration files
├── scripts/            # Build and utility scripts
├── assets/             # Static assets
├── input/              # Input data files
├── output/             # Generated reports and plots
└── README.md           # This file
```

## Development

### Running Tests

```bash
pytest
```

### Building

```bash
python setup.py build
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/qaqc-report-generator](https://github.com/yourusername/qaqc-report-generator)

## Import Cookbook (CLI)

Quick examples to import, map, normalize, and export cleaned data.

- Infer mapping, normalize qualifiers/DLs, and write cleaned CSV
```bash
python main.py --input input/assays.csv --output output \
  --infer-mapping --normalize-results --yes -v
```

- Use a saved mapping profile and normalize
```bash
python main.py --input input/assays.csv --output output \
  --mapping mapping.yaml --normalize-results -v
```

- Save the inferred mapping for future runs
```bash
python main.py --input input/assays.csv --output output \
  --infer-mapping --yes --save-mapping mapping.yaml
```

- Process a directory (all CSV/XLSX files)
```bash
python main.py --input input/ --output output \
  --infer-mapping --normalize-results --yes -v
```

- Select Excel sheet; handle CSV delimiter/encoding
```bash
python main.py --input input/data.xlsx --sheet "Assays" --infer-mapping --yes
python main.py --input input/data.csv --csv-delimiter ";" --encoding "utf-8-sig" \
  --infer-mapping --normalize-results --yes
```

- Large CSV performance
```bash
python main.py --input input/big.csv --csv-chunksize 2000 \
  --infer-mapping --normalize-results --yes
```

- Provenance sidecar (auto)
  - For each output `<stem>_clean.csv`, a `<stem>_clean.provenance.json` is printed (in dry-run) or written alongside the CSV.

Notes
- Required fields after mapping: `sample_id`, `sample_type`, `result`.
- Normalization creates `qualifier` and `detection_limit` columns and supports tokens: ND, <DL, >DL, negative values as below DL.
- Per-row detection limits are respected when a `detection_limit` column exists; otherwise the default from `config.yaml` is used.
