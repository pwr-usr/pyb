"""
Analysis and visualization functions for financial data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def compare_strategies_performance(results, figsize=(14, 8), title='Strategy Performance Comparison'):
    """
    Plot a comparison of strategy performances.
    
    Parameters:
    -----------
    results : dict
        Dictionary of strategy results {name: result}
    figsize : tuple, optional
        Figure size
    title : str, optional
        Plot title
        
    Returns:
    --------
    matplotlib.figure.Figure
        Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for name, result in results.items():
        result.plot(ax=ax)
    
    plt.title(title)
    plt.legend()
    
    return fig


def display_strategy_stats(results):
    """
    Display performance statistics for multiple strategies.
    
    Parameters:
    -----------
    results : dict
        Dictionary of strategy results {name: result}
    """
    for name, result in results.items():
        print(f"=== {name} Performance ===")
        result.display()
        print("\n")


def analyze_sector_performance(strategy_result, stocks_info):
    """
    Analyze sector allocation and performance for a strategy.
    
    Parameters:
    -----------
    strategy_result : bt.backtest.Result
        Result from running a backtest
    stocks_info : pandas.DataFrame
        DataFrame containing stock information including sector data
        
    Returns:
    --------
    pandas.DataFrame
        Sector analysis DataFrame
    """
    # Get latest weights
    latest_weights = strategy_result.weights.iloc[-1]
    
    # Get sectors for each stock
    sectors = {}
    for stock in latest_weights.index:
        if stock in stocks_info['stockCode'].values:
            sector = stocks_info.loc[stocks_info['stockCode'] == stock, 'sector'].iloc[0]
            sectors[stock] = sector
    
    # Create DataFrame with stock weights and sectors
    sector_df = pd.DataFrame({
        'stock': latest_weights.index,
        'weight': latest_weights.values,
        'sector': [sectors.get(stock, 'Unknown') for stock in latest_weights.index]
    })
    
    # Group by sector and sum weights
    sector_weights = sector_df.groupby('sector')['weight'].sum().sort_values(ascending=False)
    
    return sector_weights


def plot_sector_allocation(sector_weights, title='Sector Allocation', figsize=(10, 6)):
    """
    Plot sector allocation.
    
    Parameters:
    -----------
    sector_weights : pandas.DataFrame
        Sector weights DataFrame
    title : str, optional
        Plot title
    figsize : tuple, optional
        Figure size
        
    Returns:
    --------
    matplotlib.figure.Figure
        Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    sector_weights.plot(kind='bar', ax=ax, title=title)
    plt.tight_layout()
    
    return fig


def plot_sector_comparisons(sector_weights_dict, figsize=(16, 12)):
    """
    Plot sector allocation comparison for multiple strategies.
    
    Parameters:
    -----------
    sector_weights_dict : dict
        Dictionary of sector weights {name: sector_weights}
    figsize : tuple, optional
        Figure size
        
    Returns:
    --------
    matplotlib.figure.Figure
        Figure object
    """
    num_strategies = len(sector_weights_dict)
    if num_strategies <= 2:
        num_rows, num_cols = 1, num_strategies
    else:
        num_rows = (num_strategies + 1) // 2
        num_cols = 2
    
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    
    if num_strategies == 1:
        axes = [axes]
    
    for i, (name, sector_weights) in enumerate(sector_weights_dict.items()):
        if num_rows > 1:
            row, col = i // num_cols, i % num_cols
            ax = axes[row, col]
        else:
            ax = axes[i]
            
        sector_weights.plot(kind='bar', ax=ax, title=f'{name} - Sector Allocation')
    
    plt.tight_layout()
    
    return fig


def analyze_strategy_holdings(strategy_result, date=None):
    """
    Analyze strategy holdings at a specific date.
    
    Parameters:
    -----------
    strategy_result : bt.backtest.Result
        Result from running a backtest
    date : str or pd.Timestamp, optional
        Date to analyze holdings. If None, uses the last date.
        
    Returns:
    --------
    pandas.DataFrame
        Holdings analysis DataFrame
    """
    if date is None:
        date = strategy_result.positions.index[-1]
    
    # Get positions at date
    positions = strategy_result.positions.loc[date]
    
    # Get weights at date
    weights = strategy_result.weights.loc[date]
    
    # Create DataFrame with positions and weights
    holdings_df = pd.DataFrame({
        'stock': positions.index,
        'position': positions.values,
        'weight': weights.values
    })
    
    # Filter out zero positions
    holdings_df = holdings_df[holdings_df['position'] > 0]
    
    # Sort by weight (descending)
    holdings_df = holdings_df.sort_values('weight', ascending=False)
    
    return holdings_df


def plot_rolling_returns(results, window=20, figsize=(14, 8), title='Rolling Returns'):
    """
    Plot rolling returns for strategies.
    
    Parameters:
    -----------
    results : dict
        Dictionary of strategy results {name: result}
    window : int, optional
        Rolling window size in days
    figsize : tuple, optional
        Figure size
    title : str, optional
        Plot title
        
    Returns:
    --------
    matplotlib.figure.Figure
        Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for name, result in results.items():
        # Get returns
        returns = result.returns
        # Calculate rolling returns
        rolling_returns = returns.rolling(window).mean() * 252  # Annualize
        rolling_returns.plot(ax=ax, label=name)
    
    plt.title(title)
    plt.legend()
    
    return fig


def plot_drawdowns(results, figsize=(14, 8), title='Drawdowns'):
    """
    Plot drawdowns for strategies.
    
    Parameters:
    -----------
    results : dict
        Dictionary of strategy results {name: result}
    figsize : tuple, optional
        Figure size
    title : str, optional
        Plot title
        
    Returns:
    --------
    matplotlib.figure.Figure
        Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for name, result in results.items():
        # Get equity curve
        equity = result.prices
        # Calculate drawdowns
        drawdowns = equity / equity.cummax() - 1
        drawdowns.plot(ax=ax, label=name)
    
    plt.title(title)
    plt.legend()
    
    return fig 