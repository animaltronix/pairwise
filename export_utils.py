"""
Export utilities for pairwise testing results.

Supports exporting test cases to Excel (.xlsx) and CSV formats.
"""

import pandas as pd
from typing import List, Dict
import os


def export_to_excel(test_cases: List[Dict[str, str]], filename: str = "pairwise_test_cases.xlsx") -> str:
    """
    Export test cases to Excel format.
    
    Args:
        test_cases: List of test case dictionaries
        filename: Output filename
        
    Returns:
        Path to the exported file
        
    Raises:
        Exception: If export fails
    """
    try:
        # Convert test cases to DataFrame
        df = pd.DataFrame(test_cases)
        
        # Add test case number column
        df.insert(0, 'Test Case #', range(1, len(df) + 1))
        
        # Export to Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        
        return os.path.abspath(filename)
    
    except Exception as e:
        raise Exception(f"Failed to export to Excel: {str(e)}")


def export_to_csv(test_cases: List[Dict[str, str]], filename: str = "pairwise_test_cases.csv") -> str:
    """
    Export test cases to CSV format.
    
    Args:
        test_cases: List of test case dictionaries
        filename: Output filename
        
    Returns:
        Path to the exported file
        
    Raises:
        Exception: If export fails
    """
    try:
        # Convert test cases to DataFrame
        df = pd.DataFrame(test_cases)
        
        # Add test case number column
        df.insert(0, 'Test Case #', range(1, len(df) + 1))
        
        # Export to CSV
        df.to_csv(filename, index=False)
        
        return os.path.abspath(filename)
    
    except Exception as e:
        raise Exception(f"Failed to export to CSV: {str(e)}")


def get_export_summary(test_cases: List[Dict[str, str]]) -> Dict:
    """
    Get summary statistics for test cases.
    
    Args:
        test_cases: List of test case dictionaries
        
    Returns:
        Dictionary with summary information
    """
    if not test_cases:
        return {
            'total_test_cases': 0,
            'parameters': 0,
            'average_values_per_parameter': 0
        }
    
    # Count parameters
    parameters = list(test_cases[0].keys())
    
    # Calculate average values per parameter
    total_values = sum(len(set(test_case[param] for test_case in test_cases)) for param in parameters)
    avg_values = total_values / len(parameters) if parameters else 0
    
    return {
        'total_test_cases': len(test_cases),
        'parameters': len(parameters),
        'average_values_per_parameter': round(avg_values, 2)
    } 