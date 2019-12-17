from config import Config
import requests
from db import MongoAdapter
import math
from bson.objectid import ObjectId
import hashlib
from util.log import Logger
from datetime import datetime
from tzlocal import get_localzone
from pymongo.errors import DuplicateKeyError


class DataGatherer:
    def __init__(self):
        self.business_url = Config.INDIAN_BNEWS_URL_BASE
        self.api_key = Config.NEWS_API_KEY
        self.client = MongoAdapter().get_mongo_client()
        self.news_collection = self.client[Config.MONGO_DB][Config.NEWS_COLLECTION]
        self.inserted_articles = 0
        self.total_articles = 0
        self.not_inserted_articles = 0

    def indian_business_news(self):
        res = requests.get(self.business_url + '&pageSize=100&apiKey=' + self.api_key).json()
        total_results = res['totalResults']
        self.total_articles = int(total_results)

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
        if self.inserted_articles > 0:
            Logger.info('News data stored successfully!\nTotal articles: {}\nInserted articles: {}'.format(self.total_articles, self.inserted_articles), push_to_slack=True)
        else:
            Logger.info('Total articles: {}\nNot inserted articles: {}'.format(self.total_articles, self.not_inserted_articles))
                

    def insert_data_into_db(self, articles: list):
        self.total_articles = len(articles)
        for article in articles:
            article['_id'] = ObjectId(hashlib.md5(article['title'].encode()).hexdigest()[8:])
            article['createdDate'] = datetime.now().astimezone(get_localzone())
            try:
                self.news_collection.insert_one(article)
                self.inserted_articles = self.inserted_articles + 1
            except DuplicateKeyError as err:
                self.not_inserted_articles = self.not_inserted_articles + 1
