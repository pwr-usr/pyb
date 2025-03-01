"""
Data preprocessing functions for financial analysis.
"""

import pandas as pd
import numpy as np


def filter_by_ipo_date(candlestick_df: pd.DataFrame, stock_info_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters out (sets to NaN) all close prices in candlestick_df that occur before the IPO date of each stock.
    Afterwards, forward fills missing prices using the previous valid value along the date index.
    
    Parameters:
        candlestick_df (pd.DataFrame): A pivot table with dates as the index and stock codes as columns.
        stock_info_df (pd.DataFrame): A DataFrame containing stock information, including 'stockCode' and 'ipoDate'.
        
    Returns:
        pd.DataFrame: A new DataFrame where prices dated before the IPO date for each stock have been removed,
                      and missing prices are forward filled with the last valid price.
    """
    # Create a copy to avoid modifying the original DataFrame
    filtered_df = candlestick_df.copy()
    
    # Ensure that the 'ipoDate' column is in datetime format
    stock_info_df = stock_info_df.copy()  # avoid modifying the original stock_info_df
    stock_info_df['ipoDate'] = pd.to_datetime(stock_info_df['ipoDate'])
    
    # Iterate over each stock (column) in the candlestick DataFrame
    for stock in filtered_df.columns:
        # Check if the stock code exists in the stock_info DataFrame
        if stock in stock_info_df['stockCode'].values:
            # Get the IPO date for this stock
            ipo_date = stock_info_df.loc[stock_info_df['stockCode'] == stock, 'ipoDate'].iloc[0]
            # Set all prices before the IPO date to NaN
            filtered_df.loc[filtered_df.index < ipo_date, stock] = np.nan

    # Forward fill the prices along the date index (assumes the index is sorted chronologically)
    filtered_df = filtered_df.fillna(method='ffill')
    
    return filtered_df


def filter_factors_by_first_close(close_df, factor_df):
    """
    Filter factor DataFrame by setting values to NaN for dates before first close price exists.
    
    Parameters:
    -----------
    close_df : pandas.DataFrame
        DataFrame containing close prices with stock codes as columns and dates as index
    factor_df : pandas.DataFrame
        DataFrame containing factor values with same structure as close_df
    
    Returns:
    --------
    pandas.DataFrame
        Filtered factor DataFrame with values set to NaN before first close date for each stock
    """
    # Create a copy of factor_df to avoid modifying the original
    filtered_factor_df = factor_df.copy()
    
    # Get the first non-NaN date for each stock in close_df
    first_close_dates = {}
    for column in close_df.columns:
        if column in factor_df.columns:  # Only process columns that exist in both DataFrames
            non_nan_idx = close_df[column].first_valid_index()
            if non_nan_idx is not None:
                first_close_dates[column] = non_nan_idx
    
    # Filter factor_df based on first close dates
    for stock_code, first_date in first_close_dates.items():
        # Get all dates before the first close price date
        mask = factor_df.index < first_date
        # Set those values to NaN
        filtered_factor_df.loc[mask, stock_code] = np.nan
    
    return filtered_factor_df 