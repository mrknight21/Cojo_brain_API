
import json
import datetime
from news_processes.news import News


class NewsRetreiver(object):


    def __init__(self, mongo_db, news_api_key = None, max_load = 2000, analyzers = [], save = False, *argv, **kwas):
        self.max_load = max_load
        self.mongo_db = mongo_db
        self.analyzers = analyzers
        self.now = datetime.datetime.utcnow()

    def retreive_news(self, page_cache):
        return []