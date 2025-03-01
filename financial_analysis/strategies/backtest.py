"""
Backtest module for creating and running investment strategies.
"""

import bt
import pandas as pd


class LogAvailableStocks(bt.Algo):
    """Algorithm for logging available stocks at each rebalance date."""
    
    def __init__(self, store_dict=None):
        """
        Initialize the algorithm.
        
        Parameters:
        -----------
        store_dict : dict, optional
            Dictionary to store available stock counts
        """
        super(LogAvailableStocks, self).__init__()
        if store_dict is None:
            store_dict = {}
        self.store_dict = store_dict

    def __call__(self, target):
        """
        Execute the algorithm.
        
        Parameters:
        -----------
        target : bt.Backtest
            Backtest target
            
        Returns:
        --------
        bool
            Always returns True
        """
        # Extract the row of data for target.now
        row = target.data.loc[target.now]

        # Count how many tickers have valid (non-NaN) price
        num_available = row.dropna().shape[0]

        # Record it in the dictionary
        self.store_dict[target.now] = num_available

        return True


class SelectTopK(bt.AlgoStack):
    """Algorithm for selecting top K securities based on a signal."""
    
    def __init__(self, signal, K, sort_descending=True, all_or_none=False, filter_selected=True):
        """
        Initialize the algorithm.
        
        Parameters:
        -----------
        signal : pandas.DataFrame
            Signal DataFrame for selection
        K : int
            Number of securities to select
        sort_descending : bool, optional
            If True, sort in descending order (higher is better)
        all_or_none : bool, optional
            If True, select all securities or none
        filter_selected : bool, optional
            If True, filter out securities not in the universe
        """
        super(SelectTopK, self).__init__(bt.algos.SetStat(signal),
                                      bt.algos.SelectN(K, sort_descending, all_or_none, filter_selected))


def create_strategy(name, signal_df, k=50, rebalance_period='quarterly', sort_descending=False):
    """
    Create a strategy based on a signal DataFrame.
    
    Parameters:
    -----------
    name : str
        Strategy name
    signal_df : pandas.DataFrame
        Signal DataFrame for selection
    k : int, optional
        Number of securities to select
    rebalance_period : str, optional
        Rebalance period: 'quarterly', 'monthly', or 'weekly'
    sort_descending : bool, optional
        If True, sort in descending order (higher is better)
        
    Returns:
    --------
    bt.Strategy
        Strategy object
    """
    available_stocks_log = {}
    
    if rebalance_period == 'quarterly':
        rebalance_algo = bt.algos.RunQuarterly(run_on_first_date=True)
    elif rebalance_period == 'monthly':
        rebalance_algo = bt.algos.RunMonthly(run_on_first_date=True)
    elif rebalance_period == 'weekly':
        rebalance_algo = bt.algos.RunWeekly(run_on_first_date=True)
    else:  # default to quarterly
        rebalance_algo = bt.algos.RunQuarterly(run_on_first_date=True)
    
    return bt.Strategy(name, [
        rebalance_algo,
        LogAvailableStocks(available_stocks_log),
        SelectTopK(signal_df, K=k, sort_descending=sort_descending),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance()
    ])


def create_pb_strategy(pb_df_filtered, k=50, rebalance_period='quarterly'):
    """
    Create a strategy based on PB ratio.
    
    Parameters:
    -----------
    pb_df_filtered : pandas.DataFrame
        Filtered PB ratio DataFrame
    k : int, optional
        Number of securities to select
    rebalance_period : str, optional
        Rebalance period: 'quarterly', 'monthly', or 'weekly'
        
    Returns:
    --------
    bt.Strategy
        Strategy object
    """
    return create_strategy('pb_strategy', pb_df_filtered, k, rebalance_period, sort_descending=False)


def create_pe_strategy(pe_df_filtered, k=50, rebalance_period='quarterly'):
    """
    Create a strategy based on PE ratio.
    
    Parameters:
    -----------
    pe_df_filtered : pandas.DataFrame
        Filtered PE ratio DataFrame
    k : int, optional
        Number of securities to select
    rebalance_period : str, optional
        Rebalance period: 'quarterly', 'monthly', or 'weekly'
        
    Returns:
    --------
    bt.Strategy
        Strategy object
    """
    return create_strategy('pe_strategy', pe_df_filtered, k, rebalance_period, sort_descending=False)


def create_dividend_strategy(dyr_df_filtered, k=50, rebalance_period='quarterly'):
    """
    Create a strategy based on Dividend Yield.
    
    Parameters:
    -----------
    dyr_df_filtered : pandas.DataFrame
        Filtered Dividend Yield ratio DataFrame
    k : int, optional
        Number of securities to select
    rebalance_period : str, optional
        Rebalance period: 'quarterly', 'monthly', or 'weekly'
        
    Returns:
    --------
    bt.Strategy
        Strategy object
    """
    return create_strategy('dividend_strategy', dyr_df_filtered, k, rebalance_period, sort_descending=True)


def create_combined_strategy(combined_ratio, k=50, rebalance_period='quarterly'):
    """
    Create a strategy based on a combined ratio.
    
    Parameters:
    -----------
    combined_ratio : pandas.DataFrame
        Combined ratio DataFrame
    k : int, optional
        Number of securities to select
    rebalance_period : str, optional
        Rebalance period: 'quarterly', 'monthly', or 'weekly'
        
    Returns:
    --------
    bt.Strategy
        Strategy object
    """
    return create_strategy('combined_strategy', combined_ratio, k, rebalance_period, sort_descending=False)


def run_backtest(strategy, price_data, name=None):
    """
    Run a backtest for the given strategy.
    
    Parameters:
    -----------
    strategy : bt.Strategy
        Strategy object
    price_data : pandas.DataFrame
        Price data DataFrame
    name : str, optional
        Backtest name
        
    Returns:
    --------
    bt.backtest.Result
        Backtest result
    """
    if name is None:
        name = strategy.name
        
    backtest = bt.Backtest(strategy, price_data, name=name)
    result = bt.run(backtest)
    
    return result 