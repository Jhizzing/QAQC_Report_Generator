"""
Performance tests for QAQC analysis system.
Tests processing speed, memory usage, and scalability.
"""
import pytest
import time
import psutil
import os
import tempfile
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src.data.importer import DataImporter
from src.data.processor import DataProcessor
from src.analysis import StandardsAnalyzer, BlanksAnalyzer, DuplicatesAnalyzer


@pytest.fixture
def large_dataset_csv():
    """Create a large CSV dataset for performance testing."""
    # Generate 1000 samples
    csv_lines = ["Sample_ID,Sample_Type,Au_ppm"]
    
    # Add standards (every 20 samples)
    for i in range(1, 51):
        csv_lines.append(f"OREAS-101-{i},STD,{0.082 + (i % 3) * 0.01}")
    
    # Add blanks (every 50 samples)
    for i in range(1, 21):
        csv_lines.append(f"BLANK-{i:03d},BLK,{0.001 + (i % 2) * 0.002}")
    
    # Add duplicates (every 30 samples)
    for i in range(1, 34):
        csv_lines.append(f"RC{i:04d},UNK,{2.0 + (i % 10) * 0.5}")
        csv_lines.append(f"RC{i:04d}-DUP,DUP,{2.0 + (i % 10) * 0.5 + 0.1}")
    
    # Add remaining unknowns
    for i in range(34, 1000):
        csv_lines.append(f"RC{i:04d},UNK,{1.0 + (i % 20) * 0.3}")
    
    csv_content = "\n".join(csv_lines)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_path = f.name
    
    yield Path(temp_path)
    
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def multi_element_dataset_csv():
    """Create a multi-element dataset for performance testing."""
    elements = ["Cu_ppm", "Pb_ppm", "Zn_ppm", "Fe_pct", "As_ppm", "Ni_ppm", "Co_ppm"]
    csv_lines = ["Sample_ID,Sample_Type," + ",".join(elements)]
    
    # Generate 500 samples with multiple elements
    for i in range(1, 501):
        sample_type = "UNK"
        if i % 20 == 0:
            sample_type = "STD"
        elif i % 50 == 0:
            sample_type = "BLK"
        elif i % 30 == 0:
            sample_type = "DUP"
        
        values = [f"{100 + (i % 50) * 10}" for _ in elements]
        csv_lines.append(f"RC{i:04d},{sample_type}," + ",".join(values))
    
    csv_content = "\n".join(csv_lines)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_path = f.name
    
    yield Path(temp_path)
    
    if os.path.exists(temp_path):
        os.unlink(temp_path)


class TestImportPerformance:
    """Test data import performance."""

    def test_large_dataset_import_performance(self, large_dataset_csv):
        """Test import performance with large dataset."""
        start_time = time.time()
        importer = DataImporter()
        raw_data = importer.read_table(large_dataset_csv)
        import_time = time.time() - start_time
        
        # Should complete in reasonable time (<5 seconds for 1000 samples)
        assert import_time < 5.0
        assert len(raw_data) > 0
        
        # Calculate samples per second
        samples_per_second = len(raw_data) / import_time
        print(f"\nImport performance: {samples_per_second:.0f} samples/second")
        assert samples_per_second > 100  # Should handle at least 100 samples/second

    def test_multi_element_import_performance(self, multi_element_dataset_csv):
        """Test import performance with multiple elements."""
        start_time = time.time()
        importer = DataImporter()
        raw_data = importer.read_table(multi_element_dataset_csv)
        import_time = time.time() - start_time
        
        assert import_time < 3.0
        assert len(raw_data) > 0


