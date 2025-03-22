import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta
import logging

# Create a simple logger
logger = logging.getLogger('stock_analysis')
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

def fetch_market_data(symbols=['SPY', 'AAPL', 'MSFT'], 
                     start_date=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
                     end_date=datetime.now().strftime('%Y-%m-%d')):
    """
    Fetch market data for given symbols and date range
    """
    logger.info(f"Starting data fetch for symbols: {symbols}")
    data_frames = []
    
    for i, symbol in enumerate(symbols, 1):
        logger.info(f"Fetching data for {symbol} ({i}/{len(symbols)})")
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date)
            df['Symbol'] = symbol
            data_frames.append(df)
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {str(e)}")
    
    combined_data = pd.concat(data_frames)
    output_file = os.path.join(DATA_DIR, 'market_data.csv')
    os.makedirs(DATA_DIR, exist_ok=True)
    combined_data.to_csv(output_file)
    logger.info(f"Data saved to {output_file}")
    return output_file

if __name__ == "__main__":
    fetch_market_data()
