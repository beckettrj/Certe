import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_historical_prices(data, stock_symbol):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Date'], data['Close'], label='Close Price', color='blue')
    plt.title(f'Historical Prices for {stock_symbol}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()

def plot_predicted_vs_actual(actual_data, predicted_data, stock_symbol):
    plt.figure(figsize=(14, 7))
    plt.plot(actual_data['Date'], actual_data['Close'], label='Actual Price', color='blue')
    plt.plot(predicted_data['Date'], predicted_data['Predicted'], label='Predicted Price', color='orange')
    plt.title(f'Predicted vs Actual Prices for {stock_symbol}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()

def plot_strategy_performance(daily_returns, strategy_name):
    plt.figure(figsize=(14, 7))
    plt.plot(daily_returns.index, daily_returns, label=strategy_name, color='green')
    plt.title(f'Strategy Performance: {strategy_name}')
    plt.xlabel('Date')
    plt.ylabel('Daily Returns')
    plt.legend()
    plt.grid()
    plt.show()