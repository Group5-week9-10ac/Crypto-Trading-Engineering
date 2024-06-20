import yfinance as yf
from pandas_datareader import data as pdr
from backend.src.backtest.crypto_data.config import CRYPTO_SYMBOLS, START_DATE, END_DATE
from backend.src.backtest.crypto_data.utils import save_data

def download_data(symbol: str, start_date: str, end_date: str):
    """
    Download historical data for a given cryptocurrency symbol from Yahoo Finance.

    Args:
    - symbol (str): Cryptocurrency symbol (e.g., 'BTC-USD').
    - start_date (str): Start date in 'YYYY-MM-DD' format.
    - end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
    - pd.DataFrame or None: DataFrame containing historical data, or None if download fails.
    """
    try:
        yf.pdr_override()  # override yfinance API
        data = pdr.get_data_yahoo(symbol, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Error downloading data for {symbol}: {str(e)}")
        return None

def load_crypto_data():
    """
    Download data for each cryptocurrency symbol in CRYPTO_SYMBOLS and save as CSV.

    This function iterates through each symbol in CRYPTO_SYMBOLS, downloads historical data
    using download_data function, and saves the data as CSV files in the 'data' folder.

    """
    for symbol in CRYPTO_SYMBOLS:
        data = download_data(symbol, START_DATE, END_DATE)
        if data is not None:
            save_data(data, f"{symbol}_data.csv")  # Save data in the 'data' folder

if __name__ == "__main__":
    load_crypto_data()
