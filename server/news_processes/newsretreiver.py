
import json
import datetime
from news_processes.news import News
from bson.objectid import ObjectId

class NewsRetreiver(object):

    def __init__(self, db, max_load = 2000, *argv, **kwas):
        self.max_load = max_load
        self.db = db
        self.now = datetime.datetime.utcnow()

    # def construct_news_page(self, page_cache):
    #     ranked_news = None
    #     page, news_ids = self.parsing_single_page_cache(page_cache)
    #     news_lst = self.retreive_news(news_ids)
    #     if news_lst:
    #         for news_obj in news_lst:
    #             try:
    #                 id = news_obj['_id']
    #                 page[id].update(news_obj)
    #                 page[id]['_id'] = str(page[id]['_id'])
    #                 page[id]['publishedAt'] = self.time_parser(page[id]['publishedAt'])
    #                 page[id]['downloadedAt'] = self.time_parser(page[id]['downloadedAt'])
    #             except Exception:
    #                 pass
    #             if not self.validate_news_obj(page[id]):
    #                 del page[id]
    #         ranked_news = sorted(page.values(), key = lambda x: x['rank'])
    #     return ranked_news

    def retreive_news(self, news_ids):
        assert isinstance(news_ids[0], ObjectId)
        query = { '_id': {'$in': news_ids}}
        try:
            return self.mongo_db.find_many('News_pool', query)
        except Exception as e:
            print(e)
            return None

    def parsing_single_page_cache(self, page_cache):
        page = { news_cache['_id']:{'_id':str(news_cache['_id']) ,'rank': rank, 'interaction':news_cache['interaction']} for rank, news_cache in enumerate(page_cache)}
        news_ids = list(page.keys())
        return page, news_ids

    def time_parser(self, time_obj, time_format = "%m/%d/%Y, %H:%M:%S"):
        return time_obj.strftime(time_format)

    def validate_news_obj(self, news_obj):
        valid = True
        if not news_obj['_id']: valid = False
        if not news_obj['news_id']: valid = False
        if not news_obj['url']: valid = False
        if not news_obj['main_category']: valid = False
        return valid