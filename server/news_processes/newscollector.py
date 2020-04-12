import json
import datetime
import os
from config import Config
# from database.mongo_db_util import Mongo_conn
from database.firebase_db_util import Firebase_conn
from newsapi import NewsApiClient
from analyzers.simple_analyzer import SimpleAnalyzer
from news_processes.news import News
import hashlib
import datetime

class NewsCollector(object):

    CATEGORY = ['business', 'entertainment', 'general', 'health', 'science', 'sports' ,'technology']

    def __init__(self, db_conn, news_api_key = None, max_load = 2000, analyzers = [], save = False, country = None,*argv, **kwas):
        if news_api_key:
            self.news_api = NewsApiClient(api_key=news_api_key)
        elif Config.NEWS_API_KEY:
            self.news_api = NewsApiClient(api_key=Config.NEWS_API_KEY)
        else:
            raise Exception('No API KEY')
        self.save = save
        self.country = country
        self.max_load = max_load
        self.db_conn = db_conn
        self.analyzers = analyzers
        self.now = datetime.datetime.utcnow()
        if 'sources' not in kwas:
            self.sources =self.get_country_source_str()

    def collect_news(self, mode='headlines', country = None, category = None):
        processed_news_count = 0
        total_news_count = 0
        cur_page = 1
        total = 0
        download_time = self.now
        bacth_collection = self.get_batch_news_api_call(mode = mode, page=cur_page, country = country,category = category)
        status = False
        if bacth_collection['status'] == 'ok':
            status = True
            total_news_count = bacth_collection['totalResults']
        else:
            raise Exception('Abnormal response from API. code: {}'.format(bacth_collection['status']))
        # Looping through the pages from the API
        while(status and processed_news_count < total_news_count):
            if cur_page > 1:
                bacth_collection = self.get_batch_news_api_call(mode = mode, page=cur_page, country = country, category = category)
                download_time = datetime.datetime.utcnow()
            batch_news =  bacth_collection['articles']
            parsed_news_data, flag = self.batch_process_news(batch_news, download_time = download_time, country = country, category = category)
            if flag and self.save:
                self.news_dump(parsed_news_data)
            processed_news_count += len(batch_news)
            cur_page += 1

    def get_country_source_str(self, country = None):
        if not country:
            country = self.country
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

    def get_batch_news_api_call(self, mode = "headlines", page= 1, country = None, category = None):
        collection = {}
        if mode == 'headlines':
            # /v2/top-headlines
            # for api params, see: https://newsapi.org/docs/endpoints/top-headlines
            if not country:
                collection = self.news_api.get_top_headlines(sources=self.sources, page_size=100, page=page, category = category)
            else:
                collection = self.news_api.get_top_headlines(country = country, page_size=100, page=page, category=category)
        if mode == 'general':
            # # /v2/everything
            # for api params, see: https://newsapi.org/docs/endpoints/sources
            if not country:
                collection = self.news_api.get_everything(sources=self.sources, sort_by='relevancy', page=page, category = category)
            else:
                collection = self.news_api.get_everything(country = country, sort_by='relevancy', page=page, category = category)
        return collection


    def batch_process_news(self, batch_raw_content, download_time = None, country = None, category = None, thread = 5):
        if not country:
            country = self.country
        batch_container = []
        flag = True
        if not download_time:
            download_time = datetime.datetime.utcnow()
        for news_info in batch_raw_content:
            try:
                news = News(news_info, news_info['url'], download_time, country= country, category = category)
                content = news.get_article_full_text()
                news.tags = self.tag_news(content)
                news.to_dic()
                # json_obj = news_api.out_put_json()
                batch_container.append((news.news_id, news.info_dic))
                print("Scraped and processed article: {}".format(news.title) )
            except Exception as e:
                print("Failed scraping article: {}".format(news.title))
                print("due to :{}".format(e))
                continue
        return batch_container, flag

    def tag_news(self, content):
        tags = {}
        for analyzer in self.analyzers:
            tags.update(analyzer.single_analyze(content))
        return tags

    def news_dump(self, news_data):
        flag = False
        try:
            self.db_conn.bulk_insert(news_data, 'news_articles', )
            flag = True
        except Exception as e:
            print(e)
        if flag:
            print("Successfully uploaded {} of news into database".format(len(news_data)))


def tester():
    countries = ['us', 'nz']
    db_conn = Firebase_conn()
    simple_analyzer = SimpleAnalyzer()
    collector  = NewsCollector(db_conn, analyzers=[simple_analyzer], save = True, country = 'us')
    print(collector.sources)
    for c in countries:
        for cat in collector.CATEGORY:
            collector.collect_news(country = c, category= cat)

if __name__ == "__main__":
    tester()