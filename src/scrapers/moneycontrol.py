import pandas as pd
from bs4 import BeautifulSoup
import requests as r
from config import Config
# from util.selenium_dispatcher import SeleniumDispatcher
from db.mongo_adapter import MongoAdapter
from util.log import Logger
from datetime import datetime
from tzlocal import get_localzone
from bson.objectid import ObjectId
import hashlib
from pymongo.errors import DuplicateKeyError


class MoneyControl:
    def __init__(self) -> None:
        self.client = MongoAdapter().get_mongo_client()
        self.news_collection = self.client[Config.MONGO_DB][Config.NEWS_COLLECTION]
        self.news_details_collection = self.client[Config.MONGO_DB][Config.NEWS_DETAILS_COLLECTION]
        self.source = 'moneycontrol'

    def filter_results_from_source(self):
        cur = self.news_collection.aggregate([
            {
                '$addFields':
                {
                    "urlMatch":
                    {
                        '$regexMatch':
                                {
                                    'input': "$url",
                                    'regex': self.source
                                }
                    }
                }
            }
            ,
            {
                '$match':
                {
                    'urlMatch': True
                }
            }
            ,
            {
                '$project':
                {
                    'url': 1
                }
            }
        ])

        objs = {}
        for dat in cur:
            # print(dat)
            id = dat['_id']
            url = dat['url']
            # print(id, url)
            objs[id] = url 

        urls = list(objs.values())
        ids = list(objs.keys())

        return ids, urls



    def insert_data_into_db(self, item: dict):
            tz = get_localzone()
            item['_id'] = ObjectId(hashlib.md5(item['title'][10:].encode()).hexdigest()[8:])
            item['createdDate'] = tz.localize(datetime.now())
            try:
                self.news_details_collection.insert_one(item)
            except DuplicateKeyError as duperr:
                Logger.err(f'Record with data: {item} already exists, skipping!')
            except Exception as err:
                Logger.err(f'Error while inserting record: {item} into DB. Error: {str(err)}')


    def run_scraper(self):

        ids, urls = self.filter_results_from_source()

        for id, url in zip(ids, urls):

            try:
                res = r.get(url)
                html_str = res.content
                bs = BeautifulSoup(html_str, 'html.parser')
                title = bs.find_all(class_="article_title artTitle")[0].text
                subtitle = bs.find_all(class_="article_desc")[0].text

                content_div = bs.find_all('div', class_="content_wrapper arti-flow")
                content = ''
                for p in  content_div[0].find_all('p'):
                    content = content + p.text + '\n'

                item = {
                    'newsId': id,
                    'title': title,
                    'subtitle': subtitle,
                    'content': content,
                    'source': self.source
                }

                self.insert_data_into_db(item)
            
            except Exception as ex:
                Logger.err(f'Error while scraping url: {url}. Error: {str(ex)}')
                continue
