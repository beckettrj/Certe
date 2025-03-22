import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from fetch_market_data import fetch_market_data

st.set_page_config(page_title="Stock Market Analysis", layout="wide")
st.title("Stock Market Analysis Dashboard")

# Sidebar controls
st.sidebar.header("Settings")
default_symbols = ['SPY', 'AAPL', 'MSFT']
symbols = st.sidebar.multiselect(
    "Select stocks to analyze",
    options=['SPY', 'AAPL', 'MSFT', 'GOOGL', 'AMZN'],
    default=default_symbols
)

date_col1, date_col2 = st.sidebar.columns(2)
with date_col1:
    start_date = st.date_input(
        "Start date",
        value=datetime.now() - timedelta(days=365)
    )
with date_col2:
    end_date = st.date_input(
        "End date",
        value=datetime.now()
    )

if st.sidebar.button("Fetch Data"):
    with st.spinner("Fetching market data..."):
        data_file = fetch_market_data(
            symbols=symbols,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        df = pd.read_csv(data_file, index_col=0)
        df.index = pd.to_datetime(df.index)
        
        # Price chart
        st.subheader("Stock Prices Over Time")
        fig = px.line(df, x=df.index, y='Close', color='Symbol',
                     title="Closing Prices")
        st.plotly_chart(fig, use_container_width=True)
        
        # Volume chart
        st.subheader("Trading Volume")
        fig_volume = px.bar(df, x=df.index, y='Volume', color='Symbol',
                          title="Trading Volume")
        st.plotly_chart(fig_volume, use_container_width=True)
        
        # Summary statistics
        st.subheader("Summary Statistics")
        summary = df.groupby('Symbol')['Close'].agg(['mean', 'min', 'max', 'std']).round(2)
        st.dataframe(summary)
