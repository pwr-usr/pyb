"""
Main script to run financial ratio analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import modules
from financial_analysis.data.loading import load_and_filter_price_data, load_stock_info, get_ah_stocks
from financial_analysis.ratios.financial_ratios import (
    load_and_prepare_ratios,
    create_value_composite
)
from financial_analysis.strategies.backtest import (
    create_pb_strategy,
    create_pe_strategy,
    create_dividend_strategy,
    create_combined_strategy,
    run_backtest
)
from financial_analysis.visualization.analysis import (
    compare_strategies_performance,
    display_strategy_stats,
    analyze_sector_performance,
    plot_sector_comparisons,
    plot_rolling_returns,
    plot_drawdowns
)


def main():
    """Run the main analysis."""
    # 1. Load data
    print("Loading data...")
    stocks_info = load_stock_info()
    ah_stocks = get_ah_stocks()
    close_df, close_df_filtered = load_and_filter_price_data(ah_stocks, stocks_info)
    
    # 2. Load and prepare ratios
    print("Preparing financial ratios...")
    ratios = load_and_prepare_ratios(ah_stocks, close_df_filtered)
    
    # 3. Create combined value ratio
    print("Creating combined value ratio...")
    combined_ratio = create_value_composite(ratios)
    
    # 4. Create strategies
    print("Creating strategies...")
    strategies = {
        'PB Strategy': create_pb_strategy(ratios['pb']),
        'PE Strategy': create_pe_strategy(ratios['pe']),
        'Dividend Strategy': create_dividend_strategy(ratios['dividend_yield']),
        'Combined Strategy': create_combined_strategy(combined_ratio)
    }
    
    # 5. Run backtests
    print("Running backtests...")
    results = {}
    for name, strategy in strategies.items():
        results[name] = run_backtest(strategy, close_df_filtered, name)
    
    # 6. Analyze and visualize results
    print("Analyzing results...")
    
    # Performance comparison
    fig1 = compare_strategies_performance(results)
    fig1.savefig('strategy_performance.png')
    
    # Display performance statistics
    display_strategy_stats(results)
    
    # Sector analysis
    sector_weights = {}
    for name, result in results.items():
        sector_weights[name] = analyze_sector_performance(result, stocks_info)
    
    # Plot sector comparisons
    fig2 = plot_sector_comparisons(sector_weights)
    fig2.savefig('sector_allocation.png')
    
    # Rolling returns
    fig3 = plot_rolling_returns(results)
    fig3.savefig('rolling_returns.png')
    
    # Drawdowns
    fig4 = plot_drawdowns(results)
    fig4.savefig('drawdowns.png')
    
    print("Analysis complete!")


if __name__ == "__main__":
    main() 