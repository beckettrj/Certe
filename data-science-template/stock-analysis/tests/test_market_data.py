import unittest
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.fetch_market_data import fetch_market_data

class TestMarketData(unittest.TestCase):
    def test_fetch_market_data(self):
        # Test with a single symbol for a short duration
        result = fetch_market_data(
            symbols=['SPY'],
            start_date=(datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
            end_date=datetime.now().strftime('%Y-%m-%d')
        )
        self.assertTrue(os.path.exists(result))
        
if __name__ == '__main__':
    unittest.main()
