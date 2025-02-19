import os
import json
import time
from libs.candlestick import download_candlestick
from pyb.paths import get_data_dir

REQUEST_INTERVAL = 0.07  # seconds between requests

def main():
    # Take user input for the date range and stock codes
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    stock_codes_input = input("Enter a comma separated list of stock codes: ")
    stock_codes = [s.strip() for s in stock_codes_input.split(",") if s.strip()]
    
    # Determine the directory to store candlestick data
    data_dir = get_data_dir()
    candlestick_dir = os.path.join(data_dir, "candlestick_data")
    os.makedirs(candlestick_dir, exist_ok=True)
    
    # Download and save candlestick data for each stock
    for stock in stock_codes:
        print(f"Downloading candlestick data for {stock}...")
        data = download_candlestick(stock, start_date, end_date)
        if not data:
            print(f"No data returned for {stock}.")
            continue
        output_file = os.path.join(candlestick_dir, f"{stock}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Candlestick data for {stock} saved to {output_file}")
        time.sleep(REQUEST_INTERVAL)


if __name__ == "__main__":
    main() 