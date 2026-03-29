"""
Loader module for Evidence Pack Assembler.

Handles loading and basic validation of CSV data files.
"""

import csv

def load_csv(file_path: str, required_columns: list) -> list:
    """
    Load data from a CSV file and validate required columns.
    
    Args:
        file_path: Path to the CSV file
        required_columns: List of column names that must be present
        
    Returns:
        List of dictionaries representing the CSV rows
        
    Raises:
        ValueError: If required columns are missing or file cannot be read
    """
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            
        # Validate required columns
        if not all(col in reader.fieldnames for col in required_columns):
            missing = [col for col in required_columns if col not in reader.fieldnames]
            raise ValueError(f"Missing required columns in {file_path}: {missing}")
            
        return data
        
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error reading {file_path}: {str(e)}")