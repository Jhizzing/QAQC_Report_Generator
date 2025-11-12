# QAQC Application Packaging & Distribution Guide

This document explains how to convert the QAQC Analysis Application into standalone executables, wrap them in platform-specific installers, and verify the builds before release. It assumes the codebase is already passing tests and that Python 3.11+ plus Node-like build tools are available on the build machine.

---

## 1. Build Prerequisites
- Python 3.11+ with `pip install -r requirements.txt`
- PyInstaller 5.13+ (already listed in `requirements.txt`)
- Platform SDK tooling (only when building installers):
  - **Windows**: PowerShell 7+, Inno Setup 6+, optional `signtool` for code signing
  - **macOS**: Xcode command line tools (`xcode-select --install`), `codesign`, `notarize` credentials if required
  - **Linux**: `appimagetool` (AppImage), `dpkg-deb` (DEB), or `rpmbuild` (RPM)
- Clean workspace: `git pull && git status` should show no pending commits before cutting a release build.

---

## 2. Building Single-File Executables
Use the helper script to orchestrate PyInstaller builds. It consumes the spec files under `packaging/pyinstaller` and places artifacts in `dist/<target>`.

```bash
# Build CLI + GUI on the current platform
python3 scripts/build_executables.py --target all --clean

# Build only the GUI bundle
python3 scripts/build_executables.py --target gui

# Forward extra options to PyInstaller (example: enable debug logging)
python3 scripts/build_executables.py --target cli \
    --pyinstaller-arg --log-level=TRACE
```

### Output Layout
```
dist/
  cli/
    QAQC-CLI        # macOS/Linux binary
    QAQC-CLI.exe    # Windows binary (when built on Windows)
  gui/
    QAQC-GUI        # macOS/Linux GUI app
    QAQC-GUI.exe    # Windows GUI app
```

Both spec files embed:
- `config.yaml` and `crm_database.yaml`
- `/config`, `/mock_data`, and `/assets` directories
- All `src` modules required by the CLI and PyQt6 GUI

### Platform-Specific Notes
- **Windows**: Run builds inside a Developer PowerShell so the MSVC redistributables are discoverable. PyInstaller automatically bundles the VC runtime when executed on Windows.
- **macOS**: Use `python3 scripts/build_executables.py ...` from a virtual environment. After the build, wrap the GUI binary inside an `.app` bundle if desired and codesign it (`codesign --deep --force --options runtime --sign "Developer ID" dist/gui/QAQC-GUI`).
- **Linux**: Build on each target distribution (Ubuntu, RHEL, etc.) or rely on a manylinux-style container to avoid glibc mismatches. For portable desktop delivery, consider turning the GUI binary into an AppImage (see Section 3.3).

---

## 3. Installer Packages
Once the single-file executables are produced, ship them directly or embed them inside OS-native installers.

### 3.1 Windows (Inno Setup)
1. Install [Inno Setup](https://jrsoftware.org/isinfo.php).
2. Create a script (e.g., `packaging/windows/qaqc.iss`) pointing to `dist/cli/QAQC-CLI.exe` and `dist/gui/QAQC-GUI.exe`.
3. Include config templates as `Source: "config\\*"; DestDir: "{app}\\config"`.
4. Build via `ISCC.exe packaging/windows/qaqc.iss`.
5. Optional: sign the installer with `signtool sign /a /tr http://timestamp.digicert.com /fd sha256 QAQC_Setup.exe`.

### 3.2 macOS (DMG / PKG)
1. Create an `.app` bundle for the GUI binaries (PyInstaller can emit `.app` when run on macOS with `--windowed`).
2. Codesign the bundle.
3. Build a DMG: `hdiutil create -volname "QAQC" -srcfolder dist/gui/QAQC-GUI.app dist/gui/QAQC.dmg`.
4. Notarize if distributing outside the organization (`xcrun notarytool submit dist/gui/QAQC.dmg --apple-id ...`).
5. Provide a companion CLI binary inside `/Applications/QAQC Tools/` or ship it separately via a signed tarball.

### 3.3 Linux (AppImage / Deb / Rpm)
- **AppImage**: combine the GUI binary with the config assets using `generate_appimage.sh`:
  1. Create `AppDir/usr/bin/QAQC-GUI` (copy the PyInstaller output).
  2. Provide a `.desktop` file plus icon.
  3. Run `appimagetool AppDir QAQC-GUI-x86_64.AppImage`.
- **Debian/Ubuntu**: craft `debian/` metadata pointing to `/opt/qaqc/QAQC-CLI` and `/opt/qaqc/QAQC-GUI`. Build with `dpkg-deb --build debian/qaqc`.
- **RHEL/Fedora**: mirror the same layout via `rpmbuild`.

---

## 4. Distribution Testing Checklist
Perform these checks on every platform/architecture that will receive binaries.

1. **Smoke Test**
   - Launch GUI, import `mock_data/complex_test_data.csv`, verify panels respond.
   - Run CLI: `./QAQC-CLI --input mock_data/complex_test_data.csv --output output --auto-crm --include-plots`.
2. **Config Override**
   - Place a custom `config.yaml` next to the executable and ensure it overrides the bundled template.
3. **CRM Database**
   - Modify `crm_database.yaml`, rerun CLI, confirm new CRM metadata loads.
4. **Report Generation**
   - Confirm PDF + Excel files appear in the specified output directory and open without warnings.
5. **Log/Temp Hygiene**
   - Ensure PyInstaller onefile extracts to a writable temp directory and cleans up on exit.
6. **Installer Verification**
   - Install/uninstall flows succeed without admin rights when possible.
   - Hash the shipped artifacts (`shasum -a 256 <file>` or `Get-FileHash`).
7. **Security & Compliance**
   - Run Windows Defender / XProtect / ClamAV scans on the binaries.
   - Verify code-signing signatures and notarization tickets (where applicable).

Document test results in `docs/testing/distribution/<date>.md` for traceability.

---

## 5. Recommended Next Steps
1. **Automate CI Builds**: Integrate `scripts/build_executables.py` into GitHub Actions with matrix jobs for Windows/macOS/Linux runners.
2. **Add Installer Scripts**: Check in `packaging/windows/qaqc.iss` and shell scripts for DMG/AppImage creation to keep packaging reproducible.
3. **Code Signing Pipeline**: Securely store signing certificates and automate signing/notarization where your release policy requires it.
4. **User Acceptance Testing**: Recruit a small group of geologists to exercise the packaged apps with real data before broad rollout.
5. **Feedback Loop**: Capture installer/first-run friction in an issue tracker to prioritize quick fixes before marketing the standalone release.
