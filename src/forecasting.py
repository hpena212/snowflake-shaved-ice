"""
Time Series Forecasting Utilities

Simple, explainable forecasting models for VM demand prediction.
Focuses on moving averages and percentile-based approaches.
"""

import pandas as pd
import numpy as np
from typing import Union, Tuple


def moving_average_forecast(
    series: pd.Series,
    window: int = 24,
    forecast_horizon: int = 1
) -> pd.Series:
    """
    Generate forecasts using simple moving average.
    
    Parameters
    ----------
    series : pd.Series
        Time series data
    window : int, default=24
        Number of periods to average (24 = 24 hours for hourly data)
    forecast_horizon : int, default=1
        Number of periods ahead to forecast
        
    Returns
    -------
    pd.Series
        Forecasted values
        
    Examples
    --------
    >>> forecast = moving_average_forecast(demand_series, window=168)  # 1 week
    """
    return series.rolling(window=window, min_periods=1).mean().shift(forecast_horizon)


def weighted_moving_average(
    series: pd.Series,
    window: int = 24,
    alpha: float = 0.3
) -> pd.Series:
    """
    Exponentially weighted moving average forecast.
    
    Parameters
    ----------
    series : pd.Series
        Time series data
    window : int, default=24
        Span for exponential weighting
    alpha : float, default=0.3
        Smoothing parameter (0 < alpha < 1)
        Higher values give more weight to recent observations
        
    Returns
    -------
    pd.Series
        Forecasted values
    """
    return series.ewm(span=window, adjust=False).mean()


def calculate_safety_stock(
    actual: pd.Series,
    forecast: pd.Series,
    percentile: float = 95.0
) -> float:
    """
    Calculate safety stock level based on forecast errors.
    
    Safety stock helps prevent stockouts by accounting for demand variability.
    
    Parameters
    ----------
    actual : pd.Series
        Actual observed demand
    forecast : pd.Series
        Forecasted demand
    percentile : float, default=95.0
        Percentile for safety stock (e.g., 95 = cover 95% of scenarios)
        
    Returns
    -------
    float
        Recommended safety stock level
        
    Examples
    --------
    >>> safety = calculate_safety_stock(actual_demand, forecasted_demand, percentile=99)
    >>> print(f"Recommended safety stock: {safety:.0f} VMs")
    """
    # Calculate forecast errors (actuals - forecast)
    errors = actual - forecast
    
    # Remove NaN values
    errors = errors.dropna()
    
    if len(errors) == 0:
        return 0.0
    
    # Use percentile of positive errors (under-forecasting)
    positive_errors = errors[errors > 0]
    
    if len(positive_errors) == 0:
        return 0.0
    
    safety_stock = np.percentile(positive_errors, percentile)
    
    return max(0, safety_stock)


def forecast_accuracy_metrics(
    actual: pd.Series,
    forecast: pd.Series
) -> dict:
    """
    Calculate forecast accuracy metrics.
    
    Parameters
    ----------
    actual : pd.Series
        Actual observed values
    forecast : pd.Series
        Forecasted values
        
    Returns
    -------
    dict
        Dictionary containing:
        - mae: Mean Absolute Error
        - rmse: Root Mean Squared Error
        - mape: Mean Absolute Percentage Error
        - bias: Average forecast bias (positive = over-forecasting)
        
    Examples
    --------
    >>> metrics = forecast_accuracy_metrics(actual_demand, my_forecast)
    >>> print(f"MAPE: {metrics['mape']:.2f}%")
    """
    # Align the series and remove NaN
    df = pd.DataFrame({'actual': actual, 'forecast': forecast}).dropna()
    
    if len(df) == 0:
        return {'mae': np.nan, 'rmse': np.nan, 'mape': np.nan, 'bias': np.nan}
    
    actual = df['actual']
    forecast = df['forecast']
    
    # Calculate errors
    errors = actual - forecast
    abs_errors = np.abs(errors)
    squared_errors = errors ** 2
    
    # Calculate metrics
    mae = abs_errors.mean()
    rmse = np.sqrt(squared_errors.mean())
    
    # MAPE (avoid division by zero)
    mask = actual != 0
    mape = (abs_errors[mask] / np.abs(actual[mask])).mean() * 100 if mask.sum() > 0 else np.nan
    
    bias = errors.mean()
    
    return {
        'mae': mae,
        'rmse': rmse,
        'mape': mape,
        'bias': bias,
        'n_samples': len(df)
    }


def seasonal_naive_forecast(
    series: pd.Series,
    seasonal_period: int = 24
) -> pd.Series:
    """
    Naive seasonal forecast: use the value from the same time in the previous cycle.
    
    Parameters
    ----------
    series : pd.Series
        Time series data
    seasonal_period : int, default=24
        Length of seasonal cycle (24 hours for daily seasonality in hourly data)
        
    Returns
    -------
    pd.Series
        Forecasted values
        
    Examples
    --------
    >>> # For hourly data, use yesterday's value at the same hour
    >>> forecast = seasonal_naive_forecast(demand, seasonal_period=24)
    """
    return series.shift(seasonal_period)


def compute_percentile_forecast(
    df: pd.DataFrame,
    value_col: str,
    groupby_cols: list,
    percentile: float = 50.0
) -> pd.DataFrame:
    """
    Compute percentile-based forecasts grouped by categorical variables.
    
    Useful for creating forecasts based on historical patterns for specific
    regions, instance types, etc.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset with historical data
    value_col : str
        Column name containing the values to forecast
    groupby_cols : list
        Columns to group by (e.g., ['region', 'hour_of_day'])
    percentile : float, default=50.0
        Percentile to use for forecast (50 = median)
        
    Returns
    -------
    pd.DataFrame
        DataFrame with group keys and forecasted values
        
    Examples
    --------
    >>> # Forecast based on median demand for each region and hour
    >>> forecast_df = compute_percentile_forecast(
    ...     df, value_col='demand', 
    ...     groupby_cols=['region', 'hour'],
    ...     percentile=75
    ... )
    """
    forecast = df.groupby(groupby_cols)[value_col].quantile(percentile / 100.0).reset_index()
    forecast.rename(columns={value_col: f'{value_col}_p{int(percentile)}'}, inplace=True)
    
    return forecast
