import unittest
import pandas as pd
import numpy as np
from src.signal_classifier import SignalClassifier

class TestSignalClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = SignalClassifier()
        
    def test_signal_classification(self):
        # Create sample data
        data = pd.DataFrame({
            'Close': [100, 102, 99, 98, 103],
            'Volume': [1000, 2000, 1500, 1000, 3000],
            'Returns': [0, 0.02, -0.03, -0.01, 0.05],
            'Volume_MA': [1000] * 5
        })
        
        result = self.classifier.classify_signals(data)
        self.assertTrue('Signal_Type' in result.columns)
        self.assertTrue(all(result['Signal_Type'].isin(['strong', 'weak', 'neutral'])))

if __name__ == '__main__':
    unittest.main()
