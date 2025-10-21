# CRM Manager Module Capabilities

## Overview
The CRM (Certified Reference Material) Manager provides comprehensive functionality for managing and querying certified reference materials used in QAQC analysis. It supports YAML-based database storage with full CRUD operations, validation, and integration with the standards analyzer.

## Key Features

### Database Management
- **YAML Storage**: Human-readable, version-controllable CRM database
- **Automatic Loading**: Seamless database initialization and reloading
- **Data Validation**: Comprehensive CRM data validation and error handling
- **Metadata Support**: Rich metadata including expiry dates, batch numbers, storage conditions

### CRM Querying
- **Name-based Lookup**: Exact and case-insensitive CRM name matching
- **Matrix Filtering**: Find CRMs by matrix type (soil, sediment, ore, etc.)
- **Concentration Range**: Query CRMs within specific concentration ranges
- **Supplier Filtering**: Filter CRMs by supplier (NIST, CANMET, CDN, etc.)
- **Full-text Search**: Search across name, matrix, supplier, and notes

### Validation & Quality Control
- **Expiry Checking**: Automatic CRM expiry date validation
- **Concentration Matching**: Validate CRM suitability for sample concentrations
- **Batch Tracking**: Support for batch number tracking and validation
- **Storage Conditions**: Monitor and validate storage requirements

### Integration Features
- **Standards Analysis**: Direct integration with StandardsAnalyzer
- **Threshold Management**: Centralized analysis threshold configuration
- **Method Information**: Analysis method metadata and specifications
- **Summary Statistics**: Database overview and distribution analysis

## Database Structure

### CRM Entry Format
```yaml
- name: "NIST SRM 2709a"
  certified_value: 0.85
  uncertainty: 0.05
  units: "g/t"
  matrix: "Freshwater Sediment"
  expiry_date: "2026-06-30"
  batch_number: "SRM2709a"
  storage_conditions: "Room temperature, dry"
  supplier: "NIST"
  notes: "Low-level gold standard for environmental analysis"
```

### Analysis Thresholds
```yaml
analysis_thresholds:
  z_score_threshold: 2.0
  recovery_limits:
    min: 90.0
    max: 110.0
  precision_threshold: 5.0  # %RSD
  contamination_threshold: 3.0  # x MDL
  carryover_threshold: 5.0  # %
  blank_limit: 0.1  # g/t
  rpd_threshold: 20.0  # %
  nugget_threshold: 0.3  # ratio
```

### Analysis Methods
```yaml
methods:
  fire_assay:
    name: "Fire Assay with AAS"
    detection_limit: 0.01  # g/t
    working_range: "0.01 - 100 g/t"
    notes: "Standard fire assay method for gold analysis"
```

## API Reference

### CRMManager Class

#### Initialization
```python
from src.data.crm_manager import CRMManager

# Default database path
manager = CRMManager()

# Custom database path
manager = CRMManager('/path/to/crm_database.yaml')
```

#### Core Methods

**Database Operations**
- `get_all_crms()` - Retrieve all CRMs
- `reload_database()` - Reload database from file
- `get_database_info()` - Get database metadata

**CRM Querying**
- `get_crm_by_name(name)` - Get CRM by exact name
- `get_crms_by_matrix(matrix)` - Filter by matrix type
- `get_crms_by_concentration_range(min, max)` - Filter by concentration
- `get_crms_by_supplier(supplier)` - Filter by supplier
- `search_crms(query)` - Full-text search

**Validation & Quality Control**
- `check_crm_expiry(name)` - Check expiry status
- `validate_crm_selection(name, concentration)` - Validate CRM suitability
- `get_certified_value(name)` - Get certified value
- `get_uncertainty(name)` - Get uncertainty value

**Analysis Integration**
- `get_analysis_thresholds()` - Get analysis thresholds
- `get_methods()` - Get analysis methods
- `get_crm_summary()` - Get database statistics

## Usage Examples

### Basic CRM Lookup
```python
# Initialize manager
manager = CRMManager()

# Get specific CRM
crm = manager.get_crm_by_name('NIST SRM 2709a')
print(f"Certified Value: {crm['certified_value']} g/t")
print(f"Uncertainty: ±{crm['uncertainty']} g/t")
```

### Concentration-based CRM Selection
```python
# Find CRMs for low-grade samples
low_crms = manager.get_crms_by_concentration_range(0.1, 1.0)
print(f"Found {len(low_crms)} CRMs for low-grade samples")

# Find CRMs for high-grade samples
high_crms = manager.get_crms_by_concentration_range(10.0, 50.0)
print(f"Found {len(high_crms)} CRMs for high-grade samples")
```

