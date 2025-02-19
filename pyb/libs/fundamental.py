# libs/fundamental.py
from config.config import TOKEN, FUNDAMENTAL_ENDPOINTS
from libs.api_client import post_request


def download_fundamental(stock_code, fs_table_type, start_date="2015-01-01", end_date="2025-01-01", metrics=None):
    """
    Download fundamental data for a given stock based on its fsTableType.

    :param stock_code: The stock code (e.g., "00700").
    :param fs_table_type: The financial report type from the stock info.
    :param start_date: Start date for the data (YYYY-MM-DD).
    :param end_date: End date for the data (YYYY-MM-DD).
    :param metrics: List of metrics to retrieve.
    :return: The fundamental data returned by the API.
    """
    if metrics is None:
        metrics = ["pe_ttm", "pb", "ps_ttm", "pcf_ttm", "dyr", "ta", "mc"]
    url = FUNDAMENTAL_ENDPOINTS.get(fs_table_type)
    if not url:
        raise ValueError(f"Unknown fsTableType: {fs_table_type}")
    payload = {
        "token": TOKEN,
        "startDate": start_date,
        "endDate": end_date,
        "stockCodes": [stock_code],  # API requires a single stock code when using date range
        "metricsList": metrics
    }
    result = post_request(url, payload)
    return result.get("data", [])
