import pandas as pd
import numpy as np
from typing import Dict, List

class SignalBacktester:
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        
    def run_backtest(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Run backtest on classified signals"""
        positions = self._generate_positions(data)
        
        # Calculate returns
        strategy_returns = positions * data['Returns'].shift(-1)
        cumulative_returns = (1 + strategy_returns).cumprod()
        
        return {
            'positions': positions,
            'strategy_returns': strategy_returns,
            'cumulative_returns': cumulative_returns
        }
    
    def _generate_positions(self, data: pd.DataFrame) -> pd.Series:
        """Generate trading positions based on signals"""
        positions = pd.Series(0, index=data.index)
        
        # Take contrarian positions on weak signals
        positions[data['Signal_Type'] == 'weak'] = -1
        
        # Take momentum positions on strong signals
        positions[data['Signal_Type'] == 'strong'] = 1
        
        return positions
