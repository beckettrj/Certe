import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class SignalVisualizer:
    def __init__(self, figsize: tuple = (12, 8)):
        self.figsize = figsize
        
    def plot_strategy_performance(self, data: pd.DataFrame, backtest_results: dict):
        """Plot strategy performance and signals"""
        plt.figure(figsize=self.figsize)
        
        # Plot cumulative returns
        plt.subplot(2, 1, 1)
        backtest_results['cumulative_returns'].plot(title='Strategy Performance')
        plt.ylabel('Cumulative Returns')
        
        # Plot signal distribution
        plt.subplot(2, 1, 2)
        data['Signal_Type'].value_counts().plot(kind='bar', title='Signal Distribution')
        plt.ylabel('Count')
        
        plt.tight_layout()
        plt.show()
