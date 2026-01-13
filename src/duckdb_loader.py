"""
DuckDB Integration for Shaved Ice Analysis

This module bridges dbt transformations with Python analysis.
Load the clean data from DuckDB after running dbt models.
"""

import duckdb
import pandas as pd
from pathlib import Path
from typing import Optional


def _find_db_path() -> Path:
    """Find the DuckDB file, checking multiple possible locations."""
    # Try relative paths from different working directories
    possible_paths = [
        Path("data/processed/shaved_ice.duckdb"),           # From project root
        Path("../data/processed/shaved_ice.duckdb"),        # From notebooks/
        Path(__file__).parent.parent / "data/processed/shaved_ice.duckdb",  # From src/
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    # If none found, return the project root version (will fail with helpful error)
    return possible_paths[0]


def get_connection(db_path: Optional[Path] = None) -> duckdb.DuckDBPyConnection:
    """
    Get a connection to the DuckDB database.
    
    Parameters
    ----------
    db_path : Path, optional
        Path to DuckDB file. Auto-detected if not provided.
        
    Returns
    -------
    duckdb.DuckDBPyConnection
        Database connection
    """
    path = db_path or _find_db_path()
    
    if not path.exists():
        raise FileNotFoundError(
            f"DuckDB file not found at {path}. "
            "Did you run 'dbt run --profiles-dir .' first?"
        )
    
    return duckdb.connect(str(path), read_only=True)


def load_mart_data(table_name: str = "mart_forecast_input") -> pd.DataFrame:
    """
    Load cleaned data from a dbt mart table into pandas.
    
    This is your main entry point after running `dbt run`.
    
    Parameters
    ----------
    table_name : str, default="mart_forecast_input"
        Name of the dbt model/table to load
        
    Returns
    -------
    pd.DataFrame
        Clean, analysis-ready data
        
    Examples
    --------
    >>> df = load_mart_data()
    >>> print(f"Loaded {len(df)} days of data")
    """
    con = get_connection()
    
    try:
        df = con.execute(f"SELECT * FROM {table_name}").fetchdf()
        print(f"✅ Loaded {len(df):,} rows from '{table_name}'")
        return df
    except Exception as e:
        raise ValueError(f"Error loading table '{table_name}': {e}")
    finally:
        con.close()


def run_query(query: str) -> pd.DataFrame:
    """
    Run a custom SQL query against the DuckDB database.
    
    Parameters
    ----------
    query : str
        SQL query string
        
    Returns
    -------
    pd.DataFrame
        Query results
        
    Examples
    --------
    >>> df = run_query("SELECT * FROM int_daily_demand LIMIT 10")
    """
    con = get_connection()
    
    try:
        return con.execute(query).fetchdf()
    finally:
        con.close()


def list_tables() -> list:
    """
    List all tables in the DuckDB database.
    
    Returns
    -------
    list
        Table names
    """
    con = get_connection()
    
    try:
        result = con.execute("SHOW TABLES").fetchall()
        return [row[0] for row in result]
    finally:
        con.close()
