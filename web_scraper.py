import feedparser

def fetch_news():
    categories = {
        'Top Stories': 'https://news.google.com/news/rss',
        'World': 'https://news.google.com/news/rss/headlines/section/topic/WORLD',
        'Business': 'https://news.google.com/news/rss/headlines/section/topic/BUSINESS',
        'Technology': 'https://news.google.com/news/rss/headlines/section/topic/TECHNOLOGY',
        'Entertainment': 'https://news.google.com/news/rss/headlines/section/topic/ENTERTAINMENT',
        'Sports': 'https://news.google.com/news/rss/headlines/section/topic/SPORTS',
        'Science': 'https://news.google.com/news/rss/headlines/section/topic/SCIENCE',
        'Health': 'https://news.google.com/news/rss/headlines/section/topic/HEALTH'
    }

    news_dict = {}

    for category, url in categories.items():
        feed = feedparser.parse(url)
        news_dict[category] = [entry.title for entry in feed.entries[:3]]

    return news_dict