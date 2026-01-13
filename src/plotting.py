"""
Plotting Utilities for Publication-Ready Figures

Consistent styling for charts to be included in the ICPE 2026 paper.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, Tuple


def setup_plot_style():
    """
    Configure matplotlib and seaborn for publication-quality plots.
    Call this once at the start of your analysis.
    """
    # Set seaborn style
    sns.set_style('whitegrid')
    
    # Configure matplotlib defaults
    plt.rcParams.update({
        'figure.figsize': (12, 6),
        'figure.dpi': 100,
        'savefig.dpi': 300,
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16
    })
    
    print("✅ Plot style configured for publication")


def plot_timeseries(
    df: pd.DataFrame,
    timestamp_col: str,
    value_col: str,
    title: str,
    ylabel: str = "Demand",
    figsize: Tuple[int, int] = (12, 6),
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Plot a simple time series.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data to plot
    timestamp_col : str
        Name of timestamp column
    value_col : str
        Name of value column to plot
    title : str
        Plot title
    ylabel : str, default="Demand"
        Y-axis label
    figsize : tuple, default=(12, 6)
        Figure size in inches
    save_path : str, optional
        Path to save figure (e.g., 'figures/demand_over_time.png')
        
    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(df[timestamp_col], df[value_col], linewidth=1.5, color='#2E86AB')
    ax.set_xlabel('Time')
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved figure to {save_path}")
    
    return fig


def plot_forecast_comparison(
    df: pd.DataFrame,
    timestamp_col: str,
    actual_col: str,
    forecast_col: str,
    title: str = "Forecast vs Actual",
    figsize: Tuple[int, int] = (12, 6),
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Plot actual vs forecasted values.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data containing actual and forecast values
    timestamp_col : str
        Timestamp column name
    actual_col : str
        Actual values column name
    forecast_col : str
        Forecast values column name
    title : str, default="Forecast vs Actual"
        Plot title
    figsize : tuple, default=(12, 6)
        Figure size
    save_path : str, optional
        Path to save figure
        
    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(df[timestamp_col], df[actual_col], 
            label='Actual', linewidth=2, color='#2E86AB', alpha=0.8)
    ax.plot(df[timestamp_col], df[forecast_col], 
            label='Forecast', linewidth=2, color='#F24236', linestyle='--', alpha=0.8)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Demand')
    ax.set_title(title, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved figure to {save_path}")
    
    return fig


def plot_distribution(
    series: pd.Series,
    title: str,
    xlabel: str,
    bins: int = 50,
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Plot histogram with KDE overlay.
    
    Parameters
    ----------
    series : pd.Series
        Data to plot
    title : str
        Plot title
    xlabel : str
        X-axis label
    bins : int, default=50
        Number of histogram bins
    figsize : tuple, default=(10, 6)
        Figure size
    save_path : str, optional
        Path to save figure
        
    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot histogram
    ax.hist(series.dropna(), bins=bins, alpha=0.6, color='#2E86AB', edgecolor='black')
    
    # Add KDE
    series.dropna().plot(kind='kde', ax=ax, secondary_y=True, linewidth=2, color='#F24236')
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Frequency')
    ax.set_title(title, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved figure to {save_path}")
    
    return fig


def plot_grouped_bars(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    group_col: Optional[str] = None,
    title: str = "Comparison",
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create grouped bar chart.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data to plot
    x_col : str
        Column for x-axis categories
    y_col : str
        Column for y-axis values
    group_col : str, optional
        Column for grouping bars
    title : str, default="Comparison"
        Plot title
    figsize : tuple, default=(10, 6)
        Figure size
    save_path : str, optional
        Path to save figure
        
    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if group_col:
        df_pivot = df.pivot(index=x_col, columns=group_col, values=y_col)
        df_pivot.plot(kind='bar', ax=ax, width=0.8)
    else:
        df.plot(x=x_col, y=y_col, kind='bar', ax=ax, legend=False)
    
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved figure to {save_path}")
    
    return fig
