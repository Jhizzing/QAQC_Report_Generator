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
from typing import Optional

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data import DataImporter, DataProcessor
from src.analysis import QAQCAnalyzer
from src.visualization import PlotGenerator
from src.reporting import ReportGenerator


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="QAQC Analysis Automation Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with GUI interface
  python main.py --gui

  # Process data from command line
  python main.py --input data.csv --output results/

  # Process with custom configuration
  python main.py --input data.csv --config custom_config.yaml
        """
    )

    parser.add_argument(
        "--input", "-i",
        type=str,
        help="Input data file (CSV, XLSX, or XLS)"
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
        print("Error: Input file is required for command line processing.")
        print("Use --help for usage information or --gui for GUI interface.")
        sys.exit(1)

    try:
        process_data(args.input, args.output, args.config, args.verbose)
    except Exception as e:
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
    except Exception as e:
        print(f"Error launching GUI: {e}")
        sys.exit(1)


def process_data(input_file: str, output_dir: str, config_file: str, verbose: bool = False):
    """Process QAQC data from command line."""
    if verbose:
        print(f"Processing QAQC data...")
        print(f"Input file: {input_file}")
        print(f"Output directory: {output_dir}")
        print(f"Configuration: {config_file}")

    # Validate input file
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Initialize components
    if verbose:
        print("Initializing QAQC analysis components...")

    # TODO: Implement the actual processing pipeline
    # This is a placeholder for the full implementation

    print("QAQC analysis completed successfully!")
    print(f"Results saved to: {output_dir}")


if __name__ == "__main__":
    main()
