import yfinance as yf
import pandas as pd

class APIManager:
    def __init__(self):
        pass

    def get_yfinance_historical_data(self, ticker, period="1y", interval="1d"):
        try:
            data = yf.download(ticker, period=period, interval=interval)
            if data.empty:
                return None
            return data
        except Exception as e:
            print(f"Error fetching data for {ticker} from Yahoo Finance: {e}")
            return None


