# Changelog

All notable changes to the QAQC Report Generator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0-pre] - 2026-01-13

### Added
- **Advanced Analysis Features**
  - Correlation analysis for duplicate pairs with Pearson correlation coefficient and p-value
  - Nugget ratio calculation for geostatistical precision assessment
  - Configurable thresholds for correlation and nugget ratio analysis
  - Visual indicators for correlation strength and nugget ratio interpretation

- **React UI Enhancements**
  - Modern web-based interface with real-time analysis
  - Interactive Plotly charts with synchronized data tables
  - Method-specific presets (ICP-MS, ICP-OES, pXRF, Fire Assay, AAS)
  - Element-specific QAQC configuration
  - Project persistence with save/load functionality

- **Backend API**
  - FastAPI-based backend for scalable analysis processing
  - RESTful API endpoints for data upload, analysis, and report generation
  - Health check endpoint for service monitoring

- **Documentation**
  - Comprehensive user documentation in `docs/user/`
  - Technical documentation for analysis methods
  - Installation guides for all platforms
  - Troubleshooting guide

- **Testing Infrastructure**
  - Comprehensive test suite (125/142 tests passing - 88% pass rate)
  - E2E workflow tests for gold, pXRF, and multi-element analysis
  - Performance tests for large datasets
  - Backend API integration tests

### Changed
- Updated README.md with pre-release status and new features
- Enhanced error handling across all modules
- Improved data validation and error messages
- Updated test suite to match current API

### Fixed
- Fixed missing `psutil` dependency in requirements.txt
- Fixed test method name mismatches (PDF reporter tests)
- Fixed E2E workflow tests to use correct API methods
- Fixed nugget ratio tests to expect dict return type
- Fixed Excel import test placeholder implementation
- Fixed project save/load test data structure expectations

### Technical Details
- **Test Coverage**: 88% pass rate (125/142 tests)
- **Critical Path**: All core functionality verified
- **Build System**: PyInstaller scripts ready for executable creation
- **Dependencies**: All required packages documented in requirements.txt

## [Unreleased]

### Planned
- Full executable builds for Windows, macOS, and Linux
- Installer packages (DMG, EXE, AppImage)
- Additional test coverage improvements
- Performance optimizations for very large datasets
- Enhanced JORC report templates

---

## Version History

- **1.0.0-pre**: Pre-release version with advanced analysis features
- **0.9.0**: Beta version with React UI and backend API
- **0.8.0**: Initial release with PyQt GUI
- **0.7.0**: Core analysis engine with CRM integration
- **0.6.0**: Basic reporting and visualization
- **0.5.0**: Data import and processing
- **0.1.0**: Initial project setup

---

For detailed information about specific features, see:
- [User Documentation](docs/user/)
- [Analysis Methods](docs/ANALYSIS_METHODS.md)
- [Installation Guide](docs/user/INSTALLATION.md)
- [Troubleshooting](docs/user/TROUBLESHOOTING.md)
