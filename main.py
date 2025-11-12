#!/usr/bin/env python3
"""
QAQC Analysis Automation Application - Main Entry Point

This is the main entry point for the QAQC Analysis Automation application.
It provides comprehensive QAQC analysis including standards, blanks, duplicates,
and CRM integration with professional reporting capabilities.
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
        description="QAQC Analysis Automation Application",
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

    # CRM and Analysis options
    parser.add_argument(
        "--crm-database",
        type=str,
        help="Path to CRM database YAML file (default: crm_database.yaml)"
    )
    parser.add_argument(
        "--crm-name",
        type=str,
        help="Specific CRM to use for standards analysis (e.g., 'NIST SRM 2709a')"
    )
    parser.add_argument(
        "--auto-crm",
        action="store_true",
        help="Automatically select appropriate CRM based on sample concentrations"
    )
    parser.add_argument(
        "--skip-standards",
        action="store_true",
        help="Skip standards analysis"
    )
    parser.add_argument(
        "--skip-blanks",
        action="store_true",
        help="Skip blanks analysis"
    )
    parser.add_argument(
        "--skip-duplicates",
        action="store_true",
        help="Skip duplicates analysis"
    )

    # Output format options
    parser.add_argument(
        "--output-format",
        choices=["excel", "pdf", "both"],
        default="both",
        help="Output format: excel, pdf, or both (default: both)"
    )
    parser.add_argument(
        "--include-plots",
        action="store_true",
        help="Generate visualization plots"
    )
    parser.add_argument(
        "--plot-format",
        choices=["png", "pdf", "svg"],
        default="png",
        help="Plot file format (default: png)"
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
        version="QAQC Analysis Automation v2.0.0"
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
        from PyQt6.QtWidgets import QApplication
        from src.gui.main_window import QAQCApplication

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("QAQC Analysis Application")
        app.setApplicationVersion("2.0.0")
        app.setOrganizationName("QAQC Analysis")

        # Create and show main window
        window = QAQCApplication()
        window.show()

        print("QAQC Analysis Application GUI launched!")
        print("Ready for geological data analysis.")

        # Run application
        return app.exec()

    except ImportError as e:
        print(f"GUI dependencies not available: {e}")
        print("Please install PyQt6: pip install PyQt6")
        print("Falling back to command line interface...")
        print("Use --help for command line options.")
    except Exception as e:
        print(f"Error launching GUI: {e}")
        print("Falling back to command line interface...")
        print("Use --help for command line options.")


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
    """Process QAQC data with comprehensive analysis and reporting."""
    verbose = bool(args.verbose)
    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load configuration
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

    # Initialize components
    importer = DataImporter()
    crm_manager = CRMManager(args.crm_database) if args.crm_database else CRMManager()

    # Initialize analyzers
    standards_analyzer = StandardsAnalyzer()
    blanks_analyzer = BlanksAnalyzer()
    duplicates_analyzer = DuplicatesAnalyzer()
    plot_generator = PlotGenerator()

    # Initialize reporters
    excel_reporter = ExcelReporter()
    pdf_reporter = PDFReporter()

    if verbose:
        print("QAQC Analysis Automation v2.0.0")
        print("=" * 50)

    # Load and process data
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

    # Process each file
    all_analysis_results = []
    all_plots = {}

    for item in frames:
        df = item.dataframe
        src = Path(item.source_path)
        df_before_cols = list(df.columns)
        df_before_rows = len(df)

        if verbose:
            print(f"\nProcessing: {src.name}")
            print(f"  Rows: {df_before_rows}, Columns: {len(df_before_cols)}")

        # Apply column mapping
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
            if args.save_mapping:
                try:
                    importer.save_mapping_yaml(mapping, args.save_mapping)
                    if verbose:
                        print(f"  Saved mapping to {args.save_mapping}")
                except Exception as e:
                    print(f"  Warning: failed to save mapping: {e}")

        # Validate required columns
        required = ("sample_id", "sample_type", "result")
        missing = importer.validate_required({k: k if k in df.columns else None for k in required})
        if missing:
            print(f"Error: missing required columns after mapping: {missing}")
            print("Available columns:", ", ".join(df.columns))
            sys.exit(2)

        # Normalize results if requested
        used_per_row_dl = False
        if args.normalize_results:
            used_per_row_dl = "detection_limit" in df.columns
            df = importer.normalize_results(
                df,
                result_col="result",
                qualifier_col="qualifier",
                dl_col="detection_limit",
                default_dl=default_dl,
            )

        # Perform QAQC analysis
        analysis_results = perform_qaqc_analysis(
            df, crm_manager, standards_analyzer, blanks_analyzer, duplicates_analyzer,
            args, verbose
        )

        # Generate plots if requested
        if args.include_plots:
            plots = generate_plots(df, analysis_results, plot_generator, args, verbose)
            all_plots.update(plots)

        # Store results
        all_analysis_results.append({
            'file': src.name,
            'results': analysis_results,
            'data': df
        })

        # Write cleaned CSV
        out_name = f"{src.stem}_clean.csv"
        out_path = output_dir / out_name
        if not args.dry_run:
            df.to_csv(out_path, index=False)
            if verbose:
                print(f"  Wrote cleaned data: {out_path}")

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

    # Generate comprehensive reports
    if all_analysis_results and not args.dry_run:
        generate_reports(all_analysis_results, all_plots, excel_reporter, pdf_reporter,
                        output_dir, args, verbose)

    if verbose:
        print(f"\nAnalysis complete! Results saved to: {output_dir}")


def perform_qaqc_analysis(df, crm_manager, standards_analyzer, blanks_analyzer,
                         duplicates_analyzer, args, verbose):
    """Perform comprehensive QAQC analysis on the dataset."""
    analysis_results = {}

    if verbose:
        print("  Performing QAQC analysis...")

    # Standards analysis
    if not args.skip_standards:
        standards_data = prepare_standards_data(df, crm_manager, args, verbose)
        if standards_data:
            analysis_results['standards'] = standards_analyzer.analyze_standards(standards_data)
            if verbose:
                status = "PASS" if analysis_results['standards']['overall_acceptable'] else "FAIL"
                print(f"    Standards Analysis: {status}")

    # Blanks analysis
    if not args.skip_blanks:
        blanks_data = prepare_blanks_data(df, verbose)
        if blanks_data:
            analysis_results['blanks'] = blanks_analyzer.analyze_blanks(blanks_data)
            if verbose:
                status = "PASS" if analysis_results['blanks']['overall_acceptable'] else "FAIL"
                print(f"    Blanks Analysis: {status}")

    # Duplicates analysis
    if not args.skip_duplicates:
        duplicates_data = prepare_duplicates_data(df, verbose)
        if duplicates_data:
            analysis_results['duplicates'] = duplicates_analyzer.analyze_duplicates(duplicates_data)
            if verbose:
                status = "PASS" if analysis_results['duplicates']['overall_acceptable'] else "FAIL"
                print(f"    Duplicates Analysis: {status}")

    # Add summary information
    analysis_results['total_samples'] = len(df)
    analysis_results['analysis_date'] = _dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return analysis_results


def prepare_standards_data(df, crm_manager, args, verbose):
    """Prepare data for standards analysis."""
    # Filter standards samples
    standards_df = df[df['sample_type'].str.upper() == 'STANDARD'].copy()
    if len(standards_df) == 0:
        if verbose:
            print("    No standards found in dataset")
        return None

    # Ensure result column is numeric
    standards_df['result'] = pd.to_numeric(standards_df['result'], errors='coerce')

    # Get CRM information
    crm_name = None
    if args.crm_name:
        crm_name = args.crm_name
    elif args.auto_crm:
        # Auto-select CRM based on concentration
        mean_conc = standards_df['result'].mean()
        crm_name = select_appropriate_crm(crm_manager, mean_conc, verbose)

    if not crm_name:
        if verbose:
            print("    No CRM specified for standards analysis")
        return None

    # Validate CRM selection
    is_valid, message = crm_manager.validate_crm_selection(crm_name, standards_df['result'].mean())
    if not is_valid:
        if verbose:
            print(f"    CRM validation failed: {message}")
        return None

    # Get CRM data
    crm_info = crm_manager.get_crm_info(crm_name)
    if not crm_info:
        if verbose:
            print(f"    CRM '{crm_name}' not found in database")
        return None

    if verbose:
        print(f"    Using CRM: {crm_name} ({crm_info['certified_value']} ± {crm_info['uncertainty']} g/t)")

    return {
        'measured': standards_df['result'].tolist(),
        'certified': crm_info['certified_value'],
        'uncertainty': crm_info['uncertainty']
    }


def select_appropriate_crm(crm_manager, concentration, verbose):
    """Select appropriate CRM based on concentration."""
    # Find CRMs within 50-200% of concentration
    min_conc = concentration * 0.5
    max_conc = concentration * 2.0

    suitable_crms = crm_manager.get_crms_by_concentration_range(min_conc, max_conc)
    if not suitable_crms:
        if verbose:
            print(f"    No suitable CRMs found for concentration {concentration:.2f} g/t")
        return None

    # Select the CRM closest to the concentration
    best_crm = min(suitable_crms, key=lambda x: abs(x['certified_value'] - concentration))
    if verbose:
        print(f"    Auto-selected CRM: {best_crm['name']} ({best_crm['certified_value']} g/t)")

    return best_crm['name']


def prepare_blanks_data(df, verbose):
    """Prepare data for blanks analysis."""
    blanks_df = df[df['sample_type'].str.upper() == 'BLANK'].copy()
    if len(blanks_df) == 0:
        if verbose:
            print("    No blanks found in dataset")
        return None

    # Ensure result column is numeric
    blanks_df['result'] = pd.to_numeric(blanks_df['result'], errors='coerce')

    # Get previous samples for carry-over analysis
    all_samples = df.sort_values('sample_id') if 'sample_id' in df.columns else df
    previous_samples = all_samples[all_samples.index < blanks_df.index.min()]['result'].tolist()

    return {
        'blanks': blanks_df['result'].tolist(),
        'previous_samples': previous_samples
    }


def prepare_duplicates_data(df, verbose):
    """Prepare data for duplicates analysis."""
    # Find duplicate pairs (same sample_id, different analysis)
    if 'sample_id' not in df.columns:
        if verbose:
            print("    No sample_id column for duplicates analysis")
        return None

    # Ensure result column is numeric
    df = df.copy()
    df['result'] = pd.to_numeric(df['result'], errors='coerce')

    duplicates = []
    for sample_id in df['sample_id'].unique():
        sample_data = df[df['sample_id'] == sample_id]
        if len(sample_data) == 2:
            values = sample_data['result'].tolist()
            duplicates.append(values)

    if not duplicates:
        if verbose:
            print("    No duplicate pairs found in dataset")
        return None

    return {'duplicates': duplicates}


def generate_plots(df, analysis_results, plot_generator, args, verbose):
    """Generate visualization plots."""
    plots = {}

    if verbose:
        print("  Generating plots...")

    # Ensure result column is numeric for plotting
    df = df.copy()
    df['result'] = pd.to_numeric(df['result'], errors='coerce')

    # Standards control chart
    if 'standards' in analysis_results:
        standards_df = df[df['sample_type'].str.upper() == 'STANDARD']
        if len(standards_df) > 0:
            plot_data = plot_generator.create_control_chart(
                standards_df['result'].tolist(),
                title="Standards Control Chart"
            )
            plots['standards_control'] = plot_data

    # Duplicates scatter plot
    if 'duplicates' in analysis_results:
        duplicates_data = prepare_duplicates_data(df, False)
        if duplicates_data and duplicates_data['duplicates']:
            x_data = [pair[0] for pair in duplicates_data['duplicates']]
            y_data = [pair[1] for pair in duplicates_data['duplicates']]
            plot_data = plot_generator.create_scatter_plot(
                x_data, y_data, "Duplicates Scatter Plot"
            )
            plots['duplicates_scatter'] = plot_data

    # Results histogram
    if len(df) > 0:
        plot_data = plot_generator.create_histogram(
            df['result'].tolist(),
            title="Results Distribution"
        )
        plots['results_histogram'] = plot_data

    return plots


def generate_reports(all_analysis_results, all_plots, excel_reporter, pdf_reporter,
                    output_dir, args, verbose):
    """Generate comprehensive reports."""
    if verbose:
        print("\nGenerating reports...")

    # Combine all analysis results
    combined_results = {
        'standards': {},
        'blanks': {},
        'duplicates': {},
        'total_samples': 0,
        'analysis_date': _dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Aggregate results from all files
    for file_result in all_analysis_results:
        results = file_result['results']
        combined_results['total_samples'] += results.get('total_samples', 0)

        # Merge analysis results (take the last one for now)
        for analysis_type in ['standards', 'blanks', 'duplicates']:
            if analysis_type in results:
                combined_results[analysis_type] = results[analysis_type]

    # Generate Excel report
    if args.output_format in ['excel', 'both']:
        excel_filename = output_dir / f"qaqc_report_{_dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        excel_reporter.generate_excel_report(combined_results, filename=str(excel_filename))
        if verbose:
            print(f"  Excel report: {excel_filename}")

    # Generate PDF report
    if args.output_format in ['pdf', 'both']:
        pdf_filename = output_dir / f"qaqc_report_{_dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_reporter.generate_pdf_report(combined_results, all_plots, filename=str(pdf_filename))
        if verbose:
            print(f"  PDF report: {pdf_filename}")

    # Save plots
    if all_plots and args.include_plots:
        from src.visualization import PlotGenerator
        plot_generator = PlotGenerator()

        plots_dir = output_dir / "plots"
        plots_dir.mkdir(exist_ok=True)

        for plot_name, plot_data in all_plots.items():
            plot_filename = plots_dir / f"{plot_name}.{args.plot_format}"
            plot_generator.save_plot(plot_data, str(plot_filename), args.plot_format)
            if verbose:
                print(f"  Plot: {plot_filename}")


if __name__ == "__main__":
    main()
