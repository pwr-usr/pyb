# scripts/download_stock_info.py
import os
import json
import time
from libs.stock_info import download_stock_info

REQUEST_INTERVAL = 0.07  # seconds between requests, though only one expected
MAX_RETRIES = 3

def main():
    from pyb.paths import get_data_dir
    data_dir = get_data_dir()
    output_file = os.path.join(data_dir, "stock_info.json")
    if os.path.exists(output_file):
         print(f"Stock information already exists at {output_file}. Skipping download.")
         return

    print("Downloading stock information...")
    stock_data = None
    for attempt in range(1, MAX_RETRIES+1):
         try:
              print(f"Attempt {attempt} for stock information...")
              stock_data = download_stock_info(include_delisted=True)
              break
         except Exception as e:
              if '429' in str(e):
                  print(f"Received 429 Too Many Requests, attempt {attempt}/{MAX_RETRIES}. Waiting before retrying...")
                  time.sleep(REQUEST_INTERVAL * attempt * 2)
              else:
                  print(f"Error downloading stock information: {e}")
                  break
    if stock_data is None:
         print("Skipping saving stock information due to errors.")
         return

    with open(output_file, "w", encoding="utf-8") as f:
         json.dump(stock_data, f, indent=4, ensure_ascii=False)
    print(f"Stock information saved to {output_file}")

if __name__ == "__main__":
    main()
