# Stock Market Analysis Dashboard

An interactive dashboard for analyzing stock market data using Python, Streamlit, and yfinance.

## Features

- Fetch historical stock market data using yfinance
- Interactive data visualization with Plotly
- Customizable date ranges and stock symbols
- Price and volume analysis
- Summary statistics

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit dashboard:
```bash
cd scripts
streamlit run app.py
```

2. Use the sidebar controls to:
   - Select stocks to analyze
   - Choose date range
   - Fetch and visualize data

## Project Structure

```
stock-analysis/
├── data/               # Storage for downloaded market data
├── scripts/
│   ├── app.py         # Streamlit dashboard
│   ├── fetch_market_data.py  # Data fetching utilities
│   └── utils/         # Utility functions
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Data Sources

- Stock market data is fetched from Yahoo Finance using the yfinance library
- Default symbols: SPY, AAPL, MSFT
- Custom symbols can be added through the dashboard interface

## Testing

To run the tests, use the following command:

```bash
pytest
```

## License

This project is licensed under the MIT License.