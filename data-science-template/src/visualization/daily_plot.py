import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_daily_predictions(df, actual_col='actual', pred_col='predicted'):
    """
    Plot daily actual vs predicted values with confidence bands
    """
    plt.figure(figsize=(15, 8))
    
    # Plot actual values
    plt.plot(df.index, df[actual_col], label='Actual', color='blue', alpha=0.6)
    
    # Plot predictions with confidence band
    plt.plot(df.index, df[pred_col], label='Predicted', color='red', alpha=0.6)
    
    # Add confidence band if available
    if 'conf_lower' in df.columns and 'conf_upper' in df.columns:
        plt.fill_between(df.index, 
                        df['conf_lower'], 
                        df['conf_upper'],
                        alpha=0.2, 
                        color='gray',
                        label='95% Confidence Interval')
    
    plt.title('Daily Market Predictions vs Actual Values')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return plt.gcf()

def add_prediction_metrics(df):
    """
    Add prediction metrics like error and confidence intervals
    """
    df['error'] = df['actual'] - df['predicted']
    df['abs_error'] = abs(df['error'])
    
    # Calculate rolling standard deviation for confidence intervals
    rolling_std = df['error'].rolling(window=20).std()
    
    # Create 95% confidence intervals
    df['conf_lower'] = df['predicted'] - (1.96 * rolling_std)
    df['conf_upper'] = df['predicted'] + (1.96 * rolling_std)
    
    return df
