from config import Config
import requests
from db import MongoAdapter
import math


class DataGatherer:
    def __init__(self):
        self.business_url = Config.INDIAN_BNEWS_URL_BASE
        self.api_key = Config.NEWS_API_KEY

    def indian_business_news(self):
        res = requests.get(self.business_url + '&pageSize=100&apiKey=' + self.api_key).json()
        total_results = res['totalResults']

        # TODO: create Id by hashing the titles so that there are no duplicate news
        # 100 is the max pagesize for newsapi.org
        if total_results <=100:
            client = MongoAdapter().get_mongo_client()
            collection = client[Config.MONGO_DB][Config.NEWS_COLLECTION]
            collection.insert_many(res['articles'])
        else:
            # break them in chunks of 10
            number_of_pages = math.ceil(total_results)/10
            client = MongoAdapter().get_mongo_client()
            collection = client[Config.MONGO_DB][Config.NEWS_COLLECTION]
            for page in range(1, number_of_pages):
                res = requests.get(
                    self.business_url + \
                    '&pageSize=10&page={}&apiKey='.format(page) + \
                    self.api_key).json()
                collection.insert_many(res['articles'])


