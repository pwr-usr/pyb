# libs/api_client.py
import requests

def post_request(url, payload):
    """Send a POST request and verify the API response."""
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    result = response.json()
    if result.get("code") != 1:
        raise Exception(f"API error: {result.get('message')}")
    return result
