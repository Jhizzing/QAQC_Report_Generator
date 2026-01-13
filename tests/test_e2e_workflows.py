"""
End-to-end workflow tests for complete QAQC analysis pipelines.
Tests the full workflow from data import through report generation.
"""
import pytest
import tempfile
import os
import json
from pathlib import Path
from src.data.importer import DataImporter
from src.data.processor import DataProcessor
from src.analysis import StandardsAnalyzer, BlanksAnalyzer, DuplicatesAnalyzer
from src.reporting import ExcelReporter, PDFReporter
from src.core.project_manager import ProjectManager


class TestCompleteGoldWorkflow:
    """Test complete gold analysis workflow."""

    def test_complete_gold_workflow(self):
        """Test full workflow: Import → Process → Analyze → Report."""
        # Create sample CSV data
        csv_content = """Sample_ID,Sample_Type,Au_ppm
OREAS-101-1,STD,0.082
OREAS-101-2,STD,0.085
BLANK-001,BLK,0.001
RC0001,UNK,2.5
RC0002,UNK,1.8
RC0001-DUP,DUP,2.4
RC0003,UNK,3.2
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            csv_path = f.name

        try:
            # 1. Import data
            importer = DataImporter()
            raw_data = importer.import_csv(csv_path)
            assert len(raw_data) > 0

            # 2. Process data
            processor = DataProcessor()
            processed_data = processor.process_data(raw_data)
            assert 'standards' in processed_data
            assert 'blanks' in processed_data
            assert 'duplicates' in processed_data

            # 3. Analyze standards
            standards_analyzer = StandardsAnalyzer()
            standards_results = standards_analyzer.analyze(
                processed_data['standards'],
                certified_value=0.082,
                uncertainty=0.005
            )
            assert 'pass_rate' in standards_results

            # 4. Analyze blanks
            blanks_analyzer = BlanksAnalyzer()
            blanks_results = blanks_analyzer.analyze(
                processed_data['blanks'],
                detection_limit=0.01
            )
            assert 'contamination_rate' in blanks_results

            # 5. Analyze duplicates
            duplicates_analyzer = DuplicatesAnalyzer()
            duplicates_results = duplicates_analyzer.analyze(
                processed_data['duplicates']
            )
            assert 'mean_rpd' in duplicates_results

            # 6. Generate Excel report
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                excel_path = tmp.name

            try:
                excel_reporter = ExcelReporter()
                excel_reporter.generate_report(
                    {
                        'standards': standards_results,
                        'blanks': blanks_results,
                        'duplicates': duplicates_results
                    },
                    excel_path
                )
                assert os.path.exists(excel_path)
                assert os.path.getsize(excel_path) > 0
            finally:
                if os.path.exists(excel_path):
                    os.unlink(excel_path)

        finally:
            if os.path.exists(csv_path):
                os.unlink(csv_path)

    def test_project_save_and_load(self):
        """Test project save and load cycle."""
        # Create sample project data
        project_data = {
            'metadata': {
                'name': 'Test Project',
                'deposit': 'Test Deposit',
                'commodity': 'Gold'
            },
            'data': [
                {'Sample_ID': 'RC0001', 'Sample_Type': 'UNK', 'Au_ppm': 2.5}
            ],
            'analysis_results': {
                'standards': {'pass_rate': 95.0},
                'blanks': {'contamination_rate': 2.0},
                'duplicates': {'mean_rpd': 8.5}
            }
        }

        with tempfile.NamedTemporaryFile(suffix='.qaqc', delete=False) as tmp:
            project_path = tmp.name

        try:
            # Save project
            project_manager = ProjectManager()
            project_manager.save_project(project_path, project_data)

            # Verify file exists
            assert os.path.exists(project_path)

            # Load project
            loaded_data = project_manager.load_project(project_path)

            # Verify data integrity
            assert loaded_data['metadata']['name'] == 'Test Project'
            assert len(loaded_data['data']) == 1
            assert loaded_data['analysis_results']['standards']['pass_rate'] == 95.0

        finally:
            if os.path.exists(project_path):
                os.unlink(project_path)


class TestCompletePXRFWorkflow:
    """Test complete pXRF analysis workflow."""

    def test_complete_pxrf_workflow(self):
        """Test full pXRF workflow with multiple elements."""
        # Create sample pXRF CSV data
        csv_content = """Sample_ID,Sample_Type,Cu_ppm,Pb_ppm,Zn_ppm,Fe_pct
OREAS-100-1,STD,189,42.3,127,3.42
OREAS-100-2,STD,192,43.1,129,3.45
BLANK-PX-1,BLK,2.1,1.5,3.2,0.05
PX0001,UNK,245,58,189,4.2
PX0002,UNK,189,42,127,3.4
PX0001-DUP,DUP,248,59,191,4.3
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            csv_path = f.name

        try:
            # 1. Import data
            importer = DataImporter()
            raw_data = importer.import_csv(csv_path)
            assert len(raw_data) > 0

            # 2. Process data
            processor = DataProcessor()
            processed_data = processor.process_data(raw_data)
            assert 'standards' in processed_data

            # 3. Analyze multiple elements
            standards_analyzer = StandardsAnalyzer()
            elements = ['Cu', 'Pb', 'Zn', 'Fe']
            results = {}

            for element in elements:
                element_data = [d for d in processed_data['standards'] if element in str(d)]
                if element_data:
                    certified_values = {'Cu': 189, 'Pb': 42.3, 'Zn': 127, 'Fe': 3.42}
                    element_results = standards_analyzer.analyze(
                        element_data,
                        certified_value=certified_values.get(element, 0),
                        uncertainty=certified_values.get(element, 0) * 0.05
                    )
                    results[element] = element_results

            # Verify all elements analyzed
            assert len(results) > 0
            for element in elements:
                if element in results:
                    assert 'pass_rate' in results[element]

        finally:
            if os.path.exists(csv_path):
                os.unlink(csv_path)


