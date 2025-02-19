import os
import json
import time
from .candlestick import download_candlestick
from pyb.paths import get_data_dir


def download_candlestick_data(stock_codes, start_date, end_date, candlestick_type='bc_rights', candlestick_dir=None, request_interval=0.07):
    """
    Download candlestick data for a list of stock codes and save them as JSON files in the candlestick data directory.
    
    This function is designed to be used in a Jupyter notebook or other interactive environment and provides an interface for downloading data without command-line input.
    
    Args:
        stock_codes (list or str): A list of stock codes or a single stock code string.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        candlestick_type (str): Adjustment type; defaults to 'bc_rights'.
        candlestick_dir (str, optional): Path to the directory to store JSON files. If not provided, defaults to <project_root>/data/candlestick_data.
        request_interval (float): Seconds to wait between API requests. Default is 0.07.
        
    Returns:
        dict: A dictionary mapping each stock code to its downloaded candlestick data (list). If download fails for a stock, its value will be None.
    """
    # Ensure stock_codes is a list
    if isinstance(stock_codes, str):
        stock_codes = [stock_codes]
        
    # Determine the candlestick data directory
    if candlestick_dir is None:
        data_dir = get_data_dir()
        candlestick_dir = os.path.join(data_dir, "candlestick_data")
    os.makedirs(candlestick_dir, exist_ok=True)

    results = {}
    for stock in stock_codes:
        print(f"Downloading candlestick data for {stock}...")
        data = download_candlestick(stock, start_date, end_date, candlestick_type=candlestick_type)
        if not data:
            print(f"No data returned for {stock}.")
            results[stock] = None
        else:
            output_file = os.path.join(candlestick_dir, f"{stock}.json")
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                print(f"Candlestick data for {stock} saved to {output_file}")
            except Exception as e:
                print(f"Error saving data for {stock} to {output_file}: {e}")
            results[stock] = data
        time.sleep(request_interval)

    return results


if __name__ == '__main__':
    # Example usage in a notebook:
    stock_list = ['00700', '00001']
    start = '2024-02-17'
    end = '2025-02-17'
    data_map = download_candlestick_data(stock_list, start, end)
    print(data_map) 