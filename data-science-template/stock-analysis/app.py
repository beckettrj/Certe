import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from scripts.fetch_market_data import fetch_market_data
import plotly.express as px

st.set_page_config(page_title="Stock Analysis", layout="wide")

def main():
    st.title("Stock Market Analysis Tool")
    
    tab1, tab2, tab3 = st.tabs(["Data Fetcher", "Backtesting", "Visualizer"])
    
    with tab1:
        st.header("Market Data Fetcher")
        symbols = st.text_input("Enter stock symbols (comma-separated)", "SPY,AAPL,MSFT")
        if st.button("Fetch Data"):
            with st.spinner("Fetching market data..."):
                file_path = fetch_market_data(
                    symbols=symbols.split(','),
                    start_date=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
                    end_date=datetime.now().strftime('%Y-%m-%d')
                )
                st.success(f"Data saved successfully to {file_path}")
    
    with tab2:
        st.header("Backtesting")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365))
        with col2:
            end_date = st.date_input("End Date", datetime.now())
        
        if st.button("Run Backtest"):
            st.info("Backtesting functionality coming soon!")
            
    with tab3:
        st.header("Data Visualizer")
        try:
            df = pd.read_csv('data/market_data.csv')
            symbols = df['Symbol'].unique()
            selected_symbol = st.selectbox("Select Symbol", symbols)
            
            symbol_data = df[df['Symbol'] == selected_symbol]
            fig = px.line(symbol_data, x='Date', y='Close', title=f'{selected_symbol} Price History')
            st.plotly_chart(fig)
        except Exception as e:
            st.error("Please fetch some data first!")

if __name__ == "__main__":
    main()
