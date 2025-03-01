"""
Financial ratio functions for loading and processing ratio data.
"""

import pyb
import pandas as pd
import numpy as np
from financial_analysis.data.preprocessing import filter_factors_by_first_close


class RatioLoader:
    """Base class for loading and preparing financial ratios."""
    
    def __init__(self, ratio_name):
        """
        Initialize with the ratio name.
        
        Parameters:
        -----------
        ratio_name : str
            Name of the financial ratio
        """
        self.ratio_name = ratio_name
    
    def load_ratio(self, stock_codes):
        """
        Load ratio data for the given stock codes.
        
        Parameters:
        -----------
        stock_codes : list
            List of stock codes to load
            
        Returns:
        --------
        pandas.DataFrame
            DataFrame containing ratio data
        """
        ratio_df = pyb.get_fundamental_data(symbols=stock_codes, ratio=self.ratio_name, output_format='bt')
        return ratio_df
    
    def prepare_ratio_for_analysis(self, ratio_df, close_df_filtered):
        """
        Prepare ratio data for analysis.
        
        Parameters:
        -----------
        ratio_df : pandas.DataFrame
            DataFrame containing ratio data
        close_df_filtered : pandas.DataFrame
            Filtered DataFrame containing close price data
            
        Returns:
        --------
        pandas.DataFrame
            Filtered ratio DataFrame
        """
        return filter_factors_by_first_close(close_df_filtered, ratio_df)


class PriceToBookRatio(RatioLoader):
    """Class for loading and processing Price-to-Book ratios."""
    
    def __init__(self):
        """Initialize with the PB ratio name."""
        super().__init__('pb')


class PriceToEarningsRatio(RatioLoader):
    """Class for loading and processing Price-to-Earnings ratios."""
    
    def __init__(self):
        """Initialize with the PE ratio name."""
        super().__init__('pe_ttm')


class DividendYieldRatio(RatioLoader):
    """Class for loading and processing Dividend Yield ratios."""
    
    def __init__(self):
        """Initialize with the dividend yield ratio name."""
        super().__init__('dyr')


class MarketCapitalization(RatioLoader):
    """Class for loading and processing Market Capitalization data."""
    
    def __init__(self):
        """Initialize with the market cap ratio name."""
        super().__init__('mc')


def create_combined_ratio(ratio_dfs, weights):
    """
    Create a combined ratio from multiple financial ratios with given weights.
    
    Parameters:
    -----------
    ratio_dfs : list of pandas.DataFrame
        List of DataFrames containing different financial ratios
    weights : list of float
        Weights to apply to each ratio, must sum to 1.0
        
    Returns:
    --------
    pandas.DataFrame
        Combined ratio DataFrame
    """
    if len(ratio_dfs) != len(weights):
        raise ValueError("Number of ratio DataFrames must match number of weights")
        
    if abs(sum(weights) - 1.0) > 0.0001:
        raise ValueError("Weights must sum to 1.0")
    
    # Normalize each ratio DataFrame
    normalized_dfs = []
    for df in ratio_dfs:
        # Simple min-max normalization across all stocks for each date
        df_normalized = df.copy()
        for date in df.index:
            row = df.loc[date]
            if not row.isna().all():
                min_val = row.min(skipna=True)
                max_val = row.max(skipna=True)
                if max_val > min_val:  # Avoid division by zero
                    df_normalized.loc[date] = (row - min_val) / (max_val - min_val)
        normalized_dfs.append(df_normalized)
    
    # Combine normalized ratios with weights
    combined_df = pd.DataFrame(index=ratio_dfs[0].index, columns=ratio_dfs[0].columns)
    for i, df in enumerate(normalized_dfs):
        combined_df = combined_df.fillna(0) + df.fillna(0) * weights[i]
    
    return combined_df


# Helper functions for common ratio operations
def load_and_prepare_ratios(stock_codes, close_df_filtered):
    """
    Load and prepare all common financial ratios.
    
    Parameters:
    -----------
    stock_codes : list
        List of stock codes to load
    close_df_filtered : pandas.DataFrame
        Filtered DataFrame containing close price data
        
    Returns:
    --------
    dict
        Dictionary containing filtered ratio DataFrames
    """
    # Initialize ratio loaders
    pb_loader = PriceToBookRatio()
    pe_loader = PriceToEarningsRatio()
    dyr_loader = DividendYieldRatio()
    mc_loader = MarketCapitalization()
    
    # Load ratio data
    pb_df = pb_loader.load_ratio(stock_codes)
    pe_df = pe_loader.load_ratio(stock_codes)
    dyr_df = dyr_loader.load_ratio(stock_codes)
    mc_df = mc_loader.load_ratio(stock_codes)
    
    # Prepare ratio data for analysis
    pb_df_filtered = pb_loader.prepare_ratio_for_analysis(pb_df, close_df_filtered)
    pe_df_filtered = pe_loader.prepare_ratio_for_analysis(pe_df, close_df_filtered)
    dyr_df_filtered = dyr_loader.prepare_ratio_for_analysis(dyr_df, close_df_filtered)
    mc_df_filtered = mc_loader.prepare_ratio_for_analysis(mc_df, close_df_filtered)
    
    return {
        'pb': pb_df_filtered,
        'pe': pe_df_filtered,
        'dividend_yield': dyr_df_filtered,
        'market_cap': mc_df_filtered
    }


def create_value_composite(ratios, weights=None):
    """
    Create a value composite from PB, PE, and Dividend Yield ratios.
    
    Parameters:
    -----------
    ratios : dict
        Dictionary containing filtered ratio DataFrames
    weights : dict, optional
        Dictionary containing weights for each ratio
        
    Returns:
    --------
    pandas.DataFrame
        Combined value ratio DataFrame
    """
    if weights is None:
        weights = {'pb': 0.4, 'pe': 0.4, 'dividend_yield': 0.2}
        
    # For PB and PE lower is better, for dividend higher is better
    # So we'll invert the dividend ratio when normalizing
    inverted_dyr_df = ratios['dividend_yield'] * -1
    
    # Create combined ratio with specified weights
    combined_value_ratio = create_combined_ratio(
        [ratios['pb'], ratios['pe'], inverted_dyr_df],
        [weights['pb'], weights['pe'], weights['dividend_yield']]
    )
    
    return combined_value_ratio 