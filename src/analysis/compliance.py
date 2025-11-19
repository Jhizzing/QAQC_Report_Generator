from typing import Dict, List, Any

class ComplianceAnalyzer:
    """
    Analyzes dataset compliance with JORC QAQC requirements.
    
    Key checks:
    - Insertion rates (Standards, Blanks, Duplicates)
    - Completeness (Batch coverage)
    - Overall health
    """
    
    def __init__(self, config: Dict = None) -> None:
        """
        Initialize with QAQC configuration.
        
        Args:
            config: Dictionary with insertion rate targets and settings
        """
        self.config = config or {}
        self.insertion_targets = self.config.get('insertion_rates', {
            'target_total': 20.0,
            'target_standards': 5.0,
            'target_blanks': 5.0,
            'target_duplicates': 5.0,
            'target_check_assays': 5.0
        })

    def calculate_insertion_rates(self, counts: Dict[str, int], total_samples: int) -> Dict:
        """
        Calculate actual insertion rates against targets.
        
        Args:
            counts: Dictionary of counts per QAQC type (e.g., {'standards': 50, 'blanks': 50})
            total_samples: Total number of samples in the dataset (including QAQC)
            
        Returns:
            Dictionary with insertion rate analysis
        """
        if total_samples == 0:
            return {'rates': {}, 'compliance': False, 'summary': "No samples found"}
            
        rates = {}
        compliance = {}
        
        # Calculate rates
        for qtype, count in counts.items():
            rate = (count / total_samples) * 100
            rates[qtype] = rate
            
            # Check compliance
            target_key = f"target_{qtype}"
            target = self.insertion_targets.get(target_key, 0.0)
            compliance[qtype] = {
                'actual': rate,
                'target': target,
                'met': rate >= target,
                'deficit': max(0, target - rate)
            }
            
        # Total QAQC rate
        total_qaqc = sum(counts.values())
        total_rate = (total_qaqc / total_samples) * 100
        target_total = self.insertion_targets.get('target_total', 20.0)
        
        compliance['total'] = {
            'actual': total_rate,
            'target': target_total,
            'met': total_rate >= target_total
        }
        
        return {
            'rates': rates,
            'compliance': compliance,
            'total_samples': total_samples,
            'total_qaqc': total_qaqc
        }

    def check_batch_completeness(self, batches: List[Dict]) -> Dict:
        """
        Check if all batches have required QAQC samples.
        
        Args:
            batches: List of batch dictionaries, each containing 'id' and 'qaqc_counts'
            
        Returns:
            Dictionary with completeness analysis
        """
        incomplete_batches = []
        
        for batch in batches:
            counts = batch.get('qaqc_counts', {})
            has_standards = counts.get('standards', 0) > 0
            has_blanks = counts.get('blanks', 0) > 0
            has_duplicates = counts.get('duplicates', 0) > 0
            
            if not (has_standards and has_blanks and has_duplicates):
                missing = []
                if not has_standards: missing.append('Standards')
                if not has_blanks: missing.append('Blanks')
                if not has_duplicates: missing.append('Duplicates')
                
                incomplete_batches.append({
                    'batch_id': batch.get('id', 'Unknown'),
                    'missing': missing
                })
                
        return {
            'completeness_rate': (len(batches) - len(incomplete_batches)) / len(batches) * 100 if batches else 100,
            'incomplete_batches': incomplete_batches,
            'total_batches': len(batches)
        }

    def generate_jorc_statement(self, insertion_analysis: Dict) -> str:
        """
        Generate a JORC Table 1 style statement based on analysis.
        
        Args:
            insertion_analysis: Result from calculate_insertion_rates
            
        Returns:
            Text statement for JORC report
        """
        comp = insertion_analysis.get('compliance', {})
        total = comp.get('total', {})
        stds = comp.get('standards', {})
        blks = comp.get('blanks', {})
        dups = comp.get('duplicates', {})
        
        statement = (
            f"QAQC samples were inserted at an overall rate of {total.get('actual', 0):.1f}%, "
            f"{'meeting' if total.get('met') else 'below'} the target of {total.get('target', 0)}%. "
            f"The program included Standards ({stds.get('actual', 0):.1f}%), "
            f"Blanks ({blks.get('actual', 0):.1f}%), and "
            f"Duplicates ({dups.get('actual', 0):.1f}%)."
        )
        
        if not total.get('met'):
            statement += " Corrective action is recommended to increase QAQC frequency in future programs."
            
        return statement
