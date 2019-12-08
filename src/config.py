class Config:
    MONGO_DB = 'newsapi_business'
    MONGO_AUTH_DB = os.getenv('MONGO_AUTH_DB')
    MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING') + '/'
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')