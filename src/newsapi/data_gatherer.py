from config import Config
import requests
from db import MongoAdapter
import math
from bson.objectid import ObjectId
import hashlib
from util.log import Logger


class DataGatherer:
    def __init__(self):
        self.business_url = Config.INDIAN_BNEWS_URL_BASE
        self.api_key = Config.NEWS_API_KEY
        self.client = MongoAdapter().get_mongo_client()
        self.news_collection = self.client[Config.MONGO_DB][Config.NEWS_COLLECTION]

    def indian_business_news(self):
        res = requests.get(self.business_url + '&pageSize=100&apiKey=' + self.api_key).json()
        total_results = res['totalResults']

        # TODO: create Id by hashing the titles so that there are no duplicate news
        # 100 is the max pagesize for newsapi.org
        if total_results <=100:
            self.insert_data_into_db(res['articles'])
        else:
            # break them in chunks of 10
            number_of_pages = math.ceil(total_results)/10
            collection = self.client[Config.MONGO_DB][Config.NEWS_COLLECTION]
            for page in range(1, number_of_pages):
                res = requests.get(
                    self.business_url + \
                    '&pageSize=10&page={}&apiKey='.format(page) + \
                    self.api_key).json()
                self.insert_data_into_db(res['articles'])
        Logger.info('News data stored successfully!', push_to_slack=True)
                

    def insert_data_into_db(self, articles: list):
        for article in articles:
            article['_id'] = ObjectId(hashlib.md5(article['title'].encode()).hexdigest()[8:])
            self.news_collection.insert_one(article)

