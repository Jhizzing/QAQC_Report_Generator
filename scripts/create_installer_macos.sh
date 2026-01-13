#!/bin/bash
# Create macOS installer (DMG) for QAQC application

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DIST_DIR="$PROJECT_ROOT/dist"
BUILD_DIR="$PROJECT_ROOT/build"

echo "Creating macOS installer..."

# Check if GUI executable exists
GUI_EXE="$DIST_DIR/gui/QAQC-GUI"
if [ ! -f "$GUI_EXE" ]; then
    echo "Error: GUI executable not found at $GUI_EXE"
    echo "Please build the executable first: python scripts/build_executables.py --target gui"
    exit 1
fi

# Create .app bundle structure
APP_NAME="QAQC-GUI.app"
APP_DIR="$DIST_DIR/$APP_NAME"
APP_CONTENTS="$APP_DIR/Contents"
APP_MACOS="$APP_CONTENTS/MacOS"
APP_RESOURCES="$APP_CONTENTS/Resources"

echo "Creating .app bundle..."
rm -rf "$APP_DIR"
mkdir -p "$APP_MACOS"
mkdir -p "$APP_RESOURCES"

# Copy executable
cp "$GUI_EXE" "$APP_MACOS/QAQC-GUI"
chmod +x "$APP_MACOS/QAQC-GUI"

# Create Info.plist
cat > "$APP_CONTENTS/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>QAQC-GUI</string>
    <key>CFBundleIdentifier</key>
    <string>com.qaqc.reportgenerator</string>
    <key>CFBundleName</key>
    <string>QAQC Report Generator</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>QAQC</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
</dict>
</plist>
EOF

# Create DMG
DMG_NAME="QAQC-GUI-macos.dmg"
DMG_PATH="$DIST_DIR/$DMG_NAME"

echo "Creating DMG..."
rm -f "$DMG_PATH"

# Create temporary directory for DMG contents
DMG_TEMP="$BUILD_DIR/dmg_temp"
rm -rf "$DMG_TEMP"
mkdir -p "$DMG_TEMP"

# Copy app to temp directory
cp -R "$APP_DIR" "$DMG_TEMP/"

# Create Applications symlink
ln -s /Applications "$DMG_TEMP/Applications"

# Create DMG
hdiutil create -volname "QAQC Report Generator" \
    -srcfolder "$DMG_TEMP" \
    -ov -format UDZO \
    "$DMG_PATH"

echo "✅ DMG created: $DMG_PATH"

# Optional: Codesign (requires Developer ID)
if [ -n "$CODESIGN_IDENTITY" ]; then
    echo "Codesigning application..."
    codesign --deep --force --options runtime \
        --sign "$CODESIGN_IDENTITY" \
        "$APP_DIR"
    echo "✅ Application codesigned"
fi

echo "✅ macOS installer created successfully!"
