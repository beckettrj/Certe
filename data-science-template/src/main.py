import pandas as pd
from visualization.daily_plot import plot_daily_predictions, add_prediction_metrics
from data.loader import load_market_data, get_multiple_symbols
from models.predictor import generate_predictions

def main():
    # Load market data for SPY (S&P 500 ETF)
    df = load_market_data(symbol='SPY', period='1y', interval='1d')
    
    # Optional: Load multiple symbols
    # market_data = get_multiple_symbols(['SPY', 'QQQ', 'AAPL'])
    
    # Generate predictions
    df['predicted'] = generate_predictions(df)
    
    # Add error metrics and confidence intervals
    df = add_prediction_metrics(df)
    
    # Create and save daily plot
    fig = plot_daily_predictions(df)
    fig.savefig('outputs/daily_predictions.png')
    
    # Save detailed results
    df.to_csv('outputs/daily_results.csv')

if __name__ == "__main__":
    main()
