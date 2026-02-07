# Launch and Distribution Plan

This is a practical step-by-step plan to move from `pre-release` to a public `v1.0.0` launch.

## Goal
Ship a stable, installable QAQC application for first external users with low support friction.

## Phase 1: Release Baseline (Now)

### 1. Freeze the release candidate branch
- Work from `pre-release`
- Keep changes focused on release blockers only

### 2. Keep a single source of truth for readiness
- Update `PRE_RELEASE_STATUS.md` after each major validation pass
- Record exact command outputs and dates

### 3. Define quality gates for v1.0.0
- Functional tests must pass
- Packaged CLI smoke test must pass
- Packaged GUI launch must pass on each target OS
- React production build must pass if React UI is included in first release

## Phase 2: CI Hardening (High Priority)

### 1. Update CI branch coverage
- Ensure workflows run for `pre-release`
- Remove soft-fail patterns (`|| true`) for required checks

### 2. Align coverage policy with release intent
Choose one of these and apply consistently:
- Option A: Keep 70%, but limit measured modules to release-critical code
- Option B: Keep broad module scope, reduce threshold temporarily, and raise incrementally

### 3. Add packaging checks to CI
- Build CLI/GUI executables in CI matrix jobs
- Upload built artifacts for manual QA download/testing

## Phase 3: Cross-Platform Packaging

### 1. Build executables
```bash
venv/bin/python scripts/build_executables.py --target all --clean
```

### 2. Validate CLI artifact
```bash
./dist/cli/QAQC-CLI --help
./dist/cli/QAQC-CLI --input mock_data/complex_test_data.csv --output output/dist_smoke --infer-mapping --normalize-results --yes --auto-crm --include-plots --output-format both
```

### 3. Validate GUI artifact
- Launch `dist/gui/QAQC-GUI`
- Import `mock_data/complex_test_data.csv`
- Generate PDF + Excel + plots

### 4. Repeat on all target platforms
- Windows 11
- macOS (Intel + Apple Silicon if possible)
- Ubuntu LTS

## Phase 4: Installer + Trust Layer

### 1. Create native installers
- Windows: Inno Setup (`.exe` installer)
- macOS: `.dmg` (or `.pkg`)
- Linux: AppImage (first), then optional DEB/RPM

### 2. Add integrity and trust
- Generate SHA256 checksums for each artifact
- Add code-signing where feasible
- For macOS external distribution, notarize DMG

## Phase 5: Launch Readiness

### 1. Release assets
- Executables/installers per OS
- Checksums file
- Installation guide
- Known issues and support contact

### 2. Release notes (required sections)
- What's new
- Supported platforms
- Installation steps
- Breaking/known issues
- Quick start workflow (first report in 5 minutes)

### 3. Pilot rollout
- 3 to 5 friendly users with real datasets
- Track failures by category: install, import, analysis, report output, performance
- Patch quickly before broad release

## Phase 6: Post-Launch Operations

### 1. Support loop
- Create issue templates for bug reports
- Ask users to include sample logs and platform details

### 2. Update cadence
- Patch releases: weekly or bi-weekly initially
- Feature releases: monthly once support load stabilizes

### 3. Metrics to track
- Install success rate
- First-run success rate
- Report generation failure rate
- Top 5 user pain points

## Recommended v1.0.0 Scope
Include:
- CLI executable
- PyQt6 desktop GUI executable
- PDF + Excel reporting
- CRM integration

Hold for v1.1 if needed:
- React deployment surface (until build/test pipeline is fully green)

## Operator Checklist (Per Release Candidate)
- [ ] `pytest` functional tests pass
- [ ] Coverage policy decision documented and applied
- [ ] `react_ui` production build status decided (included or deferred)
- [ ] CLI + GUI executables built
- [ ] Cross-platform smoke tests complete
- [ ] Installers built and tested
- [ ] Checksums generated
- [ ] Release notes written
- [ ] Rollback plan documented

## Rollback Plan (Minimal)
- Keep previous stable artifacts available
- If critical defect appears:
  - Mark latest release as withdrawn
  - Re-point users to last stable build
  - Publish hotfix ETA within 24 hours
