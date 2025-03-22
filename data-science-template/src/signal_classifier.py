import pandas as pd
import numpy as np
from typing import Tuple

class SignalClassifier:
    def __init__(self, price_threshold: float = 0.02, volume_threshold: float = 2.0):
        self.price_threshold = price_threshold
        self.volume_threshold = volume_threshold
    
    def classify_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Classify signals as weak or strong based on price and volume changes"""
        data = data.copy()
        
        # Classify based on price movements and volume
        data['Signal_Strength'] = self._calculate_signal_strength(data)
        data['Signal_Type'] = np.where(
            data['Signal_Strength'] > self.price_threshold, 
            'strong', 
            np.where(data['Signal_Strength'] < -self.price_threshold, 'weak', 'neutral')
        )
        
        return data
    
    def _calculate_signal_strength(self, data: pd.DataFrame) -> pd.Series:
        """Calculate signal strength based on price and volume metrics"""
        price_change = data['Returns'].abs()
        volume_ratio = data['Volume'] / data['Volume_MA']
        
        return price_change * np.log1p(volume_ratio)
