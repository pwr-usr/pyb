# Financial Analysis Package

A modular Python package for analyzing financial ratios and backtesting investment strategies.

## Features

- Load and preprocess financial data
- Calculate and analyze various financial ratios:
  - Price-to-Book (PB)
  - Price-to-Earnings (PE)
  - Dividend Yield
  - Market Capitalization
- Create and backtest investment strategies
- Visualize performance and sector allocation
- Combine multiple ratios with custom weights

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd financial-analysis

# Install the package
pip install -e .
```

## Usage

### Running the Full Analysis

The easiest way to run the full analysis is to use the built-in script:

```bash
python -m financial_analysis.run_analysis
```

### Using Individual Components

You can also use the components individually:

```python
# Import required modules
from financial_analysis.data.loading import load_and_filter_price_data, load_stock_info, get_ah_stocks
from financial_analysis.ratios.financial_ratios import load_and_prepare_ratios, create_value_composite
from financial_analysis.strategies.backtest import create_pb_strategy, run_backtest
from financial_analysis.visualization.analysis import compare_strategies_performance

# Load data
stocks_info = load_stock_info()
ah_stocks = get_ah_stocks()
close_df, close_df_filtered = load_and_filter_price_data(ah_stocks, stocks_info)

# Load and prepare ratios
ratios = load_and_prepare_ratios(ah_stocks, close_df_filtered)

# Create and run a strategy
pb_strategy = create_pb_strategy(ratios['pb'], k=50, rebalance_period='quarterly')
result = run_backtest(pb_strategy, close_df_filtered, 'PB Strategy')

# Display results
print(result.display())
```

## Package Structure

The package is organized into several modules:

- `data`: Functions for loading and preprocessing data
- `ratios`: Classes and functions for financial ratio calculations
- `strategies`: Strategy creation and backtesting functions
- `visualization`: Analysis and visualization functions

## Requirements

- Python 3.6+
- pandas
- numpy
- matplotlib
- bt (backtesting library)
- pyb (for data access)

## License

[MIT License](LICENSE) 