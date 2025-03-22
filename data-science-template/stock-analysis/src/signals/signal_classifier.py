def classify_signal(price_change, volume_change):
    """
    Classifies market signals into weak and strong based on price and volume changes.

    Parameters:
    - price_change (float): The percentage change in stock price.
    - volume_change (float): The percentage change in trading volume.

    Returns:
    - str: 'strong' if the signal is strong, 'weak' if the signal is weak.
    """
    if abs(price_change) > 5 and volume_change > 50:
        return 'strong'
    elif abs(price_change) < 1 and volume_change < 10:
        return 'weak'
    else:
        return 'neutral'


def analyze_sentiment(news_article):
    """
    Analyzes the sentiment of a news article to determine its potential impact on stock signals.

    Parameters:
    - news_article (str): The text of the news article.

    Returns:
    - float: A sentiment score ranging from -1 (negative) to 1 (positive).
    """
    # Placeholder for sentiment analysis logic
    # In a real implementation, you would use a library like TextBlob or VADER
    return 0.0  # Neutral sentiment as a placeholder


def classify_news_signal(news_article):
    """
    Classifies the impact of a news article on stock signals based on sentiment analysis.

    Parameters:
    - news_article (str): The text of the news article.

    Returns:
    - str: 'strong' if the news is likely to have a strong impact, 'weak' otherwise.
    """
    sentiment_score = analyze_sentiment(news_article)
    if sentiment_score > 0.5:
        return 'strong'
    elif sentiment_score < -0.5:
        return 'weak'
    else:
        return 'neutral'