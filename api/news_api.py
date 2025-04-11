import requests
from config import NEWS_API_KEY, NEWS_API_URL

def fetch_financial_news(query):
    params = {
        'q': query,
        'apiKey': NEWS_API_KEY,
        'language': 'en',
        'sortBy': 'relevancy',
    }
    response = requests.get(NEWS_API_URL, params=params)
    return response.json()