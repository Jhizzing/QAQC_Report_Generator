#!/usr/bin/env bash
set -euo pipefail

# Build a simple macOS .app wrapper + DMG from PyInstaller onefile output.
# Usage:
#   bash packaging/macos/create_dmg.sh [version]

VERSION="${1:-1.0.0-pre}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GUI_DIST_DIR="$ROOT_DIR/dist/gui"
GUI_BIN="$GUI_DIST_DIR/LogiQore-Reporter-GUI"
APP_NAME="LogiQore Reporter.app"
APP_DIR="$GUI_DIST_DIR/$APP_NAME"
DMG_PATH="$GUI_DIST_DIR/LogiQore-Reporter-${VERSION}.dmg"

if [[ ! -f "$GUI_BIN" ]]; then
  echo "GUI executable not found: $GUI_BIN"
  echo "Build first: python scripts/build_executables.py --target gui --clean"
  exit 1
fi

rm -rf "$APP_DIR"
mkdir -p "$APP_DIR/Contents/MacOS" "$APP_DIR/Contents/Resources"

cp "$GUI_BIN" "$APP_DIR/Contents/MacOS/LogiQore-Reporter-GUI"
chmod +x "$APP_DIR/Contents/MacOS/LogiQore-Reporter-GUI"

cat > "$APP_DIR/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key>
  <string>LogiQore Reporter</string>
  <key>CFBundleDisplayName</key>
  <string>LogiQore Reporter</string>
  <key>CFBundleIdentifier</key>
  <string>com.logiqore.reporter</string>
  <key>CFBundleVersion</key>
  <string>${VERSION}</string>
  <key>CFBundleShortVersionString</key>
  <string>${VERSION}</string>
  <key>CFBundleExecutable</key>
  <string>LogiQore-Reporter-GUI</string>
  <key>CFBundlePackageType</key>
  <string>APPL</string>
  <key>LSMinimumSystemVersion</key>
  <string>12.0</string>
  <key>NSHighResolutionCapable</key>
  <true/>
</dict>
</plist>
PLIST

if [[ -n "${CODESIGN_IDENTITY:-}" ]]; then
  echo "Signing app with identity: $CODESIGN_IDENTITY"
  codesign --deep --force --options runtime --sign "$CODESIGN_IDENTITY" "$APP_DIR"
fi

rm -f "$DMG_PATH"
hdiutil create -volname "LogiQore Reporter ${VERSION}" -srcfolder "$APP_DIR" -ov -format UDZO "$DMG_PATH"

echo "Created DMG: $DMG_PATH"
