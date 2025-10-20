#!/usr/bin/env python3
"""
QAQC Analysis Automation Application - Main Entry Point

This is the main entry point for the QAQC Analysis Automation application.
It provides both command-line and GUI interfaces for analyzing drilling assay data.
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional, Dict, Tuple, List
import json
import platform
import datetime as _dt

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data import DataImporter, DataProcessor  # noqa: E402
from src.analysis import QAQCAnalyzer  # noqa: E402
from src.visualization import PlotGenerator  # noqa: E402
from src.reporting import ReportGenerator  # noqa: E402

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def load_config(config_file: str) -> Dict:
    if not os.path.exists(config_file):
        return {}
    if yaml is None:
        return {}
    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="QAQC Analysis Automation Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with GUI interface
  python main.py --gui

  # Process one file with mapping and normalization
  python main.py --input input/assays.csv --output output --mapping mapping.yaml --normalize-results

  # Infer mapping then normalize (no mapping file yet)
  python main.py --input input/assays.csv --output output --infer-mapping --normalize-results --yes

  # Process a directory of files
  python main.py --input input/ --output output --infer-mapping --normalize-results --yes
        """
    )

    parser.add_argument(
        "--input", "-i",
        type=str,
        help="Input data file or directory (CSV, XLSX, or XLS, or a folder containing them)"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        default="output",
        help="Output directory for reports and plots (default: output)"
    )

    parser.add_argument(
        "--config", "-c",
        type=str,
        default="config.yaml",
        help="Configuration file (default: config.yaml)"
    )

    # Mapping / normalization flags
    parser.add_argument(
        "--mapping",
        type=str,
        help="Path to a YAML column mapping file to apply"
    )
    parser.add_argument(
        "--infer-mapping",
        action="store_true",
        help="Infer column mapping from headers using synonyms and fuzzy matching"
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Auto-accept inferred mapping if confidence is sufficient"
    )
    parser.add_argument(
        "--normalize-results",
        action="store_true",
        help="Parse qualifiers and detection limits into normalized columns"
    )
    parser.add_argument(
        "--csv-delimiter",
        type=str,
        help="CSV delimiter (e.g., ',' or ';'). If omitted, pandas will infer."
    )
    parser.add_argument(
        "--encoding",
        type=str,
        default="utf-8",
        help="Text encoding for CSV files (default: utf-8). Use 'utf-8-sig' for BOM CSVs."
    )
    parser.add_argument(
        "--sheet",
        type=str,
        help="Excel sheet name to read (alternative to --sheet-index)"
    )
    parser.add_argument(
        "--sheet-index",
        type=int,
        help="Excel sheet index to read (0-based; default 0)"
    )
    parser.add_argument(
        "--save-mapping",
        type=str,
        help="If provided, save the accepted mapping to this YAML file for reuse"
    )
    parser.add_argument(
        "--csv-chunksize",
        type=int,
        help="If set, stream CSV in chunks of this many rows and concatenate (memory-friendly)"
    )
    parser.add_argument(
        "--detect-encoding-fallback",
        action="store_true",
        help="On CSV read error, try common encodings (utf-8-sig, cp1252, latin1)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show actions without writing output files"
    )

    parser.add_argument(
        "--gui", "-g",
        action="store_true",
        help="Launch GUI interface"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="QAQC Analysis Automation v1.0.0"
    )

    args = parser.parse_args()

    # Launch GUI if requested
    if args.gui:
        launch_gui()
        return

    # Command line processing
    if not args.input:
        print("Error: Input file or directory is required for command line processing.")
        print("Use --help for usage information or --gui for GUI interface.")
        sys.exit(1)

    try:
        process_data(args)
    except Exception as e:  # noqa: BLE001
        print(f"Error processing data: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def launch_gui():
    """Launch the GUI interface."""
    try:
        from src.gui.main_window import QAQCApplication
        app = QAQCApplication()
        app.run()
    except ImportError:
        print("GUI dependencies not available. Please install PySide6 or tkinter.")
        print("Falling back to command line interface...")
        print("Use --help for command line options.")
    except Exception as e:  # noqa: BLE001
        print(f"Error launching GUI: {e}")
        sys.exit(1)


def _review_and_build_mapping(
    importer: DataImporter,
    df,
    infer: bool,
    mapping_path: Optional[str],
    auto_accept: bool,
    verbose: bool,
    threshold: float = 0.85,
) -> Dict[str, str]:
    """Load mapping or infer and review with confidence; enforce acceptance policy."""
    # If mapping file provided, load and return directly
    if mapping_path:
        mapping = importer.load_mapping_yaml(mapping_path)
        if verbose:
            print(f"Loaded mapping from {mapping_path}: {mapping}")
        return mapping

    if not infer:
        return {}

    suggestions = importer.suggest_mapping(list(df.columns), threshold=threshold)

    # Build proposed mapping from suggestions above threshold
    proposed: Dict[str, str] = {}
    low_conf_required: List[str] = []
    missing_required: List[str] = []

    required_fields = ("sample_id", "sample_type", "result")

    # Print a simple review table
    if verbose:
        print("Suggested column mapping (confidence):")
        print("  canonical_field -> header (confidence)")
        for canonical, (header, score) in suggestions.items():
            tag = ""
            if canonical in required_fields and (header is None or score < threshold):
                tag = "  [REQUIRED: review]"
            print(f"  {canonical:<14} -> {str(header):<20} ({score:.2f}){tag}")

    for canonical, (header, score) in suggestions.items():
        if header is not None and score >= threshold:
            proposed[header] = canonical
        if canonical in required_fields:
            if header is None:
                missing_required.append(canonical)
            elif score < threshold:
                low_conf_required.append(canonical)

    # Enforce acceptance policy
    if (missing_required or low_conf_required) and not auto_accept:
        print("\nMapping requires review:")
        if missing_required:
            print("  Missing required fields:", ", ".join(missing_required))
        if low_conf_required:
            print("  Low-confidence required fields:", ", ".join(low_conf_required))
        print("\nRe-run with either:")
        print("  --mapping path/to/mapping.yaml   (to provide explicit mapping)")
        print("  --infer-mapping --yes            (to auto-accept suggestions)")
        sys.exit(2)

    if verbose and auto_accept:
        print("Auto-accepted inferred mapping:", proposed)

    return proposed


def _write_provenance(
    *,
    out_path: Path,
    src: Path,
    df_before_cols: List[str],
    df_before_rows: int,
    df_after,
    mapping_used: Dict[str, str],
    mapping_source: str,
    confidence_threshold: float,
    normalize_enabled: bool,
    default_dl: Optional[float],
    used_per_row_dl: bool,
    csv_delimiter: Optional[str],
    encoding: str,
    sheet_name: Optional[object],
    dry_run: bool,
) -> None:
    provenance = {
        "timestamp": _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "appVersion": "1.0.0",
        "python": platform.python_version(),
        "input": {
            "path": str(src),
            "type": src.suffix.lower().lstrip("."),
            "encoding": encoding,
            "csvDelimiter": csv_delimiter,
            "sheet": sheet_name,
        },
        "mapping": {
            "source": mapping_source,
            "confidenceThreshold": confidence_threshold,
            "used": mapping_used,
        },
        "normalization": {
            "enabled": bool(normalize_enabled),
            "defaultDetectionLimit": default_dl,
            "usedPerRowDL": bool(used_per_row_dl),
            "negativeValuesAsBelowDL": True,
            "tokens": ["ND", "<DL", ">DL"],
        },
        "output": {
            "path": str(out_path),
            "inputRows": int(df_before_rows),
            "outputRows": int(getattr(df_after, "shape", (0, 0))[0]),
            "columns": list(getattr(df_after, "columns", [])),
            "inputColumns": list(df_before_cols),
        },
    }

    prov_path = out_path.with_suffix(".provenance.json")
    if dry_run:
        print(json.dumps(provenance, indent=2))
    else:
        with open(prov_path, "w", encoding="utf-8") as f:
            json.dump(provenance, f, indent=2)


def process_data(args) -> None:
    """Process QAQC data from command line."""
    verbose = bool(args.verbose)
    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    config = load_config(args.config)
    default_dl = None
    try:
        default_dl = (
            config.get("data", {})
            .get("cleaning", {})
            .get("default_detection_limit")
        )
    except Exception:
        default_dl = None

    importer = DataImporter()

    # Collect inputs
    if input_path.is_dir():
        frames = importer.read_from_directory(
            input_path,
            csv_delimiter=args.csv_delimiter,
            encoding=args.encoding,
            sheet_name=(args.sheet if args.sheet is not None else (args.sheet_index if args.sheet_index is not None else 0)),
            csv_chunksize=args.csv_chunksize,
            detect_encoding_fallback=bool(args.detect_encoding_fallback),
        )
    else:
        frames = [
            type("_tmp", (), {
                "dataframe": importer.read_table(
                    input_path,
                    csv_delimiter=args.csv_delimiter,
                    encoding=args.encoding,
                    sheet_name=(args.sheet if args.sheet is not None else (args.sheet_index if args.sheet_index is not None else 0)),
                    csv_chunksize=args.csv_chunksize,
                    detect_encoding_fallback=bool(args.detect_encoding_fallback),
                ),
                "source_path": input_path,
            })()
        ]

    wrote_any = False
    for item in frames:
        df = item.dataframe
        src = Path(item.source_path)
        df_before_cols = list(df.columns)
        df_before_rows = len(df)

        # Determine mapping (load or infer, with review)
        mapping_source = "none"
        mapping = _review_and_build_mapping(
            importer,
            df,
            infer=bool(args.infer_mapping),
            mapping_path=args.mapping,
            auto_accept=bool(args.yes),
            verbose=verbose,
            threshold=0.85,
        )
        if args.mapping:
            mapping_source = "file"
        elif args.infer_mapping:
            mapping_source = "inferred"

        if mapping:
            df = importer.apply_mapping(df, mapping)
            # Save mapping if requested
            if args.save_mapping:
                try:
                    importer.save_mapping_yaml(mapping, args.save_mapping)
                    if verbose:
                        print(f"Saved mapping to {args.save_mapping}")
                except Exception as e:  # noqa: BLE001
                    print(f"Warning: failed to save mapping to {args.save_mapping}: {e}")

        # Validate required columns if mapping applied or already present
        required = ("sample_id", "sample_type", "result")
        missing = importer.validate_required({k: k if k in df.columns else None for k in required})
        if missing:
            print(f"Error: missing required columns after mapping: {missing}")
            print("Available columns:", ", ".join(df.columns))
            # Show top-3 candidates for each missing field
            suggestions = importer.suggest_mapping(list(df.columns), threshold=0.0)
            for canonical in missing:
                # Build scores for all headers
                scores = []
                for header, (hmatch, score) in suggestions.items():
                    # suggestions is keyed by canonical; we want per-canonical header scores
                    pass
            # Recompute focused suggestions per missing canonical
            for canonical in missing:
                norm_headers = {importer.normalize_header(h): h for h in df.columns}
                targets = {canonical} | set(SYNONYMS.get(canonical, ()))
                targets_norm = [importer.normalize_header(t) for t in targets]
                ranked = []
                for nh_norm, original in norm_headers.items():
                    import difflib as _d
                    score = max(_d.SequenceMatcher(a=nh_norm, b=tg).ratio() for tg in targets_norm)
                    ranked.append((score, original))
                ranked.sort(reverse=True)
                top = ", ".join(f"{h}({s:.2f})" for s, h in ranked[:3])
                print(f"Suggested candidates for '{canonical}': {top}")
            print("Provide a mapping file with --mapping or re-run with --infer-mapping and --yes after reviewing suggestions.")
            sys.exit(2)

        used_per_row_dl = False
        # Normalize results if requested
        if args.normalize_results:
            used_per_row_dl = "detection_limit" in df.columns
            df = importer.normalize_results(
                df,
                result_col="result",
                qualifier_col="qualifier",
                dl_col="detection_limit",
                default_dl=default_dl,
            )

        # Write output CSV unless dry-run
        out_name = f"{src.stem}_clean.csv"
        out_path = output_dir / out_name
        if args.dry_run:
            if verbose:
                print(f"Dry run: would write {out_path}")
        else:
            df.to_csv(out_path, index=False)
            wrote_any = True
            if verbose:
                print(f"Wrote {out_path}")

        # Write provenance
        _write_provenance(
            out_path=out_path,
            src=src,
            df_before_cols=df_before_cols,
            df_before_rows=df_before_rows,
            df_after=df,
            mapping_used=mapping,
            mapping_source=mapping_source,
            confidence_threshold=0.85,
            normalize_enabled=bool(args.normalize_results),
            default_dl=default_dl,
            used_per_row_dl=used_per_row_dl,
            csv_delimiter=args.csv_delimiter,
            encoding=args.encoding,
            sheet_name=(args.sheet if args.sheet is not None else (args.sheet_index if args.sheet_index is not None else 0)),
            dry_run=bool(args.dry_run),
        )

    if not wrote_any and not args.dry_run:
        if verbose:
            print("No files written. Check input path or filters.")


if __name__ == "__main__":
    main()
