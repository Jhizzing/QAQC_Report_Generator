#!/usr/bin/env python3
"""Generate a beta download manifest for LogiQore Reporter release assets."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Dict


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate LogiQore Reporter beta manifest from packaged release assets.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--release-assets-dir",
        type=Path,
        required=True,
        help="Directory that contains packaged release assets.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to write JSON manifest.",
    )
    parser.add_argument(
        "--version",
        type=str,
        default=os.environ.get("GITHUB_REF_NAME", "dev"),
        help="Version/tag to include in the manifest.",
    )
    parser.add_argument(
        "--channel",
        type=str,
        default="beta",
        help="Release channel label.",
    )
    parser.add_argument(
        "--base-download-url",
        type=str,
        default="",
        help="Optional URL prefix for hosted artifacts.",
    )
    return parser.parse_args()


def load_checksums(path: Path) -> Dict[str, str]:
    """Load SHA256 sums from a checksum manifest file."""
    checksums: Dict[str, str] = {}
    if not path.exists():
        return checksums

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        digest, rel_path = parts
        rel_path = rel_path.strip()
        # sha256sum output can contain prefixes like "./"
        rel_name = PurePosixPath(rel_path.lstrip("./")).name
        checksums[rel_name] = digest
    return checksums


def build_manifest(args: argparse.Namespace) -> dict:
    assets_dir = args.release_assets_dir.resolve()
    checksums = load_checksums(assets_dir / "SHA256SUMS.txt")
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    artifacts = []
    for path in sorted(assets_dir.iterdir()):
        if not path.is_file():
            continue
        if path.resolve() == args.output.resolve():
            continue

        artifact = {
            "name": path.name,
            "size_bytes": path.stat().st_size,
            "sha256": checksums.get(path.name),
        }

        if args.base_download_url:
            artifact["download_url"] = f"{args.base_download_url.rstrip('/')}/{path.name}"

        artifacts.append(artifact)

    return {
        "product": "LogiQore Reporter",
        "channel": args.channel,
        "version": args.version,
        "generated_at": timestamp,
        "artifacts": artifacts,
    }


def main() -> None:
    args = parse_args()
    if not args.release_assets_dir.exists():
        raise SystemExit(f"Release assets directory not found: {args.release_assets_dir}")

    manifest = build_manifest(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote beta manifest: {args.output}")


if __name__ == "__main__":
    main()