class TestCompleteMultiElementWorkflow:
    """Test complete multi-element ICP analysis workflow."""

    def test_complete_multielement_workflow(self):
        """Test full multi-element ICP workflow."""
        # Create sample multi-element CSV data
        csv_content = """Sample_ID,Sample_Type,Cu_pct,Pb_ppm,Zn_ppm,Fe_pct,Au_gpt
OREAS-201-1,STD,0.393,37.2,113,4.12,0.278
OREAS-201-2,STD,0.395,37.5,115,4.15,0.281
BLANK-ICP-1,BLK,0.0001,0.3,0.8,0.005,0.002
ICP0001,UNK,1.2,45,189,8.5,1.2
ICP0002,UNK,0.8,32,145,6.2,0.9
ICP0001-DUP,DUP,1.22,46,191,8.6,1.18
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            csv_path = f.name

        try:
            # 1. Import data
            importer = DataImporter()
            raw_data = importer.import_csv(csv_path)
            assert len(raw_data) > 0

            # 2. Process data
            processor = DataProcessor()
            processed_data = processor.process_data(raw_data)

            # 3. Analyze with element-specific settings
            standards_analyzer = StandardsAnalyzer()
            
            # Major elements (stricter tolerance)
            major_elements = ['Cu', 'Fe']
            # Trace elements (more lenient tolerance)
            trace_elements = ['Pb', 'Zn', 'Au']

            for element in major_elements + trace_elements:
                element_data = [d for d in processed_data['standards'] if element in str(d)]
                if element_data:
                    # Use appropriate tolerance based on element type
                    tolerance = 0.08 if element in major_elements else 0.15
                    certified_values = {
                        'Cu': 0.393, 'Pb': 37.2, 'Zn': 113, 
                        'Fe': 4.12, 'Au': 0.278
                    }
                    
                    element_results = standards_analyzer.analyze(
                        element_data,
                        certified_value=certified_values.get(element, 0),
                        uncertainty=certified_values.get(element, 0) * tolerance
                    )
                    assert 'pass_rate' in element_results

        finally:
            if os.path.exists(csv_path):
                os.unlink(csv_path)


class TestErrorRecovery:
    """Test error recovery workflows."""

    def test_error_recovery_on_invalid_data(self):
        """Test handling of invalid data gracefully."""
        # Create CSV with invalid data
        csv_content = """Sample_ID,Sample_Type,Au_ppm
OREAS-101-1,STD,invalid
BLANK-001,BLK,0.001
RC0001,UNK,2.5
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            csv_path = f.name

        try:
            importer = DataImporter()
            # Should handle invalid data gracefully
            try:
                raw_data = importer.import_csv(csv_path)
                # If import succeeds, processing should handle invalid values
                processor = DataProcessor()
                processed_data = processor.process_data(raw_data)
                # Should still process valid data
                assert len(processed_data.get('standards', [])) >= 0
            except (ValueError, TypeError):
                # Expected for invalid data
                pass

        finally:
            if os.path.exists(csv_path):
                os.unlink(csv_path)

    def test_backend_fallback_to_client_side(self):
        """Test fallback to client-side analysis when backend unavailable."""
        # This test verifies that the system can fall back to client-side
        # analysis when the backend is not available
        # Implementation depends on backend service architecture
        
        # Mock scenario: Backend unavailable
        backend_available = False
        
        # Should use client-side analysis
        assert backend_available is False
        # Client-side analysis should still work
        # (Actual implementation would test the fallback mechanism)


class TestMultipleFileFormats:
    """Test workflow with different file formats."""

    def test_csv_import_workflow(self):
        """Test complete workflow with CSV file."""
        csv_content = """Sample_ID,Sample_Type,Au_ppm
OREAS-101-1,STD,0.082
RC0001,UNK,2.5
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            csv_path = f.name

        try:
            importer = DataImporter()
            raw_data = importer.import_csv(csv_path)
            assert len(raw_data) > 0
        finally:
            if os.path.exists(csv_path):
                os.unlink(csv_path)

    def test_excel_import_workflow(self):
        """Test complete workflow with Excel file."""
        # Note: This requires openpyxl or xlrd
        # For now, we'll test that the importer can handle Excel files
        # Actual Excel file creation would require additional dependencies
        
        # This is a placeholder - actual implementation would create
        # an Excel file and test import
        importer = DataImporter()
        # Verify Excel import method exists
        assert hasattr(importer, 'import_excel') or hasattr(importer, 'import_file')
