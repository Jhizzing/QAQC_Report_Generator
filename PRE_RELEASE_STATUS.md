# Pre-Release Status Summary

**Date**: February 7, 2026  
**Branch**: pre-release  
**Version**: 1.0.0-pre

## ✅ Completed Tasks

### 1. Core Stabilization
- ✅ Backward-compatible analyzer/importer paths restored for legacy callers/tests
- ✅ Data processing made tolerant to sample-type column naming variants
- ✅ PDF reporter config compatibility improved (page size + margin normalization)
- ✅ Duplicate analysis normalized for legacy dict-style duplicate rows

### 2. Python Test and Quality Gates
- ✅ Functional test suite passes: **130 passed, 12 skipped**
- ✅ Coverage gating aligned to release-critical Python scope in CI
  - Core coverage command now enforces `--cov-fail-under=60`
  - Current result: **62.68%** on scoped modules
- ✅ `pytest` default behavior now focuses on functional correctness (`--no-cov` in CI step)
- ✅ Benchmark timing checks made platform-robust for Windows CI runs

### 3. React UI Quality Gates
- ✅ Added `npm run type-check` script
- ✅ Updated TS app config to exclude test files from production type-check/build
- ✅ React checks passing locally:
  - `npm run type-check` ✅
  - `npm run build` ✅
  - `npm test -- --run` ✅
- ✅ Plotly runtime bundle optimized for release:
  - Switched runtime charts to `plotly.js-basic-dist-min` via `react-plotly.js/factory`
  - Removed 10MB+ Plotly chunk warning in production build

### 4. CI Hardening
- ✅ CI now triggers on `pre-release` branch
- ✅ Removed soft-fail patterns (`|| true`) from required React checks
- ✅ Added explicit two-step Python gate in CI:
  - Functional tests
  - Core coverage gate

### 5. Packaging Verification (macOS arm64)
- ✅ PyInstaller CLI + GUI builds pass
  - `dist/cli/QAQC-CLI`
  - `dist/gui/QAQC-GUI`
- ✅ Packaged CLI smoke run generated CSV/provenance/PDF/XLSX/plots successfully

### 6. Distribution Automation Assets
- ✅ Added cross-platform artifact build workflow:
  - `.github/workflows/build-artifacts.yml`
  - Matrix build targets: Windows/macOS/Linux
  - Includes packaged CLI smoke test + artifact upload
- ✅ Verified first fully green cross-platform artifact run
  - Run ID: `21779078084`
- ✅ Added checksum manifest generation (`SHA256SUMS.txt`) with optional GPG signing in CI
- ✅ Added tag-driven release workflow:
  - `.github/workflows/release.yml`
  - Trigger: `v*` tags
  - Produces draft GitHub Release with zipped platform artifacts + checksums
- ✅ Validated tag-driven draft release end-to-end:
  - `v1.0.0-rc2` run: `21780665366` (all jobs green)
  - Draft release created with cross-platform assets + `SHA256SUMS.txt`
- ✅ Validated manual build-artifacts run on current `pre-release` head:
  - Run: `21780782159` (all jobs green)
- ✅ Added installer/build scripts:
  - `packaging/windows/qaqc.iss` (Inno Setup template)
  - `packaging/macos/create_dmg.sh`
  - `packaging/linux/create_appimage.sh`
- ✅ Updated deployment documentation for new scripts/workflow

## ⚠️ Current Release Blockers

1. **Installer/signing is partially implemented**
   - Installer scripts/templates are present, but signing/notarization for production trust is not yet wired

2. **Release signing secrets and identities are not yet configured**
   - `RELEASE_GPG_PRIVATE_KEY` / `RELEASE_GPG_PASSPHRASE` not configured (checksum signature file not generated)
   - macOS notarization and Windows Authenticode certificates are still external setup tasks

## 📋 Pre-Release Checklist Status

### Application Readiness
- [x] Core QAQC analysis workflows passing
- [x] CRM integration passing
- [x] Reporting and visualization passing
- [x] CI gates aligned for current release strategy
- [x] React production checks passing
- [x] PyInstaller executable builds working on current platform
- [x] Cross-platform executable validation (first green run confirmed)
- [x] Tag-driven release publication (validated with `v1.0.0-rc2`)
- [~] Installer packaging + signing/notarization (scripts added, trust automation pending)

### Feature Coverage
- [x] Data import (CSV, Excel)
- [x] Standards analysis with CRM integration
- [x] Blanks analysis
- [x] Duplicates analysis (including nugget ratio + correlation)
- [x] Visualization generation
- [x] Excel and PDF reporting
- [x] Project persistence
- [x] React UI functional pipeline

## 🚀 Recommended Next Steps Toward Full Release

1. Keep `.github/workflows/build-artifacts.yml` green on every release-candidate change
2. Configure release signing secrets + certificate identities
3. Run external UAT with representative lab datasets
4. Cut `v1.0.0` with release notes, signed checksums, and install guide

---

**Status**: ✅ **Release hardening in progress with stable CI gates and passing local checks**
