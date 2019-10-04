import json
import datetime
import os
from config import Config
from database.mongo_db_util import Mongo_conn
from newsapi import NewsApiClient
import hashlib

class NewsCollector(object):

    def __init__(self, mongo_db, news_api_key = None, get_content = False, max_load = 2000, analyzer = None, *argv, **kwas):
        if news_api_key:
            self.news_api = NewsApiClient(api_key=news_api_key)
        elif Config.NEWS_API_KEY:
            self.news_api = NewsApiClient(api_key=Config.NEWS_API_KEY)
        else:
            raise Exception('No API KEY')
        self.max_load = max_load
        self.get_content = get_content
        self.mongo_db = mongo_db
        self.analyzer = analyzer
        # self.hasher = eval('hashlib.'+Config.NEWS_ID_HASH)
        # self.salt = Config.HASH_SECRET_SALT

    def collect_news(self, mode='general', params = None):

        news = []
        if mode == 'headlines':
        # /v2/top-headlines
        # for api params, see: https://newsapi.org/docs/endpoints/top-headlines
            collection = self.news_api.get_top_headlines(q='Deep Learning', language='en', country='us')
        if mode == 'general':
        # # /v2/everything
        # for api params, see: https://newsapi.org/docs/endpoints/sources
            collection = self.news_api.get_everything(q='Deep Learning',
                                                  from_param='2019-10-01',
                                                  to='2019-10-03',
                                                  language='en',
                                                  sort_by='relevancy',
                                                  page=1)
        if collection['status'] == 'ok':
            print('Number of articles collected: {}'.format(collection['totalResults']))
            return collection['articles']
        else:
            print ('Collection status'.format(collection['status']))
            return None


    @staticmethod
    def generate_id(new):
        title = new['title']
        created = new['publishedAt']
        salt = 'bryanhandsome'
        concat_str = title+str(created)+str(salt)
        hashed_id = hashlib.sha224(concat_str.encode('utf-8')).digest()
        return hashed_id


    def mongo_news_dump(self, news):
        pass



def tester():
    mongo_conn = Mongo_conn(['news_store'])
    collector  = NewsCollector(mongo_conn)
    news = collector.collect_news()
    if news:
        print(len(news))
        ids = list(map( lambda  x: NewsCollector.generate_id(x), news))
        print(ids)


if __name__ == "__main__":
    tester()