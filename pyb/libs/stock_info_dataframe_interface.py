import pandas as pd
from pyb.libs.stock_info_interface import load_stock_info

def get_stock_info_dataframe():
    """
    Loads the stock information from stock_info.json and converts it to a pandas DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame containing the stock information.
    """
    data = load_stock_info()
    return pd.DataFrame(data)

if __name__ == '__main__':
    df = get_stock_info_dataframe()
    print("Stock Info DataFrame:")
    print(df.head()) 