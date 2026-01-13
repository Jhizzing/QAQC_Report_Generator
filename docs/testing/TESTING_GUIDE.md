# Testing Guide

This guide explains how to run tests, write new tests, and understand test coverage for the QAQC Report Generator.

## Running Tests

### All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html
```

### Test Categories

Tests are organized by category using pytest markers:

```bash
# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# End-to-end tests
pytest -m e2e

# Performance tests
pytest -m performance

# Backend API tests
pytest -m backend

# Exclude slow tests
pytest -m "not slow"
```

### Specific Test Files

```bash
# Run specific test file
pytest tests/test_analysis.py

# Run specific test function
pytest tests/test_analysis.py::test_standards_analysis

# Run tests matching a pattern
pytest -k "test_standards"
```

## Test Structure

### Unit Tests

Unit tests test individual components in isolation:

- **Location**: `tests/test_*.py`
- **Marker**: `@pytest.mark.unit`
- **Examples**: `test_analysis.py`, `test_importer.py`

### Integration Tests

Integration tests test component interactions:

- **Location**: `tests/test_integration.py`, `tests/test_e2e_workflows.py`
- **Marker**: `@pytest.mark.integration`
- **Examples**: Full pipeline tests, file import to report generation

### End-to-End Tests

E2E tests test complete workflows:

- **Location**: `tests/test_e2e_workflows.py`
- **Marker**: `@pytest.mark.e2e`
- **Examples**: Complete gold workflow, pXRF workflow, multi-element workflow

### Performance Tests

Performance tests measure speed and memory usage:

- **Location**: `tests/test_performance.py`
- **Marker**: `@pytest.mark.performance`
- **Examples**: Large dataset processing, memory usage, concurrent operations

### Backend Integration Tests

Backend tests test FastAPI endpoints:

- **Location**: `tests/test_backend_integration.py`
- **Marker**: `@pytest.mark.backend`
- **Examples**: File upload, analysis execution, plot generation

## Writing New Tests

### Test File Template

```python
"""Tests for [component name]."""
import pytest
from src.module import Component

class TestComponent:
    """Test suite for Component."""
    
    def test_basic_functionality(self):
        """Test basic component functionality."""
        component = Component()
        result = component.do_something()
        assert result is not None
    
    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
        (3, 6),
    ])
    def test_with_parameters(self, input, expected):
        """Test with multiple inputs."""
        component = Component()
        result = component.multiply(input, 2)
        assert result == expected
```

### Test Fixtures

Use fixtures for reusable test data:

```python
@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return {
        'samples': [1, 2, 3],
        'values': [10.0, 20.0, 30.0]
    }

def test_with_fixture(sample_data):
    """Test using fixture."""
    assert len(sample_data['samples']) == 3
```

### Mocking

Use mocks for external dependencies:

```python
from unittest.mock import Mock, patch

def test_with_mock():
    """Test with mocked dependency."""
    with patch('src.module.external_function') as mock_func:
        mock_func.return_value = 'mocked'
        result = function_under_test()
        assert result == 'mocked'
        mock_func.assert_called_once()
```

## Test Coverage

### Coverage Goals

- **Overall**: >70% (current target)
- **Critical paths**: >80%
- **New code**: >90%

### Viewing Coverage

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Coverage Exclusions

Some code is excluded from coverage:
- Test files themselves
- Abstract base classes
- Type checking blocks
- Debug/development code

## Performance Benchmarks

### Running Benchmarks

```bash
# Run performance tests
pytest -m performance -v

# Run with timing
pytest -m performance --durations=10
```

### Benchmark Targets

- **Import**: >100 samples/second
- **Analysis**: >50 standards/second
- **Report Generation**: <10 seconds for typical dataset
- **Memory**: <500MB for 1000 samples

### Recording Benchmarks

Performance benchmarks are documented in test output and should be tracked over time to detect regressions.

## Test Data

### Test Fixtures

Test data is provided through fixtures in `tests/conftest.py` and individual test files.

### Mock Data

Mock data files are in `mock_data/`:
- `complex_test_data.csv` - Complex QAQC dataset
- `gui_test_data.csv` - GUI testing dataset

### Creating Test Data

When creating new test data:
1. Use realistic values
2. Include edge cases
3. Document expected results
4. Keep files small for fast tests

## Continuous Integration

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Multiple platforms (Linux, macOS, Windows)
- Multiple Python versions (3.11, 3.12)

### CI Test Results

Check GitHub Actions for test results:
- Green checkmark: All tests passed
- Red X: Tests failed
- Yellow circle: Tests in progress

## Troubleshooting

### Tests Failing Locally

1. **Check Python version**: Requires Python 3.11+
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Check test data**: Ensure mock data files exist
4. **Clear cache**: `pytest --cache-clear`

### Import Errors

If tests fail with import errors:
1. Ensure project root is in Python path
2. Check `conftest.py` path setup
3. Verify `src/` directory structure

### Performance Test Failures

Performance tests may fail on slower machines:
- Adjust thresholds in test if needed
- Document machine specs with results
- Use `@pytest.mark.slow` for long-running tests

## Best Practices

1. **Write tests first** (TDD) when possible
2. **Test edge cases** and error conditions
3. **Keep tests independent** - no shared state
4. **Use descriptive names** for test functions
5. **Document complex test logic** with comments
6. **Keep tests fast** - use mocks for slow operations
7. **Test one thing** per test function
8. **Clean up** temporary files and resources

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Test Coverage Guide](https://coverage.readthedocs.io/)
