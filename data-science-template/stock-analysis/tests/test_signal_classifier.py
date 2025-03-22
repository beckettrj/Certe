def test_classify_signal():
    from src.signals.signal_classifier import classify_signal

    # Test case for a strong signal
    strong_signal = {
        'price_change': 5.0,
        'volume_change': 100000,
        'news_sentiment': 0.8
    }
    assert classify_signal(strong_signal) == 'strong'

    # Test case for a weak signal
    weak_signal = {
        'price_change': 0.5,
        'volume_change': 5000,
        'news_sentiment': 0.2
    }
    assert classify_signal(weak_signal) == 'weak'

    # Test case for a borderline signal
    borderline_signal = {
        'price_change': 2.0,
        'volume_change': 20000,
        'news_sentiment': 0.5
    }
    assert classify_signal(borderline_signal) == 'weak'  # Assuming the threshold is set to classify as weak

    # Additional test cases can be added as needed to cover more scenarios.