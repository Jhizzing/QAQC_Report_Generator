# Importer Module Capabilities

## Overview
The importer ingests assay datasets (CSV/XLSX), maps columns to a canonical schema, parses qualifiers and detection limits, and emits a cleaned dataset plus a provenance record for audit.

## Key Features
- File support: CSV, XLSX/XLS (single file, list, or directory)
- CSV options: `--csv-delimiter`, `--encoding`, `--csv-chunksize`, `--detect-encoding-fallback`
- Excel options: `--sheet` (name) or `--sheet-index`
- Hybrid column mapping:
  - Header normalization + synonyms + fuzzy matching
  - Required fields: `sample_id`, `sample_type`, `result`
  - Load/save mapping YAML (`--mapping`, `--save-mapping`)
  - CLI review with confidence and `--yes` auto-accept
- Qualifier + detection limit normalization:
  - Tokens: `ND`, `<DL`, `>DL`
  - Patterns: `<0.02`, `>10`, negative values as below DL (e.g., `-0.02`)
  - Per-row DL respected when present; fallback to default from `config.yaml`
  - Outputs `qualifier` and `detection_limit` columns
- Sample type normalization: maps common variants to `STANDARD`, `BLANK`, `DUPLICATE`
- Provenance sidecar (JSON): inputs, mapping, normalization, environment, output summary

## CLI Quick Start
```bash
# Infer mapping, normalize, write cleaned CSV and provenance
python main.py --input input/assays.csv --output output \
  --infer-mapping --normalize-results --yes

# Save the inferred mapping for reuse
python main.py --input input/assays.csv --output output \
  --infer-mapping --yes --save-mapping mapping.yaml

# Use a saved mapping
python main.py --input input/assays.csv --output output \
  --mapping mapping.yaml --normalize-results

# Select Excel sheet / CSV delimiter & encoding
python main.py --input input/data.xlsx --sheet "Assays" --infer-mapping --yes
python main.py --input input/data.csv --csv-delimiter ";" --encoding "utf-8-sig" \
  --infer-mapping --normalize-results --yes

# Large CSVs: chunked reading
python main.py --input input/big.csv --csv-chunksize 2000 --infer-mapping --yes
```

## Configuration
- `config.yaml` → `data.cleaning.default_detection_limit` used as default DL if row-level DL is absent.
- Extend mapping synonyms by editing `SYNONYMS` (or we can add config-driven synonyms in the future).

## Outputs
- Cleaned CSV: `<stem>_clean.csv`
- Provenance JSON: `<stem>_clean.provenance.json`

## Notes and Limitations
- Fuzzy mapping accepts suggestions with confidence ≥ 0.85 by default.
- If required fields can’t be matched and `--yes` isn’t provided, the CLI exits with guidance and top-3 candidates.
- Encoding auto-detect uses a simple fallback loop (`utf-8-sig`, `cp1252`, `latin1`). For stronger detection we can add `chardet`.
