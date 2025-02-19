import os
import json
import glob
import pandas as pd

def get_fundamental_data(symbols=None, ratio='mc', output_format='bt', fundamental_dir=None):
    """
    Retrieve fundamental data for selected stocks.
    
    Args:
      symbols: a list of symbols or a single symbol string. If not provided, all stocks in the fundamental data directory are used.
      ratio: the fundamental financial ratio to extract (e.g., 'mc').
      output_format: desired output format, 'bt' for pivot table (date index, symbols as columns) or 'double' for multiindex dataframe on [date, symbol].
      fundamental_dir: optional path to the directory containing fundamental JSON files. If not provided, defaults to <project_root>/data/fundamental_data.
    
    Returns:
      pandas.DataFrame: The resulting dataframe according to the selected format.
    """
    
    # Determine the fundamental data directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if fundamental_dir is None:
        fundamental_dir = os.path.join(BASE_DIR, 'data', 'fundamental_data')
    
    # If symbols is None, get all available symbols from JSON files
    if symbols is None:
        all_files = glob.glob(os.path.join(fundamental_dir, '*.json'))
        symbols = [os.path.splitext(os.path.basename(f))[0] for f in all_files]
    elif isinstance(symbols, str):
        symbols = [symbols]
    
    records = []
    for symbol in symbols:
        file_path = os.path.join(fundamental_dir, f"{symbol}.json")
        if not os.path.exists(file_path):
            print(f"Warning: Fundamental file not found for symbol {symbol} at {file_path}")
            continue
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading data for symbol {symbol} from {file_path}: {e}")
            continue
        
        # If data is wrapped in a dict under key 'data', use that
        if isinstance(data, dict) and 'data' in data:
            data = data['data']
        if not isinstance(data, list):
            print(f"Unexpected data format in {file_path}. Expected a list of records.")
            continue
        
        for rec in data:
            if ratio in rec:
                record_date = rec.get('date')
                ratio_val = rec.get(ratio)
                if record_date is not None:
                    records.append({'date': record_date, 'symbol': symbol, ratio: ratio_val})
            else:

                print("record is ", rec)
                print(f"Warning: Ratio '{ratio}' not found in record for symbol {symbol}.")
    
    if not records:
        print("No fundamental records found.")
        return pd.DataFrame()
    
    df = pd.DataFrame(records)
    
    # Convert 'date' column to datetime if possible
    try:
        df['date'] = pd.to_datetime(df['date'])
    except Exception as e:
        print("Warning: Could not convert 'date' column to datetime:", e)
    
    if output_format == 'bt':
        # Pivot: index = date, columns = symbol, values = ratio
        result = df.pivot_table(index='date', columns='symbol', values=ratio)
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
    df = get_fundamental_data(symbols=['00001'], ratio='·', output_format='bt')
    print(df.head()) 