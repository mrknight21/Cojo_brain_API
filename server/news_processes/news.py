from newsplease import NewsPlease
from newsplease.single_crawler import SingleCrawler
import json
import hashlib
from datetime import datetime

class News(object):

    def __init__(self, raw_info, url, download_time, use_newsapi = True, country = None, category = None):
        self.raw_info = raw_info
        self.news_id = self.generate_news_id(raw_info)
        self.url = url
        self.info_dic = None
        self.country = country
        self.source = self.raw_info['source']
        self.author = self.raw_info['author']
        self.title = self.raw_info['title']
        self.lang = None
        self.domain = None
        self.description = self.raw_info['description']
        self.image_url = self.raw_info['urlToImage']
        if use_newsapi:
            self.published_time = self.parse_api_time_str(self.raw_info['publishedAt'])
        else:
            self.published_time = None
        self.download_time = download_time
        self.tags = {}
        self.bags = {}
        self.short_content = self.raw_info['content']
        if not category:
            self.main_category = "general"
        else:
            self.main_category = category
        self.categories = []
        self.article_obj = None

    def parse_api_time_str(self, time_str):
        '''
        :param time_str: a string from api timestamp, e.g. 2019-09-23T08:48:54Z
        :return: a python datetime object
        '''
        time_str = time_str[:19]
        try:
            time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
            return time_obj
        except ValueError as e:
            print(time_str+ " " +e)
            return None

    def to_dic(self):
        self.info_dic = {
            'country': self.country,
            'source': self.source,
            'source_domain': self.domain,
            'language': self.lang,
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'urlToImage': self.image_url,
            'publishedAt': self.published_time,
            'downloadedAt': self.download_time,
            'tag': self.tags,
            'bag': self.bags,
            'main_category': self.main_category,
            'categories': self.categories
        }
    def out_put_json(self):
        if self.info_dic:
            json_obj = json.dumps(self.info_dic)
            return json_obj
        else:
            self.to_dic()
            json_obj = json.dumps(self.info_dic)
            return json_obj

    def get_article_obj(self):
        self.article_obj = NewsPlease.from_url(self.url)
        if self.article_obj:
            self.lang = self.article_obj.language
            self.domain = self.article_obj.source_domain

    def get_article_full_text(self):
        if not self.article_obj:
            self.get_article_obj()
        return self.article_obj.text

    def generate_news_id(self, raw_info, digits = 18):
        title = raw_info['title']
        url = raw_info['url']
        # salt = 'bryanhandsome'
        concat_str = title + str(url)
        hashed_id = hashlib.sha224(concat_str.encode('utf-8')).hexdigest()
        id_str = hashed_id[:digits]
        return id_str


    def fill_object_with_news_please(self):
        if not self.article_obj:
            self.get_article_obj()
        pass

