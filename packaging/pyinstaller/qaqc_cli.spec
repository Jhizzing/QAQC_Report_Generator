# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for QAQC CLI executable (single-file)."""

import os
from pathlib import Path

block_cipher = None

# PyInstaller may execute spec files without __file__ set.
PROJECT_ROOT = Path(os.environ.get("QAQC_PROJECT_ROOT", Path.cwd())).resolve()
MAIN_SCRIPT = PROJECT_ROOT / "main.py"
SPEC_NAME = "qaqc_cli"


def _collect_data_files() -> list:
    datas = []

    def add(path: str, target: str = "."):
        abs_path = PROJECT_ROOT / path
        if abs_path.exists():
            datas.append((str(abs_path), target))

    # Ship default configuration + reference data so first run works offline.
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
    hiddenimports=[],
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
    name="QAQC-CLI",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
