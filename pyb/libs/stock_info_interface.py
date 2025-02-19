import json
import os

# Compute the base directory of the project (three levels up from this file)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STOCK_INFO_PATH = os.path.join(BASE_DIR, 'data', 'stock_info.json')

def load_stock_info():
    """Load the stock information from the JSON file."""
    with open(STOCK_INFO_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_ah_stock_codes():
    """Retrieve a list of stock codes for AH stocks (where 'ah' is in the mutualMarkets list)."""
    stocks = load_stock_info()
    ah_stocks = [stock['stockCode'] for stock in stocks if 'mutualMarkets' in stock and stock['mutualMarkets'] == ["ah"]]
    return ah_stocks

def get_stock_info_summary():
    """Return a summary dict with total stocks, count of AH stocks, and count of normally_listed stocks."""
    stocks = load_stock_info()
    total = len(stocks)
    count_ah = sum(1 for stock in stocks if 'mutualMarkets' in stock and isinstance(stock['mutualMarkets'], list) and 'ah' in stock['mutualMarkets'])
    count_normally_listed = sum(1 for stock in stocks if stock.get('listingStatus') == 'normally_listed')
    return {
        'total_stocks': total,
        'ah_stocks': count_ah,
        'normally_listed': count_normally_listed
    }

if __name__ == '__main__':
    print("AH Stocks:", get_ah_stock_codes())
    print("Stock Info Summary:", get_stock_info_summary()) 