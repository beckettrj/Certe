import yfinance as yf
import pandas as pd
from typing import Optional

class StockDataFetcher:
    def __init__(self, symbol: str):
        self.symbol = symbol
        
    def fetch_data(self, period: str = "1y") -> pd.DataFrame:
        """Fetch stock data from Yahoo Finance"""
        stock = yf.Ticker(self.symbol)
        data = stock.history(period=period)
        return self._preprocess_data(data)
    
    def _preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the raw stock data"""
        data['Returns'] = data['Close'].pct_change()
        data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
        data['Price_MA'] = data['Close'].rolling(window=20).mean()
        return data.dropna()
