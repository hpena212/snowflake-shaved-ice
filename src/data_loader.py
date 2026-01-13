"""
Data Loading Utilities for Shaved Ice Dataset

This module provides functions to load, validate, and preprocess the Shaved Ice dataset.
Supports both compressed CSV and Parquet formats.
"""

import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path
from typing import Optional, Union
from tqdm import tqdm


def load_shaved_ice_data(
    filepath: Union[str, Path],
    parse_dates: bool = True,
    show_progress: bool = True
) -> pd.DataFrame:
    """
    Load the Shaved Ice dataset from a CSV file (compressed or uncompressed).
    
    Parameters
    ----------
    filepath : str or Path
        Path to the CSV file
    parse_dates : bool, default=True
        Automatically parse datetime columns
    show_progress : bool, default=True
        Show progress bar for large files
        
    Returns
    -------
    pd.DataFrame
        Loaded dataset
        
    Examples
    --------
    >>> df = load_shaved_ice_data('data/raw/shavedice-dataset/demand.csv.gz')
    >>> print(df.head())
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found: {filepath}")
    
    print(f"Loading data from {filepath.name}...")
    
    try:
        # Read CSV with automatic datetime parsing
        df = pd.read_csv(
            filepath,
            parse_dates=['timestamp'] if parse_dates else None,
            compression='infer'  # Automatically detect .gz, .zip, etc.
        )
        
        print(f"✅ Loaded {len(df):,} rows, {len(df.columns)} columns")
        return df
        
    except Exception as e:
        raise ValueError(f"Error loading CSV: {e}")


def load_parquet(filepath: Union[str, Path]) -> pd.DataFrame:
    """
    Load data from a Parquet file.
    
    Parameters
    ----------
    filepath : str or Path
        Path to the Parquet file
        
    Returns
    -------
    pd.DataFrame
        Loaded dataset
        
    Examples
    --------
    >>> df = load_parquet('data/processed/demand_daily.parquet')
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Parquet file not found: {filepath}")
    
    print(f"Loading Parquet from {filepath.name}...")
    
    try:
        df = pd.read_parquet(filepath)
        print(f"✅ Loaded {len(df):,} rows, {len(df.columns)} columns")
        return df
        
    except Exception as e:
        raise ValueError(f"Error loading Parquet: {e}")


def validate_time_range(
    df: pd.DataFrame,
    timestamp_col: str = 'timestamp',
    expected_freq: str = 'H'
) -> dict:
    """
    Validate the time range and check for gaps in the time series.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset with datetime column
    timestamp_col : str, default='timestamp'
        Name of the timestamp column
    expected_freq : str, default='H'
        Expected frequency ('H' for hourly, 'D' for daily)
        
    Returns
    -------
    dict
        Validation results with keys:
        - start_date: First timestamp
        - end_date: Last timestamp
        - total_records: Number of records
        - missing_periods: Number of missing time periods
        - completeness: Percentage of expected records present
        
    Examples
    --------
    >>> validation = validate_time_range(df)
    >>> print(f"Data completeness: {validation['completeness']:.1f}%")
    """
    if timestamp_col not in df.columns:
        raise ValueError(f"Column '{timestamp_col}' not found in DataFrame")
    
    # Ensure timestamp column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    
    # Sort by timestamp
    df_sorted = df.sort_values(timestamp_col)
    
    start_date = df_sorted[timestamp_col].min()
    end_date = df_sorted[timestamp_col].max()
    total_records = len(df_sorted)
    
    # Create expected date range
    expected_range = pd.date_range(start=start_date, end=end_date, freq=expected_freq)
    expected_count = len(expected_range)
    
    # Find missing periods
    actual_timestamps = set(df_sorted[timestamp_col])
    expected_timestamps = set(expected_range)
    missing_timestamps = expected_timestamps - actual_timestamps
    missing_count = len(missing_timestamps)
    
    completeness = (total_records / expected_count) * 100 if expected_count > 0 else 0
    
    results = {
        'start_date': start_date,
        'end_date': end_date,
        'total_records': total_records,
        'expected_records': expected_count,
        'missing_periods': missing_count,
        'completeness': completeness
    }
    
    # Print summary
    print("\n📊 Time Range Validation")
    print(f"   Start: {start_date}")
    print(f"   End: {end_date}")
    print(f"   Total records: {total_records:,}")
    print(f"   Expected records: {expected_count:,}")
    print(f"   Missing periods: {missing_count:,}")
    print(f"   Completeness: {completeness:.2f}%")
    
    if missing_count > 0:
        print(f"   ⚠️  Warning: {missing_count} time periods are missing")
    else:
        print("   ✅ No gaps detected")
    
    return results


def get_sample_data(df: pd.DataFrame, n: int = 1000) -> pd.DataFrame:
    """
    Get a random sample of the dataset for quick exploration.
    
    Parameters
    ----------
    df : pd.DataFrame
        Full dataset
    n : int, default=1000
        Number of rows to sample
        
    Returns
    -------
    pd.DataFrame
        Random sample
    """
    if len(df) <= n:
        return df.copy()
    
    return df.sample(n=n, random_state=42).sort_index()
