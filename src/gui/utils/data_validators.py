"""
Data Validation Utilities

This module provides data validation functions for the QAQC Analysis Application GUI.
"""

from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
import numpy as np


class DataValidators:
    """Data validation utilities for GUI operations."""

    @staticmethod
    def validate_csv_file(file_path: str) -> Tuple[bool, str]:
        """Validate CSV file format and content."""
        try:
            # Try to read the file
            df = pd.read_csv(file_path, nrows=5)  # Read first 5 rows for validation

            if df.empty:
                return False, "File is empty"

            # Check for required columns (case insensitive)
            required_columns = ['sample_id', 'sample_type', 'result']
            df_columns_lower = [col.lower() for col in df.columns]

            missing_columns = []
            for req_col in required_columns:
                if req_col not in df_columns_lower:
                    missing_columns.append(req_col)

            if missing_columns:
                return False, f"Missing required columns: {', '.join(missing_columns)}"

            # Check data types
            if 'result' in df.columns:
                try:
                    pd.to_numeric(df['result'], errors='coerce')
                except:
                    return False, "Result column contains non-numeric data"

            return True, "File is valid"

        except Exception as e:
            return False, f"Error reading file: {str(e)}"

    @staticmethod
    def validate_excel_file(file_path: str) -> Tuple[bool, str]:
        """Validate Excel file format and content."""
        try:
            # Try to read the file
            df = pd.read_excel(file_path, nrows=5)  # Read first 5 rows for validation

            if df.empty:
                return False, "File is empty"

            # Check for required columns (case insensitive)
            required_columns = ['sample_id', 'sample_type', 'result']
            df_columns_lower = [col.lower() for col in df.columns]

            missing_columns = []
            for req_col in required_columns:
                if req_col not in df_columns_lower:
                    missing_columns.append(req_col)

            if missing_columns:
                return False, f"Missing required columns: {', '.join(missing_columns)}"

            # Check data types
            if 'result' in df.columns:
                try:
                    pd.to_numeric(df['result'], errors='coerce')
                except:
                    return False, "Result column contains non-numeric data"

            return True, "File is valid"

        except Exception as e:
            return False, f"Error reading file: {str(e)}"

    @staticmethod
    def validate_data_quality(data: pd.DataFrame) -> Dict[str, Any]:
        """Validate data quality and return statistics."""
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }

        try:
            # Check for missing values
            missing_counts = data.isnull().sum()
            if missing_counts.any():
                validation_results['warnings'].append(f"Missing values found in columns: {missing_counts[missing_counts > 0].to_dict()}")

            # Check for duplicate sample IDs
            if 'sample_id' in data.columns:
                duplicates = data['sample_id'].duplicated().sum()
                if duplicates > 0:
                    validation_results['warnings'].append(f"Found {duplicates} duplicate sample IDs")

            # Check sample types
            if 'sample_type' in data.columns:
                valid_types = ['STANDARD', 'BLANK', 'DUPLICATE', 'SAMPLE']
                invalid_types = data[~data['sample_type'].isin(valid_types)]['sample_type'].unique()
                if len(invalid_types) > 0:
                    validation_results['warnings'].append(f"Invalid sample types found: {list(invalid_types)}")

            # Check result values
            if 'result' in data.columns:
                numeric_results = pd.to_numeric(data['result'], errors='coerce')
                non_numeric_count = numeric_results.isnull().sum()
                if non_numeric_count > 0:
                    validation_results['warnings'].append(f"Found {non_numeric_count} non-numeric result values")

                # Check for negative values
                negative_count = (numeric_results < 0).sum()
                if negative_count > 0:
                    validation_results['warnings'].append(f"Found {negative_count} negative result values")

            # Calculate statistics
            validation_results['statistics'] = {
                'total_samples': len(data),
                'standards_count': len(data[data['sample_type'] == 'STANDARD']) if 'sample_type' in data.columns else 0,
                'blanks_count': len(data[data['sample_type'] == 'BLANK']) if 'sample_type' in data.columns else 0,
                'duplicates_count': len(data[data['sample_type'] == 'DUPLICATE']) if 'sample_type' in data.columns else 0,
                'samples_count': len(data[data['sample_type'] == 'SAMPLE']) if 'sample_type' in data.columns else 0,
                'columns_count': len(data.columns)
            }

        except Exception as e:
            validation_results['is_valid'] = False
            validation_results['errors'].append(f"Validation error: {str(e)}")

        return validation_results

    @staticmethod
    def validate_column_mapping(mapping: Dict[str, str], available_columns: List[str]) -> Tuple[bool, List[str]]:
        """Validate column mapping configuration."""
        errors = []

        # Check if all required fields are mapped
        required_fields = ['sample_id', 'sample_type', 'result']
        for field in required_fields:
            if field not in mapping:
                errors.append(f"Required field '{field}' is not mapped")

        # Check if mapped columns exist
        for field, mapped_column in mapping.items():
            if mapped_column and mapped_column not in available_columns:
                errors.append(f"Mapped column '{mapped_column}' for field '{field}' does not exist")

        return len(errors) == 0, errors

    @staticmethod
    def validate_analysis_configuration(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate analysis configuration."""
        errors = []

        # Check if at least one analysis type is enabled
        analysis_types = ['standards_enabled', 'blanks_enabled', 'duplicates_enabled']
        if not any(config.get(analysis_type, False) for analysis_type in analysis_types):
            errors.append("At least one analysis type must be enabled")

        # Validate thresholds
        if config.get('z_score_threshold', 0) <= 0:
            errors.append("Z-score threshold must be positive")

        if config.get('rpd_threshold', 0) <= 0:
            errors.append("RPD threshold must be positive")

        # Validate recovery limits
        recovery_limits = config.get('recovery_limits', [])
        if len(recovery_limits) == 2:
            if recovery_limits[0] >= recovery_limits[1]:
                errors.append("Minimum recovery must be less than maximum recovery")

        return len(errors) == 0, errors

    @staticmethod
    def validate_crm_selection(crm_name: str, data_mean: float) -> Tuple[bool, str]:
        """Validate CRM selection based on data characteristics."""
        if not crm_name or crm_name == "Auto-Select CRM":
            return True, "CRM will be auto-selected"

        # Define CRM concentration ranges
        crm_ranges = {
            "NIST SRM 2709a": (0.5, 1.5),
            "NIST SRM 2704": (10.0, 20.0),
            "CANMET OREAS 101": (0.05, 0.25)
        }

        for crm, (min_conc, max_conc) in crm_ranges.items():
            if crm in crm_name:
                if min_conc <= data_mean <= max_conc:
                    return True, f"CRM {crm} is appropriate for data mean {data_mean:.3f} g/t"
                else:
                    return False, f"CRM {crm} may not be appropriate for data mean {data_mean:.3f} g/t (expected range: {min_conc}-{max_conc} g/t)"

        return True, "CRM validation not available"
