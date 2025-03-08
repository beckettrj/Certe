import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def load_market_data(symbol='SPY', period='1y', interval='1d'):
    """
    Load market data from Yahoo Finance
    
    Args:
        symbol (str): Stock symbol (default: SPY)
        period (str): Data period (default: 1y)
        interval (str): Data interval (default: 1d)
    
    Returns:
        pd.DataFrame: DataFrame with market data
    """
    # Fetch data from Yahoo Finance
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    
    # Prepare the data
    df = df.rename(columns={'Close': 'actual'})
    df = df[['actual']]  # Keep only the closing price for now
    
    # Handle any missing values
    df = df.fillna(method='ffill')
    
    return df

def get_multiple_symbols(symbols=['SPY', 'QQQ'], period='1y', interval='1d'):
    """
    Load data for multiple symbols
    """
    dfs = {}
    for symbol in symbols:
        dfs[symbol] = load_market_data(symbol, period, interval)
    return dfs
