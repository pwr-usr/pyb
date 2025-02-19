import os
import json
import glob
import pandas as pd


def get_candlestick_data(symbols=None, output_format='bt', candlestick_dir=None):
    """
    Retrieve candlestick data for selected stocks from local JSON files.
    
    Args:
      symbols: A list of symbols or a single symbol string. If not provided, all stocks in the candlestick data directory are used.
      output_format: Desired output format, 'bt' for pivot table (date index, symbols as columns with close price) or 'double' for multiindex dataframe on [date, symbol].
      candlestick_dir: Optional path to the directory containing candlestick JSON files. If not provided, defaults to <project_root>/data/candlestick_data.
    
    Returns:
      pandas.DataFrame: The resulting dataframe according to the selected format.
    """
    # Determine the candlestick data directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if candlestick_dir is None:
        candlestick_dir = os.path.join(BASE_DIR, 'data', 'candlestick_data')
    
    # If symbols is None, get all available symbols from JSON files
    if symbols is None:
        all_files = glob.glob(os.path.join(candlestick_dir, '*.json'))
        symbols = [os.path.splitext(os.path.basename(f))[0] for f in all_files]
    elif isinstance(symbols, str):
        symbols = [symbols]
    
    records = []
    for symbol in symbols:
        file_path = os.path.join(candlestick_dir, f"{symbol}.json")
        if not os.path.exists(file_path):
            print(f"Warning: Candlestick file not found for symbol {symbol} at {file_path}")
            continue
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading data for symbol {symbol} from {file_path}: {e}")
            continue
        
        for rec in data:
            record_date = rec.get('date')
            close_val = rec.get('close')
            if record_date is not None and close_val is not None:
                records.append({'date': record_date, 'symbol': symbol, 'close': close_val})
            else:
                print(f"Warning: Missing 'date' or 'close' in record for symbol {symbol}: {rec}")
    
    if not records:
        print("No candlestick records found.")
        return pd.DataFrame()
    
    df = pd.DataFrame(records)
    try:
        df['date'] = pd.to_datetime(df['date'])
    except Exception as e:
        print("Warning: Could not convert 'date' column to datetime:", e)
    
    if output_format == 'bt':
        # Pivot: index = date, columns = symbol, values = close
        result = df.pivot_table(index='date', columns='symbol', values='close')
        result = result.sort_index()
    elif output_format == 'double':
        # MultiIndex DataFrame with index [date, symbol]
        result = df.set_index(['date', 'symbol']).sort_index()
    else:
        print(f"Output format '{output_format}' not recognized. Returning original dataframe.")
        result = df
    
    return result


if __name__ == '__main__':
    # Example usage:
    df = get_candlestick_data(symbols=['00700'], output_format='bt')
    print(df.head()) 