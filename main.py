#!/usr/bin/env python3
"""
LogiQore Reporter - Main Entry Point.

This is the main entry point for LogiQore Reporter. It provides comprehensive
QAQC analysis including standards, blanks, duplicates, and CRM integration with
professional reporting capabilities.
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional, Dict, Tuple, List
import json
import platform
import datetime as _dt
import pandas as pd

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data import DataImporter, DataProcessor  # noqa: E402
from src.data.crm_manager import CRMManager  # noqa: E402
from src.analysis import StandardsAnalyzer, BlanksAnalyzer, DuplicatesAnalyzer  # noqa: E402
from src.visualization import PlotGenerator  # noqa: E402
from src.reporting import ExcelReporter, PDFReporter  # noqa: E402
from src.utils.runtime_paths import resolve_runtime_path  # noqa: E402

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

# ─── Rich Console Setup ─────────────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
    from rich.text import Text
    from rich.theme import Theme
    from rich import box

    # LogiQore branded theme
    logiqore_theme = Theme({
        "primary": "bold #F59E0B",
        "accent": "#0EA5E9",
        "surface": "#1E293B",
        "success": "bold #10B981",
        "warning": "bold #F59E0B",
        "error": "bold #EF4444",
        "info": "bold #3B82F6",
        "muted": "#94A3B8",
        "heading": "bold #F1F5F9",
        "pass_status": "bold #10B981",
        "fail_status": "bold #EF4444",
        "warn_status": "bold #F59E0B",
    })

    console = Console(theme=logiqore_theme)
    RICH_AVAILABLE = True

except ImportError:
    RICH_AVAILABLE = False
    console = None


def _strip_markup(text: str) -> str:
    """Strip Rich markup tags like [bold], [muted], [/] etc. from text."""
    import re
    return re.sub(r'\[/?[^\]]*\]', '', text)


def rprint(*args, **kwargs):
    """Print using Rich if available, else fallback to plain print."""
    if RICH_AVAILABLE and console:
        console.print(*args, **kwargs)
    else:
        plain = " ".join(str(a) for a in args)
        print(_strip_markup(plain))


def show_banner():
    """Display the LogiQore branded banner."""
    if not RICH_AVAILABLE:
        print("=" * 58)
        print("  LogiQore Reporter v2.0.0")
        print("  Secure, Intelligent Assay QAQC Analysis")
        print("=" * 58)
        return

    banner_text = Text()
    banner_text.append("  LogiQore Reporter", style="bold #F59E0B")
    banner_text.append("  v2.0.0\n", style="#94A3B8")
    banner_text.append("  Secure, Intelligent Assay QAQC Analysis", style="#CBD5E1")

    console.print()
    console.print(Panel(
        banner_text,
        border_style="#F59E0B",
        box=box.DOUBLE_EDGE,
        padding=(1, 2),
    ))
    console.print()


def show_status(label: str, status: str, detail: str = ""):
    """Show a status line with pass/fail/warning indicators."""
    if not RICH_AVAILABLE:
        icon = {"PASS": "[PASS]", "FAIL": "[FAIL]", "WARN": "[WARN]", "SKIP": "[SKIP]", "INFO": "[INFO]"}.get(status, "[----]")
        suffix = f" -- {detail}" if detail else ""
        print(f"  {icon} {label}{suffix}")
        return

    icon_map = {
        "PASS": ("[bold #10B981]OK[/]", "pass_status"),
        "FAIL": ("[bold #EF4444]FAIL[/]", "fail_status"),
        "WARN": ("[bold #F59E0B]WARN[/]", "warn_status"),
        "SKIP": ("[#94A3B8]SKIP[/]", "muted"),
        "INFO": ("[bold #3B82F6]INFO[/]", "info"),
    }
    icon, style = icon_map.get(status, ("[#94A3B8]--[/]", "muted"))
    suffix = f"  [muted]{detail}[/]" if detail else ""
    console.print(f"  {icon}  [{style}]{label}[/]{suffix}")


def show_summary_table(analysis_results: Dict, output_dir: Path):
    """Display a rich summary table of analysis results."""
    if not RICH_AVAILABLE:
        print("\n--- Analysis Summary ---")
        for key, val in analysis_results.items():
            if isinstance(val, dict) and 'overall_acceptable' in val:
                status = "PASS" if val['overall_acceptable'] else "FAIL"
                print(f"  {key}: {status}")
        return

    table = Table(
        title="QAQC Analysis Summary",
        title_style="primary",
        border_style="#334155",
        box=box.ROUNDED,
        show_header=True,
        header_style="heading",
        padding=(0, 2),
    )
    table.add_column("Analysis", style="heading", min_width=18)
    table.add_column("Status", justify="center", min_width=10)
    table.add_column("Details", style="muted", min_width=30)

    for analysis_type in ['standards', 'blanks', 'duplicates']:
        if analysis_type in analysis_results and isinstance(analysis_results[analysis_type], dict):
            result = analysis_results[analysis_type]
            passed = result.get('overall_acceptable', False)
            status_text = "[pass_status]PASS[/]" if passed else "[fail_status]FAIL[/]"

            details = []
            if 'mean_z_score' in result:
                details.append(f"Z={result['mean_z_score']:.2f}")
            if 'mean_recovery' in result:
                details.append(f"Rec={result['mean_recovery']:.1f}%")
            if 'mean_rpd' in result:
                details.append(f"RPD={result['mean_rpd']:.1f}%")
            if 'count' in result:
                details.append(f"n={result['count']}")

            table.add_row(
                analysis_type.capitalize(),
                status_text,
                ", ".join(details) if details else "--"
            )
        else:
            table.add_row(
                analysis_type.capitalize(),
                "[muted]SKIP[/]",
                "[muted]Not analysed[/]"
            )

    total = analysis_results.get('total_samples', 0)
    table.add_section()
    table.add_row("Total Samples", f"[primary]{total}[/]", f"Output: {output_dir}")

    console.print()
    console.print(table)
    console.print()


def create_progress():
    """Create a Rich progress bar context manager."""
    if not RICH_AVAILABLE:
        return None

    return Progress(
        SpinnerColumn(style="#F59E0B"),
        TextColumn("[primary]{task.description}[/]"),
        BarColumn(bar_width=30, style="#334155", complete_style="#F59E0B", finished_style="#10B981"),
        TextColumn("[muted]{task.percentage:>3.0f}%[/]"),
        TimeElapsedColumn(),
        console=console,
    )


def load_config(config_file: str) -> Dict:
    config_path = resolve_runtime_path(config_file)
    if config_path is None or not config_path.exists():
        return {}
    if yaml is None:
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="LogiQore Reporter -- Secure, Intelligent Assay QAQC Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis with auto-mapping and CRM selection
  python main.py --input input/assays.csv --output output --infer-mapping --normalize-results --yes --auto-crm --include-plots

  # Full analysis with specific CRM
  python main.py --input input/assays.csv --output output --crm-name "NIST SRM 2709a" --include-plots --output-format both

  # Process directory with Excel output only
  python main.py --input input/ --output output --infer-mapping --normalize-results --yes --output-format excel

  # Skip specific analyses
  python main.py --input input/assays.csv --output output --skip-standards --skip-duplicates

  # Dry run to see what would be processed
  python main.py --input input/assays.csv --output output --infer-mapping --normalize-results --yes --dry-run --verbose
        """
    )

    parser.add_argument("--input", "-i", type=str, help="Input data file or directory (CSV, XLSX, or XLS)")
    parser.add_argument("--output", "-o", type=str, default="output", help="Output directory for reports (default: output)")
    parser.add_argument("--config", "-c", type=str, default="config.yaml", help="Configuration file (default: config.yaml)")

    # Mapping / normalization flags
    parser.add_argument("--mapping", type=str, help="Path to a YAML column mapping file to apply")
    parser.add_argument("--infer-mapping", action="store_true", help="Infer column mapping from headers using synonyms and fuzzy matching")
    parser.add_argument("--yes", action="store_true", help="Auto-accept inferred mapping if confidence is sufficient")
    parser.add_argument("--normalize-results", action="store_true", help="Parse qualifiers and detection limits into normalized columns")
    parser.add_argument("--csv-delimiter", type=str, help="CSV delimiter (e.g., ',' or ';'). If omitted, pandas will infer.")
    parser.add_argument("--encoding", type=str, default="utf-8", help="Text encoding for CSV files (default: utf-8)")
    parser.add_argument("--sheet", type=str, help="Excel sheet name to read (alternative to --sheet-index)")
    parser.add_argument("--sheet-index", type=int, help="Excel sheet index to read (0-based; default 0)")
    parser.add_argument("--save-mapping", type=str, help="Save the accepted mapping to this YAML file for reuse")
    parser.add_argument("--csv-chunksize", type=int, help="Stream CSV in chunks of this many rows (memory-friendly)")
    parser.add_argument("--detect-encoding-fallback", action="store_true", help="On CSV read error, try common encodings (utf-8-sig, cp1252, latin1)")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing output files")

    # CRM and Analysis options
    parser.add_argument("--crm-database", type=str, help="Path to CRM database YAML file (default: crm_database.yaml)")
    parser.add_argument("--crm-name", type=str, help="Specific CRM to use for standards analysis (e.g., 'NIST SRM 2709a')")
    parser.add_argument("--auto-crm", action="store_true", help="Automatically select appropriate CRM based on sample concentrations")
    parser.add_argument("--skip-standards", action="store_true", help="Skip standards analysis")
    parser.add_argument("--skip-blanks", action="store_true", help="Skip blanks analysis")
    parser.add_argument("--skip-duplicates", action="store_true", help="Skip duplicates analysis")

    # Output format options
    parser.add_argument("--output-format", choices=["excel", "pdf", "both"], default="both", help="Output format (default: both)")
    parser.add_argument("--include-plots", action="store_true", help="Generate visualization plots")
    parser.add_argument("--plot-format", choices=["png", "pdf", "svg"], default="png", help="Plot file format (default: png)")

    parser.add_argument("--gui", "-g", action="store_true", help="Launch GUI interface")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("--version", action="version", version="LogiQore Reporter v2.0.0")

    args = parser.parse_args()

    # Disable rich if --no-color
    global RICH_AVAILABLE, console
    if args.no_color:
        RICH_AVAILABLE = False
        console = None

    # Launch GUI if requested
    if args.gui:
        launch_gui()
        return

    # Command line processing
    if not args.input:
        show_banner()
        if RICH_AVAILABLE:
            console.print("[error]Error:[/] Input file or directory is required for command line processing.")
            console.print("[muted]Use [primary]--help[/primary] for usage information or [primary]--gui[/primary] for the GUI interface.[/]")
        else:
            print("Error: Input file or directory is required for command line processing.")
            print("Use --help for usage information or --gui for GUI interface.")
        sys.exit(1)

    try:
        show_banner()
        process_data(args)
    except Exception as e:  # noqa: BLE001
        if RICH_AVAILABLE:
            console.print(f"\n[error]Error processing data:[/] {e}")
            if args.verbose:
                console.print_exception()
        else:
            print(f"Error processing data: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
        sys.exit(1)


def launch_gui():
    """Launch the GUI interface."""
    try:
        from PyQt6.QtWidgets import QApplication
        from src.gui.main_window import QAQCApplication

        app = QApplication(sys.argv)
        app.setApplicationName("LogiQore Reporter")
        app.setApplicationVersion("2.0.0")
        app.setOrganizationName("LogiQore")

        window = QAQCApplication()
        window.show()

        rprint("[primary]LogiQore Reporter[/primary] GUI launched!")
        rprint("[muted]Ready for geological data analysis.[/]")

        return app.exec()

    except ImportError as e:
        rprint(f"[error]GUI dependencies not available:[/] {e}")
        rprint("[muted]Please install PyQt6: pip install PyQt6[/]")
    except Exception as e:
        rprint(f"[error]Error launching GUI:[/] {e}")
        rprint("[muted]Falling back to command line interface...[/]")


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
    if mapping_path:
        mapping = importer.load_mapping_yaml(mapping_path)
        if verbose:
            show_status(f"Loaded mapping from {mapping_path}", "INFO", f"{len(mapping)} fields")
        return mapping

    if not infer:
        return {}

    suggestions = importer.suggest_mapping(list(df.columns), threshold=threshold)

    proposed: Dict[str, str] = {}
    low_conf_required: List[str] = []
    missing_required: List[str] = []
    required_fields = ("sample_id", "sample_type", "result")

    # Print a rich mapping review table
    if verbose and RICH_AVAILABLE:
        table = Table(
            title="Column Mapping Suggestions",
            title_style="primary",
            border_style="#334155",
            box=box.SIMPLE_HEAD,
            show_header=True,
            header_style="heading",
        )
        table.add_column("Canonical Field", style="heading", min_width=16)
        table.add_column("Mapped Header", min_width=20)
        table.add_column("Confidence", justify="right", min_width=12)
        table.add_column("Status", justify="center", min_width=10)

        for canonical, (header, score) in suggestions.items():
            is_required = canonical in required_fields
            needs_review = is_required and (header is None or score < threshold)

            header_str = str(header) if header else "[muted]--[/]"
            conf_style = "pass_status" if score >= threshold else ("warn_status" if score >= 0.5 else "fail_status")
            conf_str = f"[{conf_style}]{score:.0%}[/]"
            status = "[fail_status]REVIEW[/]" if needs_review else ("[pass_status]OK[/]" if score >= threshold else "[muted]low[/]")

            table.add_row(canonical, header_str, conf_str, status)

        console.print(table)

    elif verbose:
        print("Suggested column mapping (confidence):")
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

    if (missing_required or low_conf_required) and not auto_accept:
        rprint("\n[warning]Mapping requires review:[/]")
        if missing_required:
            rprint(f"  [error]Missing required fields:[/] {', '.join(missing_required)}")
        if low_conf_required:
            rprint(f"  [warning]Low-confidence required fields:[/] {', '.join(low_conf_required)}")
        rprint("\n[muted]Re-run with either:[/]")
        rprint("  [primary]--mapping path/to/mapping.yaml[/]   (to provide explicit mapping)")
        rprint("  [primary]--infer-mapping --yes[/]            (to auto-accept suggestions)")
        sys.exit(2)

    if verbose and auto_accept:
        show_status("Auto-accepted inferred mapping", "PASS", f"{len(proposed)} fields mapped")

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
        "appVersion": "2.0.0",
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
        if RICH_AVAILABLE:
            console.print_json(json.dumps(provenance))
        else:
            print(json.dumps(provenance, indent=2))
    else:
        with open(prov_path, "w", encoding="utf-8") as f:
            json.dump(provenance, f, indent=2)


def process_data(args) -> None:
    """Process QAQC data with comprehensive analysis and reporting."""
    verbose = bool(args.verbose)
    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    config = load_config(args.config)
    default_dl = None
    try:
        default_dl = config.get("data", {}).get("cleaning", {}).get("default_detection_limit")
    except Exception:
        default_dl = None

    importer = DataImporter()
    crm_manager = CRMManager(args.crm_database) if args.crm_database else CRMManager()
    standards_analyzer = StandardsAnalyzer()
    blanks_analyzer = BlanksAnalyzer()
    duplicates_analyzer = DuplicatesAnalyzer()
    plot_generator = PlotGenerator()
    excel_reporter = ExcelReporter()
    pdf_reporter = PDFReporter()

    rprint(f"  [muted]Input:[/]  [heading]{input_path}[/]")
    rprint(f"  [muted]Output:[/] [heading]{output_dir}[/]")
    if args.dry_run:
        rprint("  [warning]DRY RUN -- no files will be written[/]\n")

    # Load data
    sheet = args.sheet if args.sheet is not None else (args.sheet_index if args.sheet_index is not None else 0)
    read_kwargs = dict(
        csv_delimiter=args.csv_delimiter,
        encoding=args.encoding,
        sheet_name=sheet,
        csv_chunksize=args.csv_chunksize,
        detect_encoding_fallback=bool(args.detect_encoding_fallback),
    )

    progress = create_progress()
    if progress:
        with progress:
            task = progress.add_task("Loading data...", total=100)
            frames = _load_frames(importer, input_path, read_kwargs)
            progress.update(task, completed=100)
    else:
        frames = _load_frames(importer, input_path, read_kwargs)

    # Process each file
    all_analysis_results = []
    all_plots = {}

    for item in frames:
        df = item.dataframe
        src = Path(item.source_path)
        df_before_cols = list(df.columns)
        df_before_rows = len(df)

        show_status(f"Processing {src.name}", "INFO", f"{df_before_rows:,} rows x {len(df_before_cols)} cols")

        mapping_source = "none"
        mapping = _review_and_build_mapping(
            importer, df,
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
            if args.save_mapping:
                try:
                    importer.save_mapping_yaml(mapping, args.save_mapping)
                    if verbose:
                        show_status(f"Saved mapping to {args.save_mapping}", "INFO")
                except Exception as e:
                    show_status(f"Failed to save mapping: {e}", "WARN")

        required = ("sample_id", "sample_type", "result")
        missing = importer.validate_required({k: k if k in df.columns else None for k in required})
        if missing:
            rprint(f"[error]Error:[/] missing required columns after mapping: {missing}")
            rprint(f"[muted]Available columns:[/] {', '.join(df.columns)}")
            sys.exit(2)

        used_per_row_dl = False
        if args.normalize_results:
            used_per_row_dl = "detection_limit" in df.columns
            df = importer.normalize_results(
                df, result_col="result", qualifier_col="qualifier",
                dl_col="detection_limit", default_dl=default_dl,
            )
            if verbose:
                show_status("Normalized results", "PASS", "Qualifiers and DL processed")

        rprint("  [muted]Running QAQC analysis...[/]")
        analysis_results = perform_qaqc_analysis(
            df, crm_manager, standards_analyzer, blanks_analyzer,
            duplicates_analyzer, args, verbose
        )

        if args.include_plots:
            plots = generate_plots(df, analysis_results, plot_generator, args, verbose)
            all_plots.update(plots)

        all_analysis_results.append({'file': src.name, 'results': analysis_results, 'data': df})

        out_name = f"{src.stem}_clean.csv"
        out_path = output_dir / out_name
        if not args.dry_run:
            df.to_csv(out_path, index=False)
            if verbose:
                show_status(f"Wrote cleaned data: {out_path}", "INFO")

        _write_provenance(
            out_path=out_path, src=src,
            df_before_cols=df_before_cols, df_before_rows=df_before_rows,
            df_after=df, mapping_used=mapping, mapping_source=mapping_source,
            confidence_threshold=0.85, normalize_enabled=bool(args.normalize_results),
            default_dl=default_dl, used_per_row_dl=used_per_row_dl,
            csv_delimiter=args.csv_delimiter, encoding=args.encoding,
            sheet_name=sheet, dry_run=bool(args.dry_run),
        )

    if all_analysis_results and not args.dry_run:
        generate_reports(all_analysis_results, all_plots, excel_reporter, pdf_reporter,
                        output_dir, args, verbose)

    if all_analysis_results:
        combined = all_analysis_results[-1]['results']
        show_summary_table(combined, output_dir)

    rprint("[success]Analysis complete![/]")
    rprint(f"[muted]Results saved to:[/] [heading]{output_dir}[/]\n")


def _load_frames(importer, input_path, read_kwargs):
    """Load data frames from file or directory."""
    if input_path.is_dir():
        return importer.read_from_directory(input_path, **read_kwargs)
    else:
        return [
            type("_tmp", (), {
                "dataframe": importer.read_table(input_path, **read_kwargs),
                "source_path": input_path,
            })()
        ]


def perform_qaqc_analysis(df, crm_manager, standards_analyzer, blanks_analyzer,
                         duplicates_analyzer, args, verbose):
    """Perform comprehensive QAQC analysis on the dataset."""
    analysis_results = {}

    if not args.skip_standards:
        standards_data = prepare_standards_data(df, crm_manager, args, verbose)
        if standards_data:
            analysis_results['standards'] = standards_analyzer.analyze_standards(standards_data)
            passed = analysis_results['standards']['overall_acceptable']
            show_status("Standards Analysis", "PASS" if passed else "FAIL")
        else:
            show_status("Standards Analysis", "SKIP", "No standards data available")
    else:
        show_status("Standards Analysis", "SKIP", "Skipped by user")

    if not args.skip_blanks:
        blanks_data = prepare_blanks_data(df, verbose)
        if blanks_data:
            analysis_results['blanks'] = blanks_analyzer.analyze_blanks(blanks_data)
            passed = analysis_results['blanks']['overall_acceptable']
            show_status("Blanks Analysis", "PASS" if passed else "FAIL")
        else:
            show_status("Blanks Analysis", "SKIP", "No blanks data available")
    else:
        show_status("Blanks Analysis", "SKIP", "Skipped by user")

    if not args.skip_duplicates:
        duplicates_data = prepare_duplicates_data(df, verbose)
        if duplicates_data:
            analysis_results['duplicates'] = duplicates_analyzer.analyze_duplicates(duplicates_data)
            passed = analysis_results['duplicates']['overall_acceptable']
            show_status("Duplicates Analysis", "PASS" if passed else "FAIL")
        else:
            show_status("Duplicates Analysis", "SKIP", "No duplicate pairs found")
    else:
        show_status("Duplicates Analysis", "SKIP", "Skipped by user")

    analysis_results['total_samples'] = len(df)
    analysis_results['analysis_date'] = _dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return analysis_results


def prepare_standards_data(df, crm_manager, args, verbose):
    """Prepare data for standards analysis."""
    standards_df = df[df['sample_type'].str.upper() == 'STANDARD'].copy()
    if len(standards_df) == 0:
        return None

    standards_df['result'] = pd.to_numeric(standards_df['result'], errors='coerce')

    crm_name = None
    if args.crm_name:
        crm_name = args.crm_name
    elif args.auto_crm:
        mean_conc = standards_df['result'].mean()
        crm_name = select_appropriate_crm(crm_manager, mean_conc, verbose)

    if not crm_name:
        if verbose:
            show_status("No CRM specified for standards", "WARN")
        return None

    is_valid, message = crm_manager.validate_crm_selection(crm_name, standards_df['result'].mean())
    if not is_valid:
        if verbose:
            show_status(f"CRM validation failed: {message}", "WARN")
        return None

    crm_info = crm_manager.get_crm_info(crm_name)
    if not crm_info:
        if verbose:
            show_status(f"CRM '{crm_name}' not found in database", "FAIL")
        return None

    if verbose:
        show_status(f"Using CRM: {crm_name}", "INFO", f"{crm_info['certified_value']} +/- {crm_info['uncertainty']} g/t")

    return {
        'measured': standards_df['result'].tolist(),
        'certified': crm_info['certified_value'],
        'uncertainty': crm_info['uncertainty']
    }


def select_appropriate_crm(crm_manager, concentration, verbose):
    """Select appropriate CRM based on concentration."""
    min_conc = concentration * 0.5
    max_conc = concentration * 2.0

    suitable_crms = crm_manager.get_crms_by_concentration_range(min_conc, max_conc)
    if not suitable_crms:
        if verbose:
            show_status(f"No suitable CRMs for concentration {concentration:.2f} g/t", "WARN")
        return None

    best_crm = min(suitable_crms, key=lambda x: abs(x['certified_value'] - concentration))
    if verbose:
        show_status(f"Auto-selected CRM: {best_crm['name']}", "INFO", f"{best_crm['certified_value']} g/t")

    return best_crm['name']


def prepare_blanks_data(df, verbose):
    """Prepare data for blanks analysis."""
    blanks_df = df[df['sample_type'].str.upper() == 'BLANK'].copy()
    if len(blanks_df) == 0:
        return None

    blanks_df['result'] = pd.to_numeric(blanks_df['result'], errors='coerce')
    all_samples = df.sort_values('sample_id') if 'sample_id' in df.columns else df
    previous_samples = all_samples[all_samples.index < blanks_df.index.min()]['result'].tolist()

    return {'blanks': blanks_df['result'].tolist(), 'previous_samples': previous_samples}


def prepare_duplicates_data(df, verbose):
    """Prepare data for duplicates analysis."""
    if 'sample_id' not in df.columns:
        return None

    df = df.copy()
    df['result'] = pd.to_numeric(df['result'], errors='coerce')

    duplicates = []
    for sample_id in df['sample_id'].unique():
        sample_data = df[df['sample_id'] == sample_id]
        if len(sample_data) == 2:
            values = sample_data['result'].tolist()
            duplicates.append(values)

    if not duplicates:
        return None
    return {'duplicates': duplicates}


def generate_plots(df, analysis_results, plot_generator, args, verbose):
    """Generate visualization plots."""
    plots = {}
    show_status("Generating plots...", "INFO")

    df = df.copy()
    df['result'] = pd.to_numeric(df['result'], errors='coerce')

    if 'standards' in analysis_results:
        standards_df = df[df['sample_type'].str.upper() == 'STANDARD']
        if len(standards_df) > 0:
            plots['standards_control'] = plot_generator.create_control_chart(
                standards_df['result'].tolist(), title="Standards Control Chart"
            )

    if 'duplicates' in analysis_results:
        duplicates_data = prepare_duplicates_data(df, False)
        if duplicates_data and duplicates_data['duplicates']:
            x_data = [pair[0] for pair in duplicates_data['duplicates']]
            y_data = [pair[1] for pair in duplicates_data['duplicates']]
            plots['duplicates_scatter'] = plot_generator.create_scatter_plot(
                x_data, y_data, "Duplicates Scatter Plot"
            )

    if len(df) > 0:
        plots['results_histogram'] = plot_generator.create_histogram(
            df['result'].tolist(), title="Results Distribution"
        )

    show_status(f"Generated {len(plots)} plots", "PASS")
    return plots


def generate_reports(all_analysis_results, all_plots, excel_reporter, pdf_reporter,
                    output_dir, args, verbose):
    """Generate comprehensive reports."""
    rprint("\n  [muted]Generating reports...[/]")

    combined_results = {
        'standards': {}, 'blanks': {}, 'duplicates': {},
        'total_samples': 0,
        'analysis_date': _dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    for file_result in all_analysis_results:
        results = file_result['results']
        combined_results['total_samples'] += results.get('total_samples', 0)
        for analysis_type in ['standards', 'blanks', 'duplicates']:
            if analysis_type in results:
                combined_results[analysis_type] = results[analysis_type]

    if args.output_format in ['excel', 'both']:
        excel_filename = output_dir / f"qaqc_report_{_dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        excel_reporter.generate_excel_report(combined_results, filename=str(excel_filename))
        show_status(f"Excel report: {excel_filename.name}", "PASS")

    if args.output_format in ['pdf', 'both']:
        pdf_filename = output_dir / f"qaqc_report_{_dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_reporter.generate_pdf_report(combined_results, all_plots, filename=str(pdf_filename))
        show_status(f"PDF report: {pdf_filename.name}", "PASS")

    if all_plots and args.include_plots:
        from src.visualization import PlotGenerator
        pg = PlotGenerator()
        plots_dir = output_dir / "plots"
        plots_dir.mkdir(exist_ok=True)
        for plot_name, plot_data in all_plots.items():
            plot_filename = plots_dir / f"{plot_name}.{args.plot_format}"
            pg.save_plot(plot_data, str(plot_filename), args.plot_format)
        show_status(f"Saved {len(all_plots)} plots to plots/", "PASS")


if __name__ == "__main__":
    main()
