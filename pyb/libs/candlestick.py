from config.config import TOKEN
from .api_client import post_request


def download_candlestick(stock_code, start_date, end_date, candlestick_type='bc_rights'):
    """
    Download candlestick data for a given stock.

    Args:
        stock_code (str): The stock code.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        candlestick_type (str): Adjustment type; defaults to 'bc_rights'.

    Returns:
        list: The list of candlestick data records from the API.
    """
    url = "https://open.lixinger.com/api/hk/company/candlestick"
    payload = {
        "token": TOKEN,
        "type": candlestick_type,
        "startDate": start_date,
        "endDate": end_date,
        "stockCode": stock_code
    }
    result = post_request(url, payload)
    return result.get("data", []) 