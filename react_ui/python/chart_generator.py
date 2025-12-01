"""
QAQC Chart Generation Module
Generates publication-quality charts for QAQC reports using Matplotlib
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import List, Dict, Any, Tuple
import json
import sys
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
LOGIQORE_GOLD = '#FBBF24'
LOGIQORE_DARK = '#1F2937'

def generate_control_chart(
    data: List[Dict[str, Any]],
    certified_value: float,
    element: str,
    crm_name: str,
    output_path: str
) -> str:
    """
    Generate a Shewhart control chart for standards monitoring
    
    Args:
        data: List of dicts with 'sequence', 'value', 'batch_id'
        certified_value: Target value from CRM certificate
        element: Element name (e.g., 'Au')
        crm_name: CRM identifier (e.g., 'OREAS-101')
        output_path: Path to save the chart
    
    Returns:
        Path to saved chart
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Extract data
    sequences = [d['sequence'] for d in data]
    values = [d['value'] for d in data]
    
    # Calculate statistics
    mean_value = np.mean(values)
    std_dev = np.std(values, ddof=1)
    
    # Control limits
    ucl_3 = certified_value + 3 * std_dev
    lcl_3 = certified_value - 3 * std_dev
    ucl_2 = certified_value + 2 * std_dev
    lcl_2 = certified_value - 2 * std_dev
    
    # Plot data points
    ax.plot(sequences, values, 'o-', color=LOGIQORE_DARK, markersize=6, linewidth=1.5, label='Measured')
    
    # Plot control lines
    ax.axhline(certified_value, color=LOGIQORE_GOLD, linewidth=2, label='Target', zorder=3)
    ax.axhline(ucl_3, color='red', linewidth=1, linestyle='--', label='±3σ', alpha=0.7)
    ax.axhline(lcl_3, color='red', linewidth=1, linestyle='--', alpha=0.7)
    ax.axhline(ucl_2, color='orange', linewidth=1, linestyle=':', label='±2σ', alpha=0.7)
    ax.axhline(lcl_2, color='orange', linewidth=1, linestyle=':', alpha=0.7)
    
    # Shade control zones
    ax.fill_between(sequences, lcl_2, ucl_2, alpha=0.1, color='green', label='Pass Zone')
    ax.fill_between(sequences, ucl_2, ucl_3, alpha=0.1, color='yellow')
    ax.fill_between(sequences, lcl_3, lcl_2, alpha=0.1, color='yellow')
    
    # Highlight out-of-control points
    for i, (seq, val) in enumerate(zip(sequences, values)):
        if val > ucl_3 or val < lcl_3:
            ax.plot(seq, val, 'ro', markersize=10, markeredgewidth=2, markerfacecolor='none')
    
    # Styling
    ax.set_xlabel('Sample Sequence', fontsize=12, fontweight='bold')
    ax.set_ylabel(f'{element} Value', fontsize=12, fontweight='bold')
    ax.set_title(f'Control Chart: {crm_name} - {element}', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    # Add statistics text box
    stats_text = f'Mean: {mean_value:.4f}\nSD: {std_dev:.4f}\nRSD: {(std_dev/mean_value*100):.2f}%'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_path


def generate_scatter_plot(
    data: List[Dict[str, Any]],
    element: str,
    output_path: str
) -> str:
    """
    Generate scatter plot for duplicate analysis (Original vs Duplicate)
    
    Args:
        data: List of dicts with 'original', 'duplicate', 'rpd'
        element: Element name
        output_path: Path to save the chart
    
    Returns:
        Path to saved chart
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Extract data
    originals = [d['original'] for d in data]
    duplicates = [d['duplicate'] for d in data]
    rpds = [d['rpd'] for d in data]
    
    # Calculate plot range
    all_values = originals + duplicates
    min_val = min(all_values) * 0.9
    max_val = max(all_values) * 1.1
    
    # 45-degree reference line (perfect agreement)
    ax.plot([min_val, max_val], [min_val, max_val], 'k--', linewidth=2, label='Perfect Agreement', alpha=0.7)
    
    # ±10% envelope
    envelope_upper = np.array([min_val, max_val]) * 1.1
    envelope_lower = np.array([min_val, max_val]) * 0.9
    ax.fill_between([min_val, max_val], envelope_lower, envelope_upper, 
                     alpha=0.2, color='green', label='±10% Envelope')
    
    # Color points by RPD
    scatter = ax.scatter(originals, duplicates, c=rpds, cmap='RdYlGn_r', 
                        s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('RPD (%)', fontsize=12, fontweight='bold')
    
    # Styling
    ax.set_xlabel(f'{element} Original', fontsize=12, fontweight='bold')
    ax.set_ylabel(f'{element} Duplicate', fontsize=12, fontweight='bold')
    ax.set_title(f'Duplicate Precision: {element}', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    # Add statistics
    mean_rpd = np.mean(rpds)
    within_target = sum(1 for rpd in rpds if rpd <= 10) / len(rpds) * 100
    stats_text = f'Mean RPD: {mean_rpd:.2f}%\nWithin ±10%: {within_target:.1f}%\nn = {len(data)}'
    ax.text(0.98, 0.02, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_path


def generate_histogram(
    data: List[float],
    threshold: float,
    title: str,
    xlabel: str,
    output_path: str
) -> str:
    """
    Generate histogram for distribution analysis
    
    Args:
        data: List of values
        threshold: Threshold line to display
        title: Chart title
        xlabel: X-axis label
        output_path: Path to save the chart
    
    Returns:
        Path to saved chart
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create histogram
    n, bins, patches = ax.hist(data, bins=20, color=LOGIQORE_GOLD, alpha=0.7, 
                                edgecolor='black', linewidth=1)
    
    # Color bars based on threshold
    for i, patch in enumerate(patches):
        if bins[i] > threshold:
            patch.set_facecolor('red')
            patch.set_alpha(0.7)
    
    # Threshold line
    ax.axvline(threshold, color='red', linewidth=2, linestyle='--', 
               label=f'Threshold ({threshold})', zorder=3)
    
    # Statistics
    mean_val = np.mean(data)
    median_val = np.median(data)
    ax.axvline(mean_val, color='blue', linewidth=2, linestyle='-', 
               label=f'Mean ({mean_val:.2f})', alpha=0.7)
    ax.axvline(median_val, color='green', linewidth=2, linestyle=':', 
               label=f'Median ({median_val:.2f})', alpha=0.7)
    
    # Styling
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Statistics text box
    exceeds_threshold = sum(1 for val in data if val > threshold) / len(data) * 100
    stats_text = f'Count: {len(data)}\nMean: {mean_val:.2f}\nMedian: {median_val:.2f}\n> Threshold: {exceeds_threshold:.1f}%'
    ax.text(0.98, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_path


if __name__ == '__main__':
    # CLI interface for Node.js to call
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No command provided'}))
        sys.exit(1)
    
    command = sys.argv[1]
    input_data = json.loads(sys.argv[2])
    
    try:
        if command == 'control_chart':
            result = generate_control_chart(
                data=input_data['data'],
                certified_value=input_data['certified_value'],
                element=input_data['element'],
                crm_name=input_data['crm_name'],
                output_path=input_data['output_path']
            )
            print(json.dumps({'success': True, 'path': result}))
        
        elif command == 'scatter_plot':
            result = generate_scatter_plot(
                data=input_data['data'],
                element=input_data['element'],
                output_path=input_data['output_path']
            )
            print(json.dumps({'success': True, 'path': result}))
        
        elif command == 'histogram':
            result = generate_histogram(
                data=input_data['data'],
                threshold=input_data['threshold'],
                title=input_data['title'],
                xlabel=input_data['xlabel'],
                output_path=input_data['output_path']
            )
            print(json.dumps({'success': True, 'path': result}))
        
        else:
            print(json.dumps({'error': f'Unknown command: {command}'}))
            sys.exit(1)
    
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)
