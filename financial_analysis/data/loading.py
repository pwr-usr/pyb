"""
Data loading functions for financial analysis.
"""

import pyb
import pandas as pd
from .preprocessing import filter_by_ipo_date, filter_factors_by_first_close


def load_price_data(stock_codes, data_dir="./data/candlestick_data"):
    """
    Load price data for the given stock codes.
    
    Parameters:
    -----------
    stock_codes : list
        List of stock codes to load
    data_dir : str, optional
        Directory containing candlestick data files
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing price data with dates as index and stock codes as columns
    """
    return pyb.get_candlestick_data(symbols=stock_codes, output_format='bt', candlestick_dir=data_dir)


def load_stock_info():
    """
    Load stock information from the data source.
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing stock information
    """
    return pyb.get_stock_info_dataframe()


def get_ah_stocks():
    """
    Get a list of A/H stock codes.
    
    Returns:
    --------
    list
        List of A/H stock codes
    """
    return pyb.get_ah_stock_codes()


def load_and_filter_price_data(stock_codes=None, stock_info_df=None, data_dir="./data/candlestick_data"):
    """
    Load and filter price data for the given stock codes.
    
    Parameters:
    -----------
    stock_codes : list, optional
        List of stock codes to load. If None, uses A/H stock codes.
    stock_info_df : pandas.DataFrame, optional
        DataFrame containing stock information. If None, loads it.
    data_dir : str, optional
        Directory containing candlestick data files
        
    Returns:
    --------
    tuple
        Tuple containing (original_prices, filtered_prices)
    """
    if stock_codes is None:
        stock_codes = get_ah_stocks()
        
    if stock_info_df is None:
        stock_info_df = load_stock_info()
        
    close_df = load_price_data(stock_codes, data_dir)
    close_df_filtered = filter_by_ipo_date(close_df, stock_info_df)
    
    return close_df, close_df_filtered 