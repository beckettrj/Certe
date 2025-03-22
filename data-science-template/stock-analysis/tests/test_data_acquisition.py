def test_fetch_historical_data():
    import src.data.data_acquisition as data_acquisition

    # Test fetching historical data for a valid stock symbol
    data = data_acquisition.fetch_historical_data('AAPL', '2022-01-01', '2022-12-31')
    assert data is not None
    assert not data.empty
    assert 'Close' in data.columns

def test_fetch_trading_volume():
    import src.data.data_acquisition as data_acquisition

    # Test fetching trading volume for a valid stock symbol
    volume_data = data_acquisition.fetch_trading_volume('AAPL', '2022-01-01', '2022-12-31')
    assert volume_data is not None
    assert not volume_data.empty
    assert 'Volume' in volume_data.columns

def test_fetch_news_data():
    import src.data.data_acquisition as data_acquisition

    # Test fetching news data for a valid stock symbol
    news_data = data_acquisition.fetch_news_data('AAPL')
    assert news_data is not None
    assert isinstance(news_data, list)  # Assuming news data is returned as a list
    assert len(news_data) > 0  # Ensure there is at least one news item