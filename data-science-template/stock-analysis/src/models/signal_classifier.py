import pandas as pd
import numpy as np

def classify_signal_strength(data: pd.DataFrame) -> pd.Series:
    """
    Classify market signals based on price movements and sentiment
    
    Parameters from paper:
    - α (alpha): overreaction coefficient for weak signals
    - β (beta): underreaction coefficient for strong signals
    """
    # Constants from the paper
    ALPHA_THRESHOLD = 1.5  # Overreaction threshold
    BETA_THRESHOLD = 0.7   # Underreaction threshold
    
    # Calculate signal strength based on combined metrics
    signal_strength = pd.Series(index=data.index)
    
    for i in range(len(data)):
        sentiment_score = data['sentiment_score'].iloc[i]
        price_change = data['price'].pct_change().iloc[i]
        volume_change = data['volume'].pct_change().iloc[i]
        
        # Combined signal strength metric
        signal_magnitude = abs(sentiment_score * price_change * volume_change)
        
        if signal_magnitude > BETA_THRESHOLD:
            signal_strength.iloc[i] = 'strong'
        elif signal_magnitude < ALPHA_THRESHOLD:
            signal_strength.iloc[i] = 'weak'
        else:
            signal_strength.iloc[i] = 'neutral'
            
    return signal_strength