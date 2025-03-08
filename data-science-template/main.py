from src.data_acquisition import StockDataFetcher
from src.signal_classifier import SignalClassifier
from src.backtester import SignalBacktester
from src.visualizer import SignalVisualizer
import argparse

def main():
    parser = argparse.ArgumentParser(description='Market Signal Analysis')
    parser.add_argument('--symbol', type=str, default='AAPL', help='Stock symbol to analyze')
    parser.add_argument('--period', type=str, default='1y', help='Data period to analyze')
    args = parser.parse_args()

    # Initialize components
    fetcher = StockDataFetcher(args.symbol)
    classifier = SignalClassifier()
    backtester = SignalBacktester()
    visualizer = SignalVisualizer()

    # Run analysis pipeline
    data = fetcher.fetch_data(period=args.period)
    classified_data = classifier.classify_signals(data)
    backtest_results = backtester.run_backtest(classified_data)
    visualizer.plot_strategy_performance(classified_data, backtest_results)

if __name__ == "__main__":
    main()
