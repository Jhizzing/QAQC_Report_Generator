#!/bin/bash
# Create Linux installer (AppImage) for QAQC application

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DIST_DIR="$PROJECT_ROOT/dist"
BUILD_DIR="$PROJECT_ROOT/build"

echo "Creating Linux AppImage..."

# Check if GUI executable exists
GUI_EXE="$DIST_DIR/gui/QAQC-GUI"
if [ ! -f "$GUI_EXE" ]; then
    echo "Error: GUI executable not found at $GUI_EXE"
    echo "Please build the executable first: python scripts/build_executables.py --target gui"
    exit 1
fi

# Check for appimagetool
if ! command -v appimagetool &> /dev/null; then
    echo "Warning: appimagetool not found. Installing..."
    echo "Download from: https://github.com/AppImage/AppImageKit/releases"
    echo "Or install via: wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    echo "chmod +x appimagetool-x86_64.AppImage"
    echo "sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool"
    exit 1
fi

# Create AppDir structure
APP_DIR="$BUILD_DIR/AppDir"
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR/usr/bin"
mkdir -p "$APP_DIR/usr/share/applications"
mkdir -p "$APP_DIR/usr/share/icons/hicolor/256x256/apps"

# Copy executable
cp "$GUI_EXE" "$APP_DIR/usr/bin/qaqc-gui"
chmod +x "$APP_DIR/usr/bin/qaqc-gui"

# Create .desktop file
cat > "$APP_DIR/usr/share/applications/qaqc-gui.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=QAQC Report Generator
Comment=Quality Assurance/Quality Control analysis for geochemical data
Exec=qaqc-gui
Icon=qaqc-gui
Categories=Science;Geology;
Terminal=false
EOF

# Create AppRun
cat > "$APP_DIR/AppRun" <<'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
exec "${HERE}/usr/bin/qaqc-gui" "$@"
EOF
chmod +x "$APP_DIR/AppRun"

# Create AppImage
APPIMAGE_NAME="QAQC-GUI-x86_64.AppImage"
APPIMAGE_PATH="$DIST_DIR/$APPIMAGE_NAME"

echo "Creating AppImage..."
appimagetool "$APP_DIR" "$APPIMAGE_PATH"

echo "✅ AppImage created: $APPIMAGE_PATH"

# Make executable
chmod +x "$APPIMAGE_PATH"

echo "✅ Linux installer created successfully!"