### CRM Validation
```python
# Validate CRM selection
sample_conc = 0.8  # g/t
crm_name = 'NIST SRM 2709a'

is_valid, message = manager.validate_crm_selection(crm_name, sample_conc)
if is_valid:
    print(f"CRM {crm_name} is suitable for sample concentration {sample_conc} g/t")
else:
    print(f"CRM validation failed: {message}")
```

### Standards Analysis Integration
```python
from src.analysis import StandardsAnalyzer

# Get CRM data
crm_info = manager.get_crm_info('NIST SRM 2709a')
certified_value = crm_info['certified_value']
uncertainty = crm_info['uncertainty']

# Prepare analysis data
analysis_data = {
    'measured': [0.82, 0.87, 0.84, 0.86, 0.83],
    'certified': certified_value,
    'uncertainty': uncertainty
}

# Run analysis
analyzer = StandardsAnalyzer()
results = analyzer.analyze_standards(analysis_data)
```

### Database Statistics
```python
# Get database summary
summary = manager.get_crm_summary()
print(f"Total CRMs: {summary['total_crms']}")
print(f"Suppliers: {list(summary['suppliers'].keys())}")
print(f"Concentration Range: {summary['concentration_range']['min']:.2f} - {summary['concentration_range']['max']:.2f} g/t")
```

## Gold Assay CRM Database

The included database contains 11 gold assay CRMs from major suppliers:

### NIST Standards (5 CRMs)
- **SRM 2709a**: 0.85 ± 0.05 g/t (Freshwater Sediment)
- **SRM 2710a**: 2.1 ± 0.1 g/t (Montana Soil)
- **SRM 2711a**: 8.5 ± 0.4 g/t (Montana Soil)
- **SRM 2704**: 15.2 ± 0.8 g/t (Sediment)
- **SRM 2705**: 32.5 ± 1.5 g/t (Sediment)

### CANMET Standards (3 CRMs)
- **OREAS 101**: 0.12 ± 0.02 g/t (Gold Ore)
- **OREAS 102**: 1.25 ± 0.08 g/t (Gold Ore)
- **OREAS 103**: 5.8 ± 0.3 g/t (Gold Ore)

### CDN Standards (3 CRMs)
- **CDN-GS-1**: 0.85 ± 0.05 g/t (Gold Ore)
- **CDN-GS-2**: 2.1 ± 0.1 g/t (Gold Ore)
- **CDN-GS-3**: 8.5 ± 0.4 g/t (Gold Ore)

## Analysis Methods

### Fire Assay
- **Detection Limit**: 0.01 g/t
- **Working Range**: 0.01 - 100 g/t
- **Notes**: Standard fire assay method for gold analysis

### ICP-MS
- **Detection Limit**: 0.001 g/t
- **Working Range**: 0.001 - 10 g/t
- **Notes**: Inductively coupled plasma mass spectrometry

### ICP-AES
- **Detection Limit**: 0.01 g/t
- **Working Range**: 0.01 - 50 g/t
- **Notes**: Inductively coupled plasma atomic emission spectrometry

## Best Practices

### CRM Selection
1. **Concentration Matching**: Choose CRMs within 50-200% of sample concentration
2. **Matrix Compatibility**: Match CRM matrix to sample matrix when possible
3. **Expiry Validation**: Always check CRM expiry dates before use
4. **Batch Tracking**: Record batch numbers for traceability

### Quality Control
1. **Regular Validation**: Check CRM expiry dates monthly
2. **Concentration Verification**: Validate CRM suitability for each analysis
3. **Storage Monitoring**: Ensure proper storage conditions
4. **Documentation**: Maintain records of CRM usage and performance

### Database Maintenance
1. **Version Control**: Use Git for database version control
2. **Regular Updates**: Update CRM database with new materials
3. **Expiry Monitoring**: Track and replace expired CRMs
4. **Backup**: Maintain database backups for data integrity

## Future Enhancements

### Planned Features
- **SQLite Migration**: Database migration to SQLite for production use
- **Web Interface**: Web-based CRM management interface
- **API Integration**: REST API for external CRM data sources
- **Automated Updates**: Automatic CRM database updates from suppliers
- **Performance Analytics**: CRM performance tracking and analytics
- **Multi-language Support**: Internationalization for global use

### Integration Opportunities
- **LIMS Integration**: Laboratory Information Management System integration
- **ERP Connectivity**: Enterprise Resource Planning system connectivity
- **Cloud Storage**: Cloud-based CRM database storage
- **Mobile Access**: Mobile application for field CRM management
