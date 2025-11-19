import sys
import os
import yaml
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from analysis import StandardsAnalyzer, BlanksAnalyzer, DuplicatesAnalyzer
from analysis.compliance import ComplianceAnalyzer
from reporting import PDFReporter
from data.crm_database_loader import CRMDatabaseLoader

def test_jorc_workflow():
    print("Starting JORC Workflow Verification...")

    # 1. Load Config
    print("\n1. Loading Configuration...")
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # 2. Test CRM Database
    print("\n2. Testing CRM Database...")
    crm_loader = CRMDatabaseLoader()
    oreas_22e = crm_loader.get_crm_details("OREAS 22e", "Au")
    print(f"Found CRM: {oreas_22e}")
    assert len(oreas_22e) > 0, "Failed to load CRM details"

    # 3. Test Standards Analysis (Westgard)
    print("\n3. Testing Standards Analysis (Westgard Rules)...")
    std_analyzer = StandardsAnalyzer(config['qaqc']['standards'])
    
    # Create mock data with a 2:2s failure
    # Mean = 0.624, SD = 0.019. 2SD = 0.038. 
    # Values > 0.662 are > 2SD.
    mock_std_data = {
        'measured': [0.620, 0.625, 0.670, 0.675, 0.622], # 3rd and 4th are > 2SD
        'certified': 0.624,
        'uncertainty': 0.019
    }
    std_results = std_analyzer.analyze_standards(mock_std_data)
    print(f"Westgard Violations: {std_results['westgard']['violations']}")
    assert std_results['westgard']['failed'], "Failed to detect Westgard violation"

    # 4. Test Duplicates Analysis (Hyperbolic)
    print("\n4. Testing Duplicates Analysis (Hyperbolic Precision)...")
    dup_analyzer = DuplicatesAnalyzer(config['qaqc']['duplicates'])
    
    # Create mock duplicates
    mock_dup_data = {
        'duplicates': [
            [0.1, 0.11], # Good
            [1.0, 1.05], # Good
            [0.01, 0.05] # Bad (high relative diff at low grade)
        ]
    }
    dup_results = dup_analyzer.analyze_duplicates(mock_dup_data)
    print(f"Hyperbolic Failures: {len(dup_results['precision'].get('failures', []))}")
    print(f"Method Used: {dup_results['precision'].get('method')}")
    assert dup_results['precision'].get('method') == 'hyperbolic', "Did not use hyperbolic method"

    # 5. Test Compliance Analysis
    print("\n5. Testing Compliance Analysis...")
    comp_analyzer = ComplianceAnalyzer(config['qaqc'])
    
    counts = {
        'standards': 5,
        'blanks': 5,
        'duplicates': 5
    }
    total_samples = 100
    
    comp_results = comp_analyzer.calculate_insertion_rates(counts, total_samples)
    jorc_statement = comp_analyzer.generate_jorc_statement(comp_results)
    print(f"JORC Statement: {jorc_statement}")
    
    # 6. Test Report Generation
    print("\n6. Testing Report Generation...")
    reporter = PDFReporter(config['reporting']['pdf'])
    
    # Assemble full results
    full_results = {
        'standards': std_results,
        'blanks': {'overall_acceptable': True}, # Mock
        'duplicates': dup_results,
        'compliance': {
            'results': comp_results,
            'jorc_statement': jorc_statement
        },
        'total_samples': total_samples,
        'analysis_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    report_path = reporter.generate_pdf_report(full_results, filename="output/test_jorc_report.pdf")
    print(f"Report generated at: {report_path}")
    assert os.path.exists(report_path), "Report file not created"

    print("\nVerification Complete: SUCCESS")

if __name__ == "__main__":
    test_jorc_workflow()
