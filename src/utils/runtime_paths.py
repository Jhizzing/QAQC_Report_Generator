"""Helpers for locating resource files in both source and bundled builds."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, List, Optional

# Source checkout root (../.. from this file).
_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _unique_paths(paths: Iterable[Path]) -> List[Path]:
    seen: set[Path] = set()
    ordered: List[Path] = []
    for path in paths:
        if path and path not in seen:
            ordered.append(path)
            seen.add(path)
    return ordered


def candidate_roots(include_cwd: bool = True) -> List[Path]:
    """Return directories that may contain packaged resources."""
    roots: List[Path] = []

    frozen_root = getattr(sys, "_MEIPASS", None)
    if frozen_root:
        roots.append(Path(frozen_root))

    if getattr(sys, "frozen", False):  # Executable produced by PyInstaller
        try:
            roots.append(Path(sys.executable).resolve().parent)
        except Exception:  # pragma: no cover - defensive guard
            pass

    roots.append(_PROJECT_ROOT)

    if include_cwd:
        try:
            roots.append(Path.cwd())
        except Exception:  # pragma: no cover - cwd may be unavailable in rare cases
            pass

    return _unique_paths(roots)


def resolve_runtime_path(
    relative_path: str | Path,
    *,
    must_exist: bool = True,
    include_cwd: bool = True,
) -> Optional[Path]:
    """
    Resolve a resource path regardless of whether the app is frozen.

    Args:
        relative_path: Relative or absolute path to resolve.
        must_exist: If True, returns None when the file is missing.
        include_cwd: Whether to consider the current working directory first.

    Returns:
        Absolute Path to the resource if found; otherwise None (or the best-effort
        absolute path when must_exist=False).
    """

    rel = Path(relative_path)
    if rel.is_absolute():
        if rel.exists() or not must_exist:
            return rel
        return None

    search_roots = candidate_roots(include_cwd=include_cwd)
    for root in search_roots:
        candidate = root / rel
        if candidate.exists():
            return candidate

    if must_exist:
        return None

    # Fall back to placing the file alongside the executable/project root.
    return search_roots[0] / rel if search_roots else rel
