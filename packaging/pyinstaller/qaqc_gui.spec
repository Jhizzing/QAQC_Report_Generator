# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for QAQC PyQt6 GUI executable (single-file)."""

from pathlib import Path

block_cipher = None

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MAIN_SCRIPT = PROJECT_ROOT / "launch_gui.py"
SPEC_NAME = "qaqc_gui"


def _collect_data_files() -> list:
    datas = []

    def add(path: str, target: str = "."):
        abs_path = PROJECT_ROOT / path
        if abs_path.exists():
            datas.append((str(abs_path), target))

    add("config.yaml")
    add("crm_database.yaml")
    add("config", "config")
    add("mock_data", "mock_data")
    add("assets", "assets")
    return datas


datas = _collect_data_files()


a = Analysis(
    [str(MAIN_SCRIPT)],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=["PyQt6.QtSvg", "PyQt6.QtSvgWidgets"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="QAQC-GUI",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
