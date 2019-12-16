import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    MONGO_DB = 'news_api'
    NEWS_COLLECTION = 'business'
    MONGO_AUTH_DB = os.getenv('MONGO_AUTH_DB')
    MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING') + '/'
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    INDIAN_BNEWS_URL_BASE = 'https://newsapi.org/v2/top-headlines?country=in&category=business'
    SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK')

