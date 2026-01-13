"""
Utility Functions for Data Transformations

Helper functions for common data manipulation tasks.
"""

import pandas as pd
import numpy as np
from typing import List, Optional


def add_time_features(df: pd.DataFrame, timestamp_col: str = 'timestamp') -> pd.DataFrame:
    """
    Add useful time-based features to the dataframe.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset with timestamp column
    timestamp_col : str, default='timestamp'
        Name of the timestamp column
        
    Returns
    -------
    pd.DataFrame
        DataFrame with additional time features:
        - hour: Hour of day (0-23)
        - day_of_week: Day of week (0=Monday, 6=Sunday)
        - day_name: Name of day
        - is_weekend: Boolean for weekend days
        - month: Month number (1-12)
        - year: Year
        
    Examples
    --------
    >>> df_enhanced = add_time_features(df)
    >>> print(df_enhanced[['timestamp', 'hour', 'is_weekend']].head())
    """
    df = df.copy()
    
    # Ensure timestamp is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    
    # Extract time features
    df['hour'] = df[timestamp_col].dt.hour
    df['day_of_week'] = df[timestamp_col].dt.dayofweek
    df['day_name'] = df[timestamp_col].dt.day_name()
    df['is_weekend'] = df['day_of_week'].isin([5, 6])
    df['month'] = df[timestamp_col].dt.month
    df['year'] = df[timestamp_col].dt.year
    df['date'] = df[timestamp_col].dt.date
    
    return df


def aggregate_to_daily(
    df: pd.DataFrame,
    timestamp_col: str = 'timestamp',
    value_col: str = 'demand',
    agg_func: str = 'sum'
) -> pd.DataFrame:
    """
    Aggregate hourly data to daily granularity.
    
    Parameters
    ----------
    df : pd.DataFrame
        Hourly dataset
    timestamp_col : str, default='timestamp'
        Timestamp column name
    value_col : str, default='demand'
        Value column to aggregate
    agg_func : str, default='sum'
        Aggregation function ('sum', 'mean', 'max', 'min')
        
    Returns
    -------
    pd.DataFrame
        Daily aggregated data
        
    Examples
    --------
    >>> # Get total daily demand
    >>> daily_df = aggregate_to_daily(hourly_df, agg_func='sum')
    """
    df = df.copy()
    
    # Ensure timestamp is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    
    # Create date column
    df['date'] = df[timestamp_col].dt.date
    
    # Aggregate
    daily_df = df.groupby('date')[value_col].agg(agg_func).reset_index()
    daily_df.rename(columns={value_col: f'{value_col}_daily_{agg_func}'}, inplace=True)
    
    return daily_df


