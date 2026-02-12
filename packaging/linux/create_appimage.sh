#!/usr/bin/env bash
set -euo pipefail

# Build AppImage from PyInstaller GUI onefile output.
# Requirements: appimagetool installed and available on PATH.
# Usage:
#   bash packaging/linux/create_appimage.sh [version]

VERSION="${1:-1.0.0-pre}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GUI_BIN="$ROOT_DIR/dist/gui/QAQC-GUI"
APPDIR="$ROOT_DIR/build/appimage/AppDir"
OUTPUT="$ROOT_DIR/dist/gui/QAQC-GUI-${VERSION}-x86_64.AppImage"

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

cp "$GUI_BIN" "$APPDIR/usr/bin/QAQC-GUI"
chmod +x "$APPDIR/usr/bin/QAQC-GUI"

cat > "$APPDIR/qaqc.desktop" <<DESKTOP
[Desktop Entry]
Type=Application
Name=QAQC GUI
Comment=QAQC analysis and reporting application
Exec=QAQC-GUI
Icon=qaqc
Categories=Science;Education;
Terminal=false
DESKTOP

cp "$APPDIR/qaqc.desktop" "$APPDIR/usr/share/applications/qaqc.desktop"

# Minimal launcher expected by AppImage
cat > "$APPDIR/AppRun" <<'APPRUN'
#!/usr/bin/env bash
HERE="$(dirname "$(readlink -f "$0")")"
exec "$HERE/usr/bin/QAQC-GUI" "$@"
APPRUN
chmod +x "$APPDIR/AppRun"

# Placeholder icon (replace with branded icon file when available)
if [[ -f "$ROOT_DIR/assets/icon.png" ]]; then
  cp "$ROOT_DIR/assets/icon.png" "$APPDIR/qaqc.png"
  cp "$ROOT_DIR/assets/icon.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/qaqc.png"
else
  : > "$APPDIR/qaqc.png"
fi

rm -f "$OUTPUT"
appimagetool "$APPDIR" "$OUTPUT"

echo "Created AppImage: $OUTPUT"
