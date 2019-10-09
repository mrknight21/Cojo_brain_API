import json
import datetime
import os
from config import Config
from database.mongo_db_util import Mongo_conn
from newsapi import NewsApiClient
import hashlib
import datetime

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
        self.now = datetime.datetime.now()
        if 'sources' not in kwas:
            self.sources =self.get_local_source_str()
        # self.hasher = eval('hashlib.'+Config.NEWS_ID_HASH)
        # self.salt = Config.HASH_SECRET_SALT

    def get_local_source_str(self, country = 'us'):
        sources_ids = []
        src_str = ""
        source_info = self.news_api.get_sources(country=country)
        if source_info['status'] == 'ok':
            for source in source_info['sources']:
                id = source.get('id', None)
                if id:
                    sources_ids.append(id)
        if sources_ids:
            src_str = ','.join(sources_ids)
        return src_str

    def collect_news(self, mode='headlines', params = None):

        news = []
        page = 1
        if mode == 'headlines':
        # /v2/top-headlines
        # for api params, see: https://newsapi.org/docs/endpoints/top-headlines
            collection = self.news_api.get_top_headlines(language='en', country='nz', page_size=100, )
        if mode == 'general':
        # # /v2/everything
        # for api params, see: https://newsapi.org/docs/endpoints/sources
            collection = self.news_api.get_everything(q='Deep Learning',
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
        mongo_conn = Mongo_conn(['news_store'])
        collector = NewsCollector(mongo_conn)
        news = collector.collect_news()



def tester():
    mongo_conn = Mongo_conn(['news_store'])
    collector  = NewsCollector(mongo_conn)
    print(collector.sources)
    # news = collector.collect_news()
    # if news:
    #     print(len(news))
    #     ids = list(map( lambda  x: NewsCollector.generate_id(x), news))
    #     print(ids)


if __name__ == "__main__":
    tester()