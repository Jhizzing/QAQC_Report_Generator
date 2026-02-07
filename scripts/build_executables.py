#!/usr/bin/env python3
"""Helper to build QAQC executables via PyInstaller."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPEC_DIR = PROJECT_ROOT / "packaging" / "pyinstaller"
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build" / "pyinstaller"

TARGET_MAP = {
    "cli": SPEC_DIR / "qaqc_cli.spec",
    "gui": SPEC_DIR / "qaqc_gui.spec",
}


def _ensure_pyinstaller_available() -> None:
    try:
        import PyInstaller  # noqa: F401
    except ImportError as exc:  # pragma: no cover - utility guard
        raise SystemExit(
            "PyInstaller is not installed. Run 'pip install pyinstaller' inside your environment."
        ) from exc


def _build_target(
    target: str,
    spec_path: Path,
    *,
    clean: bool,
    dist_root: Path,
    build_root: Path,
    extra_args: Iterable[str],
) -> int:
    dist_path = dist_root / target
    build_path = build_root / target
    dist_path.mkdir(parents=True, exist_ok=True)
    build_path.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--distpath",
        str(dist_path),
        "--workpath",
        str(build_path),
    ]

    if clean:
        cmd.append("--clean")

    if extra_args:
        cmd.extend(extra_args)

    cmd.append(str(spec_path))

    print(f"\n[build] Target={target} -> {' '.join(cmd)}")
    env = os.environ.copy()
    env["QAQC_PROJECT_ROOT"] = str(PROJECT_ROOT)
    result = subprocess.run(cmd, check=False, cwd=PROJECT_ROOT, env=env)
    if result.returncode == 0:
        print(f"[build] Success ({target}) -> {dist_path}")
    else:
        print(f"[build] Failed ({target}) with exit code {result.returncode}")
    return result.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build QAQC CLI and GUI executables using PyInstaller",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--target",
        choices=["cli", "gui", "all"],
        default="all",
        help="Which executable(s) to build",
    )
    parser.add_argument(
        "--dist-dir",
        type=Path,
        default=DIST_DIR,
        help="Output directory for built artifacts",
    )
    parser.add_argument(
        "--build-dir",
        type=Path,
        default=BUILD_DIR,
        help="Temporary build directory",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Pass --clean to PyInstaller to remove cached state",
    )
    parser.add_argument(
        "--pyinstaller-arg",
        action="append",
        default=[],
        help="Additional argument to forward to PyInstaller (may be repeated)",
    )
    return parser.parse_args()


def _get_version() -> str:
    """Get application version from config or git."""
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'describe', '--tags', '--always'],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    
    # Fallback to version from config or default
    try:
        import yaml
        config_path = PROJECT_ROOT / "config.yaml"
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f)
                return config.get('version', '1.0.0')
    except Exception:
        pass
    
    return '1.0.0'


def _verify_build(executable_path: Path) -> bool:
    """Verify that built executable exists and is valid."""
    if not executable_path.exists():
        print(f"[verify] Executable not found: {executable_path}")
        return False
    
    if executable_path.stat().st_size == 0:
        print(f"[verify] Executable is empty: {executable_path}")
        return False
    
    print(f"[verify] Executable verified: {executable_path} ({executable_path.stat().st_size / 1024 / 1024:.1f} MB)")
    return True


def main() -> None:
    args = parse_args()
    _ensure_pyinstaller_available()

    version = _get_version()
    print(f"[build] Building version: {version}")

    targets = list(TARGET_MAP.keys()) if args.target == "all" else [args.target]

    failures = []
    for target in targets:
        spec_path = TARGET_MAP[target]
        if not spec_path.exists():
            raise SystemExit(f"Spec file not found: {spec_path}")

        code = _build_target(
            target,
            spec_path,
            clean=args.clean,
            dist_root=args.dist_dir,
            build_root=args.build_dir,
            extra_args=args.pyinstaller_arg,
        )
        if code != 0:
            failures.append((target, code))
        else:
            # Verify build
            dist_path = args.dist_dir / target
            if target == "cli":
                exe_name = "QAQC-CLI.exe" if sys.platform == "win32" else "QAQC-CLI"
            else:
                exe_name = "QAQC-GUI.exe" if sys.platform == "win32" else "QAQC-GUI"
            
            executable_path = dist_path / exe_name
            if not _verify_build(executable_path):
                failures.append((target, -1))

    if failures:
        summary = ", ".join(f"{target} (exit {code})" for target, code in failures)
        raise SystemExit(f"One or more builds failed: {summary}")
    
    print(f"\n[build] All builds completed successfully!")
    print(f"[build] Output directory: {args.dist_dir}")


if __name__ == "__main__":
    main()
