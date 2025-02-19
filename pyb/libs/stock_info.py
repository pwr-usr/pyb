# libs/stock_info.py
from config.config import TOKEN, STOCK_INFO_URL
from libs.api_client import post_request


def download_stock_info(include_delisted=True):
    """
    Download stock information for all HK stocks.

    :param include_delisted: Set to True to include delisted stocks.
    :return: A list of stock information dictionaries.
    """
    payload = {
        "token": TOKEN,
        "includeDelisted": include_delisted
    }
    result = post_request(STOCK_INFO_URL, payload)
    return result.get("data", [])
