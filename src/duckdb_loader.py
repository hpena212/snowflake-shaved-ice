"""
DuckDB Integration for Shaved Ice Analysis

This module bridges dbt transformations with Python analysis.
Load the clean data from DuckDB after running dbt models.
"""

import duckdb
import pandas as pd
from pathlib import Path
from typing import Optional


# Default database path (set by dbt profile)
DEFAULT_DB_PATH = Path("data/processed/shaved_ice.duckdb")


def get_connection(db_path: Optional[Path] = None) -> duckdb.DuckDBPyConnection:
    """
    Get a connection to the DuckDB database.
    
    Parameters
    ----------
    db_path : Path, optional
        Path to DuckDB file. Defaults to data/processed/shaved_ice.duckdb
        
    Returns
    -------
    duckdb.DuckDBPyConnection
        Database connection
    """
    path = db_path or DEFAULT_DB_PATH
    return duckdb.connect(str(path))


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
    >>> # After running: dbt run
    >>> df = load_mart_data()
    >>> print(f"Loaded {len(df)} days of data")
    >>> df.head()
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
        
    Examples
    --------
    >>> tables = list_tables()
    >>> print(tables)
    ['stg_shaved_ice', 'int_daily_demand', 'mart_forecast_input']
    """
    con = get_connection()
    
    try:
        result = con.execute("SHOW TABLES").fetchall()
        return [row[0] for row in result]
    finally:
        con.close()


def get_table_info(table_name: str) -> pd.DataFrame:
    """
    Get column information for a table.
    
    Parameters
    ----------
    table_name : str
        Name of table
        
    Returns
    -------
    pd.DataFrame
        Column names and types
    """
    con = get_connection()
    
    try:
        return con.execute(f"DESCRIBE {table_name}").fetchdf()
    finally:
        con.close()
