import pytest
from src.backtesting.strategies import contrarian_strategy, momentum_strategy

def test_contrarian_strategy():
    # Sample data for testing
    historical_data = [
        {'date': '2023-01-01', 'price': 100, 'signal': 'weak'},
        {'date': '2023-01-02', 'price': 90, 'signal': 'weak'},
        {'date': '2023-01-03', 'price': 95, 'signal': 'strong'},
    ]
    
    result = contrarian_strategy(historical_data)
    assert result['profit'] > 0  # Expect profit from contrarian strategy

def test_momentum_strategy():
    # Sample data for testing
    historical_data = [
        {'date': '2023-01-01', 'price': 100, 'signal': 'strong'},
        {'date': '2023-01-02', 'price': 110, 'signal': 'strong'},
        {'date': '2023-01-03', 'price': 115, 'signal': 'weak'},
    ]
    
    result = momentum_strategy(historical_data)
    assert result['profit'] > 0  # Expect profit from momentum strategy