def detect_outliers_iqr(
    series: pd.Series,
    multiplier: float = 1.5
) -> pd.Series:
    """
    Detect outliers using Interquartile Range (IQR) method.
    
    Parameters
    ----------
    series : pd.Series
        Data series
    multiplier : float, default=1.5
        IQR multiplier (1.5 is standard, 3.0 is more conservative)
        
    Returns
    -------
    pd.Series
        Boolean series where True indicates an outlier
        
    Examples
    --------
    >>> outliers = detect_outliers_iqr(df['demand'])
    >>> print(f"Found {outliers.sum()} outliers")
    >>> df_clean = df[~outliers]
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    is_outlier = (series < lower_bound) | (series > upper_bound)
    
    return is_outlier


def fill_missing_timestamps(
    df: pd.DataFrame,
    timestamp_col: str = 'timestamp',
    freq: str = 'H',
    fill_method: str = 'ffill'
) -> pd.DataFrame:
    """
    Fill in missing timestamps with a specified frequency.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset with potential gaps
    timestamp_col : str, default='timestamp'
        Timestamp column name
    freq : str, default='H'
        Frequency to fill ('H' for hourly, 'D' for daily)
    fill_method : str, default='ffill'
        Method to fill missing values ('ffill', 'bfill', or 'interpolate')
        
    Returns
    -------
    pd.DataFrame
        DataFrame with continuous timestamp range
        
    Examples
    --------
    >>> # Fill missing hours with forward-fill
    >>> df_complete = fill_missing_timestamps(df, freq='H', fill_method='ffill')
    """
    df = df.copy()
    
    # Ensure timestamp is datetime and set as index
    if not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    
    df = df.set_index(timestamp_col)
    
    # Create complete date range
    idx = pd.date_range(start=df.index.min(), end=df.index.max(), freq=freq)
    
    # Reindex to include missing timestamps
    df = df.reindex(idx)
    
    # Fill missing values
    if fill_method == 'ffill':
        df = df.fillna(method='ffill')
    elif fill_method == 'bfill':
        df = df.fillna(method='bfill')
    elif fill_method == 'interpolate':
        df = df.interpolate()
    
    # Reset index
    df = df.reset_index()
    df.rename(columns={'index': timestamp_col}, inplace=True)
    
    return df


def create_lag_features(
    df: pd.DataFrame,
    value_col: str,
    lags: List[int]
) -> pd.DataFrame:
    """
    Create lagged features for time series modeling.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset
    value_col : str
        Column to create lags for
    lags : list of int
        List of lag periods (e.g., [1, 24, 168] for 1 hour, 1 day, 1 week)
        
    Returns
    -------
    pd.DataFrame
        DataFrame with additional lag columns
        
    Examples
    --------
    >>> # Create 1-hour and 24-hour lag features
    >>> df_with_lags = create_lag_features(df, 'demand', lags=[1, 24])
    """
    df = df.copy()
    
    for lag in lags:
        df[f'{value_col}_lag_{lag}'] = df[value_col].shift(lag)
    
    return df

# ---------------------------------------------------------------------------
# Additional Feature‑Engineering Helper Functions
# ---------------------------------------------------------------------------

def rolling_mean(series: pd.Series, window: int = 7, min_periods: int = 1) -> pd.Series:
    """Calculate a rolling (moving) mean.

    Parameters
    ----------
    series : pd.Series
        The numeric series to smooth.
    window : int, default=7
        Number of periods to include in the moving window.
    min_periods : int, default=1
        Minimum number of observations required to compute a value.

    Returns
    -------
    pd.Series
        The rolling‑mean series, aligned with the original index.
    """
    return series.rolling(window=window, min_periods=min_periods).mean()


def encode_categorical(df: pd.DataFrame, columns: List[str], drop_original: bool = False) -> pd.DataFrame:
    """One‑hot encode categorical columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    columns : list of str
        Column names to encode.
    drop_original : bool, default=False
        Whether to drop the original categorical columns after encoding.

    Returns
    -------
    pd.DataFrame
        DataFrame with new one‑hot columns (``col__value``) added.
    """
    df = df.copy()
    for col in columns:
        # pandas.get_dummies creates a column for each category value
        dummies = pd.get_dummies(df[col], prefix=col, dtype=int)
        df = pd.concat([df, dummies], axis=1)
        if drop_original:
            df.drop(columns=[col], inplace=True)
    return df


def scale_numeric(df: pd.DataFrame, columns: List[str], method: str = "standard") -> pd.DataFrame:
    """Scale numeric columns using a simple scaler.

    Supported methods:
    - "standard": (x - mean) / std
    - "minmax": (x - min) / (max - min)

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    columns : list of str
        Numeric columns to scale.
    method : str, default="standard"
        Scaling technique.

    Returns
    -------
    pd.DataFrame
        DataFrame with scaled columns (original column names are overwritten).
    """
    df = df.copy()
    for col in columns:
        if method == "standard":
            mean = df[col].mean()
            std = df[col].std()
            df[col] = (df[col] - mean) / std if std != 0 else 0.0
        elif method == "minmax":
            min_val = df[col].min()
            max_val = df[col].max()
            range_val = max_val - min_val
            df[col] = (df[col] - min_val) / range_val if range_val != 0 else 0.0
        else:
            raise ValueError(f"Unsupported scaling method: {method}")
    return df

# ---------------------------------------------------------------------------
# Data Inspection and Miscellaneous Helpers
# ---------------------------------------------------------------------------

def data_audit(df: pd.DataFrame, title: str = "DATA AUDIT") -> None:
    """
    Perform a quick audit of the dataframe (prints to stdout).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to audit.
    title : str, default='DATA AUDIT'
        Header for the audit output.
    """
    print(f"=== {title} ===")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    
    print("\n--- Info ---")
    df.info()

    if 'date' in df.columns:
        print("\n--- Time Range ---")
        print(f"Start: {df['date'].min()}")
        print(f"End:   {df['date'].max()}")

    # Preview unique values for categorical/id columns
    id_cols = [col for col in df.columns if 'id' in col.lower() or 'type' in col.lower() or 'region' in col.lower()]
    if id_cols:
        print("\n--- Categorical/ID Previews ---")
        for col in id_cols:
            unique_vals = df[col].unique()
            if len(unique_vals) <= 15:
                print(f"{col}: {unique_vals}")
            else:
                print(f"{col}: {len(unique_vals)} unique values")
    print("================\n")
