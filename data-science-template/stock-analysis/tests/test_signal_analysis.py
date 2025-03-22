import pytest
import pandas as pd
import numpy as np
from src.models.sentiment_analyzer import get_market_sentiment
from src.models.signal_classifier import classify_signal_strength
from src.models.predictor import generate_predictions

def test_signal_classification():
    """Test the classification of market signals based on sentiment and price movement"""
    test_data = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=5),
        'price': [100, 102, 101, 105, 103],
        'volume': [1000, 1200, 900, 1500, 1100],
        'sentiment_score': [0.2, 0.8, -0.3, 0.9, -0.1]
    })
    
    signals = classify_signal_strength(test_data)
    assert len(signals) == len(test_data)
    assert all(s in ['weak', 'strong', 'neutral'] for s in signals)

def test_overreaction_to_weak_signals():
    """Test if the model identifies overreaction to weak signals"""
    test_data = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'price': [100, 95, 92, 94, 96, 95, 97, 96, 98, 97],
        'sentiment_score': [0.1, -0.2, -0.1, 0.1, 0.2, -0.1, 0.1, -0.1, 0.2, 0.1],
        'signal_strength': ['weak'] * 10
    })
    
    predictions = generate_predictions(test_data)
    
    # Based on paper's theorem: overreaction coefficient α > 1 for weak signals
    overreaction_coefficient = calculate_overreaction_coefficient(test_data, predictions)
    assert overreaction_coefficient > 1.0

def test_underreaction_to_strong_signals():
    """Test if the model identifies underreaction to strong signals"""
    test_data = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'price': [100, 105, 108, 106, 107, 109, 108, 110, 111, 112],
        'sentiment_score': [0.8, 0.7, 0.9, 0.8, 0.7, 0.8, 0.9, 0.8, 0.7, 0.8],
        'signal_strength': ['strong'] * 10
    })
    
    predictions = generate_predictions(test_data)
    
    # Based on paper's theorem: underreaction coefficient β < 1 for strong signals
    underreaction_coefficient = calculate_underreaction_coefficient(test_data, predictions)
    assert underreaction_coefficient < 1.0

def calculate_overreaction_coefficient(data: pd.DataFrame, predictions: pd.Series) -> float:
    """
    Calculate overreaction coefficient α based on paper's methodology
    α = (Observed Price Movement) / (Rational Price Movement)
    """
    observed_movement = data['price'].pct_change().abs().mean()
    rational_movement = predictions.pct_change().abs().mean()
    return observed_movement / rational_movement

def calculate_underreaction_coefficient(data: pd.DataFrame, predictions: pd.Series) -> float:
    """
    Calculate underreaction coefficient β based on paper's methodology
    β = (Observed Price Movement) / (Rational Price Movement)
    """
    observed_movement = data['price'].pct_change().abs().mean()
    rational_movement = predictions.pct_change().abs().mean()
    return observed_movement / rational_movement