#!/usr/bin/env bash
set -euo pipefail

# Build AppImage from PyInstaller GUI onefile output.
# Requirements: appimagetool installed and available on PATH.
# Usage:
#   bash packaging/linux/create_appimage.sh [version]

VERSION="${1:-1.0.0-pre}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GUI_BIN="$ROOT_DIR/dist/gui/LogiQore-Reporter-GUI"
APPDIR="$ROOT_DIR/build/appimage/AppDir"
OUTPUT="$ROOT_DIR/dist/gui/LogiQore-Reporter-${VERSION}-x86_64.AppImage"

if ! command -v appimagetool >/dev/null 2>&1; then
  echo "appimagetool not found. Install it first: https://appimage.org/"
  exit 1
fi

if [[ ! -f "$GUI_BIN" ]]; then
  echo "GUI executable not found: $GUI_BIN"
  echo "Build first: python scripts/build_executables.py --target gui --clean"
  exit 1
fi

rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/applications" "$APPDIR/usr/share/icons/hicolor/256x256/apps"

cp "$GUI_BIN" "$APPDIR/usr/bin/logiqore-reporter"
chmod +x "$APPDIR/usr/bin/logiqore-reporter"

cat > "$APPDIR/logiqore-reporter.desktop" <<DESKTOP
[Desktop Entry]
Type=Application
Name=LogiQore Reporter
Comment=QAQC analysis and reporting application
Exec=logiqore-reporter
Icon=logiqore-reporter
Categories=Science;Education;
Terminal=false
DESKTOP

cp "$APPDIR/logiqore-reporter.desktop" "$APPDIR/usr/share/applications/logiqore-reporter.desktop"

# Minimal launcher expected by AppImage
cat > "$APPDIR/AppRun" <<'APPRUN'
#!/usr/bin/env bash
HERE="$(dirname "$(readlink -f "$0")")"
exec "$HERE/usr/bin/logiqore-reporter" "$@"
APPRUN
chmod +x "$APPDIR/AppRun"

# Placeholder icon (replace with branded icon file when available)
if [[ -f "$ROOT_DIR/assets/icon.png" ]]; then
  cp "$ROOT_DIR/assets/icon.png" "$APPDIR/logiqore-reporter.png"
  cp "$ROOT_DIR/assets/icon.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/logiqore-reporter.png"
else
  : > "$APPDIR/logiqore-reporter.png"
fi

rm -f "$OUTPUT"
appimagetool "$APPDIR" "$OUTPUT"

echo "Created AppImage: $OUTPUT"
