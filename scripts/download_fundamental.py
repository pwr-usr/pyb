# scripts/download_fundamental.py
import os
import json
import time
from libs.fundamental import download_fundamental

REQUEST_INTERVAL = 0.07  # seconds between requests to avoid exceeding limit
MAX_RETRIES = 3

def main():
    # Load stock information from data/stock_info.json
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    stock_info_file = os.path.join(data_dir, "stock_info.json")

    if not os.path.exists(stock_info_file):
        print("Stock information file not found. Please run download_stock_info.py first.")
        return

    with open(stock_info_file, "r", encoding="utf-8") as f:
        stock_info = json.load(f)

    # Create a directory for fundamental data
    fundamental_dir = os.path.join(data_dir, "fundamental_data")
    os.makedirs(fundamental_dir, exist_ok=True)

    # Download fundamental data for each stock.
    for stock in stock_info:
        stock_code = stock.get("stockCode")
        # filter non ah stocks
        if not stock.get("mutualMarkets"):
            continue
        fs_table_type = stock.get("fsTableType")
        if not stock_code or not fs_table_type:
            print(f"Skipping stock with missing stockCode or fsTableType: {stock}")
            continue
        output_file = os.path.join(fundamental_dir, f"{stock_code}.json")
        if os.path.exists(output_file):
            print(f"Skipping download for {stock_code}: file already exists.")
            continue
        print(f"Downloading fundamental data for {stock_code} (fsTableType: {fs_table_type})...")
        fundamental_data = None
        for attempt in range(1, MAX_RETRIES+1):
            try:
                print(f"Attempt {attempt} for {stock_code}...")
                fundamental_data = download_fundamental(stock_code, fs_table_type)
                break
            except Exception as e:
                if '429' in str(e):
                    print(f"Received 429 Too Many Requests for {stock_code}, attempt {attempt}/{MAX_RETRIES}. Waiting before retrying...")
                    time.sleep(REQUEST_INTERVAL * attempt * 2)
                else:
                    print(f"Error downloading fundamental data for {stock_code}: {e}")
                    break
        if fundamental_data is None:
            print(f"Skipping saving fundamental data for {stock_code} due to errors.")
            continue
        
        # Save fundamental data to a JSON file named {stock_code}.json.
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(fundamental_data, f, indent=4, ensure_ascii=False)
        print(f"Fundamental data for {stock_code} saved to {output_file}")
        time.sleep(REQUEST_INTERVAL)

if __name__ == "__main__":
    main()
