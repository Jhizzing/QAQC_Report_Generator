# QAQC Report Generator - Testing Guide

## Table of Contents
1. [Introduction to Testing](#introduction-to-testing)
2. [Testing Setup](#testing-setup)
3. [Running Tests](#running-tests)
4. [Understanding Test Structure](#understanding-test-structure)
5. [Test Categories Explained](#test-categories-explained)
6. [Interpreting Test Results](#interpreting-test-results)
7. [Test Coverage](#test-coverage)
8. [Common Testing Scenarios](#common-testing-scenarios)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## Introduction to Testing

### What Are Tests?

Tests are pieces of code that verify your application works correctly. Think of them as automated quality checks that run every time you make changes to ensure nothing broke.

**Simple Analogy**: If your application is a car, tests are like:
- **Unit Tests**: Checking each part individually (engine, brakes, lights)
- **Integration Tests**: Checking parts work together (engine + transmission)
- **End-to-End Tests**: Taking the car for a full drive

### Why Do We Write Tests?

1. **Catch Bugs Early**: Find problems before users do
2. **Documentation**: Tests show how code is supposed to work
3. **Confidence**: Make changes knowing tests will catch mistakes
4. **Refactoring Safety**: Improve code structure without breaking functionality
5. **Regression Prevention**: Ensure old bugs don't come back

### Types of Tests in Our Application

**Unit Tests**: Test individual functions/components in isolation
- Example: Testing that a file processor correctly reads CSV files
- Location: `react_ui/src/utils/__tests__/`

**Integration Tests**: Test how multiple parts work together
- Example: Testing that file upload → analysis → report generation works
- Location: `react_ui/api/tests/test_api.py`

**Component Tests**: Test React components render and behave correctly
- Example: Testing that the ImportWorkflow component handles file drops
- Location: `react_ui/src/features/*/__tests__/`

**Error Scenario Tests**: Test that errors are handled gracefully
- Example: Testing what happens when a file is too large or corrupted
- Location: `react_ui/src/utils/__tests__/errorScenarios.test.ts`

---

## Testing Setup

### Prerequisites

Before running tests, ensure you have:

1. **Node.js and npm** (for React UI tests)
   - Check: `node --version` (should be v18+)
   - Check: `npm --version` (should be v9+)

2. **Python 3.11+** (for FastAPI tests)
   - Check: `python3 --version`

### Installing Test Dependencies

#### React UI Tests

```bash
cd react_ui
npm install
```

This installs:
- `vitest` - The testing framework
- `@testing-library/react` - Tools for testing React components
- `@testing-library/jest-dom` - Additional matchers for assertions
- `jsdom` - Simulates a browser environment for tests

#### FastAPI Tests

```bash
cd react_ui/api
pip install -r requirements-test.txt
```

This installs:
- `pytest` - Python testing framework
- `pytest-asyncio` - Support for async tests
- `httpx` - HTTP client for testing API endpoints
- `pytest-cov` - Coverage reporting

### Test Configuration Files

**React UI**: `react_ui/vitest.config.ts`
- Configures Vitest to work with Vite
- Sets up test environment (jsdom for browser simulation)
- Configures path aliases and coverage settings

**FastAPI**: `react_ui/api/tests/conftest.py`
- Sets up pytest fixtures (reusable test data)
- Creates test client for API testing
- Provides sample files for testing

---

## Running Tests

### React UI Tests

#### Run All Tests (Watch Mode)
```bash
cd react_ui
npm test
```
**What this does**: Runs all tests and watches for file changes. When you modify code, tests automatically re-run.

**Output**: Shows passing tests (✓) and failing tests (✗) with details.

#### Run Tests Once (No Watch)
```bash
cd react_ui
npm run test:run
```
**What this does**: Runs all tests once and exits. Useful for CI/CD or when you just want a quick check.

#### Run Tests with UI
```bash
cd react_ui
npm run test:ui
```
**What this does**: Opens a web-based test UI where you can:
- See all tests in a tree view
- Filter by status (pass/fail)
- See test execution time
- Click on tests to see details

#### Run Tests with Coverage
```bash
cd react_ui
npm run test:coverage
```
**What this does**: Runs tests and generates a coverage report showing:
- Which lines of code were executed during tests
- Percentage of code covered
- HTML report in `coverage/` directory

**Understanding Coverage**:
- **80%+ coverage**: Good - most code is tested
- **50-80%**: Moderate - some areas need more tests
- **<50%**: Low - significant gaps in testing

### FastAPI Tests

#### Run All API Tests
```bash
cd react_ui/api
pytest tests/
```
**What this does**: Runs all tests in the `tests/` directory.

#### Run with Verbose Output
```bash
pytest tests/ -v
```
**What this does**: Shows detailed output for each test, including test names and results.

#### Run Specific Test File
```bash
pytest tests/test_api.py
```
**What this does**: Runs only tests in that specific file.

#### Run Specific Test Function
```bash
pytest tests/test_api.py::test_health_check
```
**What this does**: Runs only the `test_health_check` function.

#### Run with Coverage
```bash
pytest tests/ --cov=api --cov-report=html
```
**What this does**: Generates coverage report for the API code.

---

## Understanding Test Structure

### Basic Test Structure

Every test follows this pattern:

```typescript
// React/TypeScript Example
describe('Component or Function Name', () => {
  it('should do something specific', () => {
    // Arrange: Set up test data
    const input = 'test data';
    
    // Act: Execute the function
    const result = myFunction(input);
    
    // Assert: Check the result
    expect(result).toBe('expected output');
  });
});
```

**Breaking it down**:
- `describe()`: Groups related tests together
- `it()` or `test()`: Defines a single test case
- `expect()`: Makes assertions about the result
- `.toBe()`, `.toEqual()`, etc.: Matchers that check values

### Real Example: File Processor Test

Let's look at an actual test from our codebase:

```typescript
// react_ui/src/utils/__tests__/fileProcessor.test.ts
describe('fileProcessor', () => {
  describe('processFile', () => {
    it('should process a valid CSV file', async () => {
      // Arrange: Create a mock CSV file
      const csvContent = 'SampleID,Type,Result\nSTD-001,STD,10.5';
      const file = createMockFile('test.csv', csvContent, 'text/csv');
      
      // Act: Process the file
      const result = await processFile(file);
      
      // Assert: Check the results
      expect(result.fileName).toBe('test.csv');
      expect(result.headers).toEqual(['SampleID', 'Type', 'Result']);
      expect(result.data.length).toBe(1);
    });
  });
});
```

**What this test does**:
1. Creates a mock CSV file with test data
2. Calls the `processFile` function
3. Verifies it correctly:
   - Extracts the filename
   - Parses the headers
   - Processes the data rows

### Python Test Example

```python
# react_ui/api/tests/test_api.py
def test_health_check(client: TestClient):
    """Test health check endpoint."""
    # Act: Make a request to the health endpoint
    response = client.get("/health")
    
    # Assert: Check the response
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
```

**What this test does**:
1. Makes an HTTP GET request to `/health`
2. Verifies the response status is 200 (OK)
3. Checks the response contains expected data

---

## Test Categories Explained

### 1. Utility Function Tests

**Location**: `react_ui/src/utils/__tests__/`

**What they test**: Pure functions that don't depend on React or external services.

**Examples**:
- **fileProcessor.test.ts**: Tests file reading and parsing
  - Valid CSV files
  - Valid Excel files
  - Empty files (should fail)
  - Corrupted files (should fail)
  - Files that are too large (should fail)

- **projectFile.test.ts**: Tests saving/loading project files
  - Saving project state to .qaqc file
  - Loading project from .qaqc file
  - Invalid file formats
  - Missing required fields

- **export.test.ts**: Tests report generation
  - Exporting figures only
  - Exporting full JORC reports
  - Different configuration options

**Why these matter**: These are foundational functions used throughout the app. If they break, everything breaks.

### 2. Hook and Store Tests

**Location**: `react_ui/src/hooks/__tests__/` and `react_ui/src/stores/__tests__/`

**What they test**: Custom React hooks and state management (Zustand stores).

**Examples**:
- **useBackendService.test.ts**: Tests backend connection management
  - Detecting when backend is available
  - Handling connection failures
  - Periodic health checks
  - Retry logic

- **settingsStore.test.ts**: Tests settings persistence
  - Updating export settings
  - Updating analysis settings
  - Resetting to defaults
  - Settings persistence across sessions

- **projectStore.test.ts**: Tests project management
  - Creating new projects
  - Opening existing projects
  - Updating project metadata
  - Recent projects list

**Why these matter**: These manage application state. Bugs here affect the entire user experience.

### 3. Component Tests

**Location**: `react_ui/src/features/*/__tests__/`

**What they test**: React components render correctly and handle user interactions.

**Examples**:
- **ImportWorkflow.test.tsx**: Tests file import functionality
  - File upload interface renders
  - File processing works
  - Error handling for invalid files
  - Demo data loading

- **AnalysisSetup.test.tsx**: Tests analysis configuration
  - Category selection
  - Methodology configuration
  - QAQC rules setup

- **ResultsDashboard.test.tsx**: Tests results display
  - Summary statistics display
  - Tab navigation
  - Chart rendering (basic checks)

- **SettingsPage.test.tsx**: Tests settings management
  - Settings sections render
  - Settings updates work
  - Backend status display

**Why these matter**: These are what users interact with. Component bugs directly impact usability.

### 4. API Endpoint Tests

**Location**: `react_ui/api/tests/test_api.py`

**What they test**: FastAPI endpoints work correctly and handle errors.

**Examples**:
- **test_health_check**: Verifies API is running
- **test_upload_csv**: Tests file upload
- **test_analyze_endpoint**: Tests analysis execution
- **test_export_excel**: Tests report generation
- **test_crms_list**: Tests CRM database queries

**Why these matter**: The API is the bridge between React UI and Python backend. API bugs break the entire workflow.

### 5. Error Scenario Tests

**Location**: `react_ui/src/utils/__tests__/errorScenarios.test.ts` and `react_ui/api/tests/test_error_handling.py`

**What they test**: How the application handles errors and edge cases.

**Examples**:
- Network failures
- Timeout errors
- Invalid file formats
- Files that are too large
- Missing required data
- Server errors (500, 404, etc.)

**Why these matter**: Real-world usage involves errors. The app must handle them gracefully, not crash.

---

## Interpreting Test Results

### Passing Tests

When a test passes, you'll see:

```
✓ fileProcessor > processFile > should process a valid CSV file (123ms)
```

**What this means**:
- ✓ = Test passed
- `fileProcessor > processFile > should process...` = Test location/name
- `(123ms)` = How long the test took

### Failing Tests

When a test fails, you'll see:

```
✗ fileProcessor > processFile > should reject empty files (45ms)

AssertionError: expected "File is empty" to be thrown

  Expected: "File is empty"
  Received: undefined
```

**What this means**:
- ✗ = Test failed
- The error message shows what was expected vs what actually happened
- The stack trace shows where the failure occurred

### Test Output Breakdown

```
Test Files  1 passed (1)
     Tests  15 passed (15)
      Time  2.34s
```

**Breaking it down**:
- **Test Files**: Number of test files that ran
- **Tests**: Total number of individual test cases
- **Time**: Total execution time

### Understanding Error Messages

**Common error types**:

1. **AssertionError**: Expected value doesn't match actual value
   ```
   Expected: "expected value"
   Received: "actual value"
   ```
   **Fix**: Check why the function returned a different value than expected

2. **TypeError**: Wrong data type used
   ```
   Cannot read property 'x' of undefined
   ```
   **Fix**: Check that variables are defined before use

3. **NetworkError**: API call failed
   ```
   Failed to fetch
   ```
   **Fix**: Check if backend is running, network connection, or API URL

4. **TimeoutError**: Operation took too long
   ```
   Request timeout after 30000ms
   ```
   **Fix**: Operation may be too slow, or server is not responding

---

## Test Coverage

### What is Coverage?

Coverage measures how much of your code is executed during tests. It's expressed as a percentage.

**Example Coverage Report**:
```
File                    | % Stmts | % Branch | % Funcs | % Lines
------------------------|---------|----------|---------|--------
src/utils/fileProcessor |   85.71 |    66.67 |   100.00 |   85.71
src/api/client.ts       |   72.22 |    50.00 |   80.00  |   72.22
```

**What the columns mean**:
- **% Stmts**: Percentage of statements executed
- **% Branch**: Percentage of if/else branches tested
- **% Funcs**: Percentage of functions called
- **% Lines**: Percentage of lines executed

### Viewing Coverage Reports

#### React UI Coverage

After running `npm run test:coverage`:

1. Open `react_ui/coverage/index.html` in a browser
2. You'll see:
   - Overall coverage percentage
   - Coverage by file
   - Click files to see which lines are covered (green) vs not covered (red)

#### FastAPI Coverage

After running `pytest tests/ --cov=api --cov-report=html`:

1. Open `htmlcov/index.html` in a browser
2. Similar interface showing Python code coverage

### What Coverage Tells Us

**High Coverage (80%+)**: Most code paths are tested. Good confidence that code works.

**Medium Coverage (50-80%)**: Some areas tested, but gaps exist. May miss edge cases.

**Low Coverage (<50%)**: Significant portions untested. Higher risk of bugs.

**Important Note**: 100% coverage doesn't mean bug-free! It just means all code ran. Tests must also check the *right* things.

---

## Common Testing Scenarios

### Scenario 1: Testing a New Feature

**Process**:
1. Write the feature code
2. Write tests for the feature
3. Run tests to verify it works
4. Run all tests to ensure nothing broke

**Example**: Adding a new export format
- Write export function
- Write test: "should export in new format"
- Run test: `npm test` (watch for your new test)
- Verify it passes
- Run all tests: `npm run test:run`

### Scenario 2: Fixing a Bug

**Process**:
1. Reproduce the bug
2. Write a test that fails (demonstrating the bug)
3. Fix the bug
4. Verify the test now passes
5. Run all tests to ensure fix didn't break anything

**Example**: File upload fails with special characters in filename
- Write test: "should handle filenames with special characters"
- Test fails (bug reproduced)
- Fix the file upload code
- Test passes (bug fixed)
- All other tests still pass (nothing broken)

### Scenario 3: Refactoring Code

**Process**:
1. Run tests to establish baseline (all passing)
2. Refactor code (improve structure without changing behavior)
3. Run tests again
4. If tests still pass, refactoring was successful

**Example**: Improving file processor code structure
- All tests pass before refactoring
- Refactor code (extract functions, improve readability)
- Run tests: `npm test`
- If all pass, refactoring maintained functionality

### Scenario 4: Testing Error Handling

**Process**:
1. Identify error scenarios (network failure, invalid input, etc.)
2. Write tests that simulate these errors
3. Verify app handles errors gracefully (shows user-friendly message, doesn't crash)

**Example**: Testing file upload with network failure
- Mock network to fail
- Attempt file upload
- Verify: Shows error message, doesn't crash, allows retry

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Tests Can't Find Modules

**Error**: `Cannot find module 'xyz'`

**Solution**: 
- Check import paths are correct
- Verify dependencies are installed: `npm install`
- Check `vitest.config.ts` path aliases match `vite.config.ts`

#### Issue: Tests Timeout

**Error**: `Test timeout exceeded`

**Solution**:
- Test may be waiting for async operation that never completes
- Check for missing `await` or unhandled promises
- Increase timeout if operation is legitimately slow

#### Issue: Mock Not Working

**Error**: Function not being mocked as expected

**Solution**:
- Verify mock is set up before the function is called
- Check mock syntax: `vi.mock()` vs `vi.fn()`
- Ensure mock is in correct scope

#### Issue: FastAPI Tests Can't Import App

**Error**: `ModuleNotFoundError: No module named 'api'`

**Solution**:
- Check Python path is set correctly in `conftest.py`
- Verify you're running from correct directory
- Check `sys.path` includes project root

#### Issue: Component Test Fails with "Not wrapped in act()"

**Error**: React warning about state updates

**Solution**:
- Use `waitFor()` for async operations
- Use `userEvent` instead of `fireEvent` for user interactions
- Wrap state updates in `act()` if needed

---

## Next Steps

### Immediate Actions

1. **Run the Test Suite**
   ```bash
   # React UI
   cd react_ui && npm test
   
   # FastAPI
   cd react_ui/api && pytest tests/ -v
   ```

2. **Review Test Results**
   - Note any failing tests
   - Understand what each test is checking
   - Review coverage report

3. **Familiarize Yourself with Test Structure**
   - Look at a few test files
   - Understand the pattern: describe → it → expect
   - See how different types of code are tested

### Learning Path

**Beginner**:
- Run existing tests
- Read test code to understand what's being tested
- Modify a simple test to see how it works

**Intermediate**:
- Write tests for new features
- Add test cases for edge cases
- Improve test coverage

**Advanced**:
- Write integration tests
- Set up CI/CD test automation
- Optimize test performance

### Recommended Reading Order

1. Start with utility tests (`fileProcessor.test.ts`) - simplest
2. Move to store tests (`settingsStore.test.ts`) - state management
3. Then component tests (`ImportWorkflow.test.tsx`) - React components
4. Finally API tests (`test_api.py`) - backend integration

### Questions to Consider

As you review tests, ask yourself:

1. **What is this test checking?** - Understand the purpose
2. **What would break if this test failed?** - Understand the impact
3. **Are there edge cases not covered?** - Think about what could go wrong
4. **Is the test clear and readable?** - Good tests document behavior

---

## Quick Reference

### React UI Test Commands

```bash
# Run all tests (watch mode)
npm test

# Run tests once
npm run test:run

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Run specific test file
npm test fileProcessor.test.ts
```

### FastAPI Test Commands

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::test_health_check

# Run with coverage
pytest tests/ --cov=api --cov-report=html
```

### Test File Locations

**React UI**:
- Utilities: `react_ui/src/utils/__tests__/`
- Hooks: `react_ui/src/hooks/__tests__/`
- Stores: `react_ui/src/stores/__tests__/`
- Components: `react_ui/src/features/*/__tests__/`

**FastAPI**:
- All tests: `react_ui/api/tests/`
- Main tests: `react_ui/api/tests/test_api.py`
- Error tests: `react_ui/api/tests/test_error_handling.py`

---

## Summary

Testing is a crucial part of software development that:

1. **Verifies functionality**: Ensures code works as intended
2. **Prevents regressions**: Catches bugs when code changes
3. **Documents behavior**: Tests show how code should work
4. **Enables refactoring**: Safe to improve code structure

Our test suite covers:
- ✅ Utility functions (file processing, exports, project files)
- ✅ State management (hooks and stores)
- ✅ React components (user interfaces)
- ✅ API endpoints (backend functionality)
- ✅ Error scenarios (edge cases and failures)

**Next**: Run the tests and explore the results. Start with simple utility tests and work your way up to more complex component and integration tests.

---

## Additional Resources

- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