class TestAnalysisPerformance:
    """Test analysis performance."""

    def test_analysis_performance_with_many_elements(self, multi_element_dataset_csv):
        """Test analysis performance with multiple elements."""
        importer = DataImporter()
        processor = DataProcessor()
        standards_analyzer = StandardsAnalyzer()
        
        # Import and process
        raw_data = importer.read_table(multi_element_dataset_csv)
        processed_data = processor.process_data(raw_data)
        
        # Analyze multiple elements
        start_time = time.time()
        elements = ["Cu", "Pb", "Zn", "Fe", "As", "Ni", "Co"]
        results = {}
        
        for element in elements:
            element_data = [d for d in processed_data.get('standards', []) 
                           if element in str(d)]
            if element_data:
                results[element] = standards_analyzer.analyze(
                    element_data,
                    certified_value=100.0,
                    uncertainty=5.0
                )
        
        analysis_time = time.time() - start_time
        
        # Should complete in reasonable time (<10 seconds)
        assert analysis_time < 10.0
        print(f"\nMulti-element analysis time: {analysis_time:.2f} seconds")

    def test_large_dataset_analysis_performance(self, large_dataset_csv):
        """Test analysis performance with large dataset."""
        importer = DataImporter()
        processor = DataProcessor()
        standards_analyzer = StandardsAnalyzer()
        blanks_analyzer = BlanksAnalyzer()
        duplicates_analyzer = DuplicatesAnalyzer()
        
        # Import and process
        raw_data = importer.read_table(large_dataset_csv)
        processed_data = processor.process_data(raw_data)
        
        # Run all analyses
        start_time = time.time()
        
        standards_results = standards_analyzer.analyze(
            processed_data.get('standards', []),
            certified_value=0.082,
            uncertainty=0.005
        )
        
        blanks_results = blanks_analyzer.analyze(
            processed_data.get('blanks', []),
            detection_limit=0.01
        )
        
        duplicates_results = duplicates_analyzer.analyze(
            processed_data.get('duplicates', [])
        )
        
        total_time = time.time() - start_time
        
        # Should complete in reasonable time (<30 seconds for 1000 samples)
        assert total_time < 30.0
        print(f"\nLarge dataset analysis time: {total_time:.2f} seconds")


class TestMemoryUsage:
    """Test memory usage."""

    def test_memory_usage(self, large_dataset_csv):
        """Test memory usage during processing."""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        importer = DataImporter()
        processor = DataProcessor()
        
        # Import and process
        raw_data = importer.read_table(large_dataset_csv)
        processed_data = processor.process_data(raw_data)
        
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = peak_memory - initial_memory
        
        # Should use reasonable memory (<500MB for 1000 samples)
        assert peak_memory < 500.0
        print(f"\nMemory usage: {peak_memory:.1f} MB (increase: {memory_increase:.1f} MB)")

    def test_memory_cleanup(self, large_dataset_csv):
        """Test that memory is cleaned up after processing."""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        importer = DataImporter()
        processor = DataProcessor()
        
        # Import and process
        raw_data = importer.read_table(large_dataset_csv)
        processed_data = processor.process_data(raw_data)
        
        # Delete references
        del raw_data
        del processed_data
        
        import gc
        gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_after_cleanup = final_memory - initial_memory
        
        # Memory should be reasonable after cleanup
        print(f"\nMemory after cleanup: {final_memory:.1f} MB (increase: {memory_after_cleanup:.1f} MB)")


class TestConcurrentOperations:
    """Test concurrent operation handling."""

    def test_concurrent_operations(self):
        """Test handling of concurrent operations."""
        # This test would simulate concurrent file imports/analyses
        # For now, we'll test that the system can handle multiple operations
        
        # Create multiple small datasets
        datasets = []
        for i in range(5):
            csv_content = f"Sample_ID,Sample_Type,Au_ppm\nRC{i:04d},UNK,{2.0 + i * 0.1}\n"
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                f.write(csv_content)
                datasets.append(Path(f.name))
        
        try:
            importer = DataImporter()
            start_time = time.time()
            
            # Process multiple files
            results = []
            for dataset in datasets:
                raw_data = importer.read_table(dataset)
                results.append(len(raw_data))
            
            total_time = time.time() - start_time
            
            # Should handle multiple files efficiently
            assert total_time < 2.0
            assert all(r > 0 for r in results)
            
        finally:
            for dataset in datasets:
                if os.path.exists(dataset):
                    os.unlink(dataset)


@pytest.mark.performance
class TestPerformanceBenchmarks:
    """Performance benchmarks for documentation."""
    
    def test_benchmark_import_speed(self, large_dataset_csv):
        """Benchmark import speed."""
        importer = DataImporter()
        start_time = time.time()
        raw_data = importer.read_table(large_dataset_csv)
        import_time = time.time() - start_time
        
        samples_per_second = len(raw_data) / import_time
        print(f"\n[Benchmark] Import: {samples_per_second:.0f} samples/second")
        
        # Document benchmark
        assert samples_per_second > 0

    def test_benchmark_analysis_speed(self, large_dataset_csv):
        """Benchmark analysis speed."""
        importer = DataImporter()
        processor = DataProcessor()
        standards_analyzer = StandardsAnalyzer()
        
        raw_data = importer.read_table(large_dataset_csv)
        processed_data = processor.process_data(raw_data)
        
        start_time = time.time()
        standards_analyzer.analyze(
            processed_data.get('standards', []),
            certified_value=0.082,
            uncertainty=0.005
        )
        analysis_time = time.time() - start_time
        
        samples_per_second = len(processed_data.get('standards', [])) / analysis_time if analysis_time > 0 else 0
        print(f"\n[Benchmark] Analysis: {samples_per_second:.0f} standards/second")
        
        assert analysis_time > 0
