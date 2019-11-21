'''
Schema for news json store in mongo db, refer to OpenAPI document

news_obj = {
        'source': {'id': None, 'name': None},
        'author':None,
        'title': None,
        'description': None,
        'url': None,
        'urlToImage': None,
        'publishedAt': None,
        'tag':
                {'polarity': float,
                 'subjectivity': float,
                 ......}
        'bag':{
            'who':[{'word': str, 'polarity': float, 'type': str}]
            'where': [{'word': str, 'polarity': float, 'geolocation': ??}]
            'when'[]
            ''
        }
        'categories': [str list],
    }
'''

from newsplease import NewsPlease
import json
import hashlib

class News(object):

    def __init__(self, raw_info, url, download_time):
        self.raw_info = raw_info
        self.news_id = self.generate_news_id(raw_info)
        self.url = url
        self.info_dic = None
        self.source = None
        self.author = None
        self.title = None
        self.description = None
        self.image_url = None
        self.published_time = None
        self.download_time = None
        self.tag = {}
        self.bag = {}
        self.main_category = "general"
        self.categories = []


    def to_dic(self):
        self.info_dic = {
            'news_id': self.news_id,
            'source': self.source,
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'urlToImage': self.image_url,
            'publishedAt': self.published_time,
            'downloadedAt': self.download_time,
            'tag': self.tags,
            'bag': self.bag,
            'main_category': self.main_category,
            'categories': self.categories
        }
    def out_put_json(self):
        if self.info_dic:
            json_obj = json.dump(self.info_dic)
            return json_obj
        else:
            return

    def get_article_obj(self):
        self.article_obj = NewsPlease.from_url(self.url)

    def get_article_full_text(self):
        if not self.article_obj:
            self.get_article_obj()
        return self.article_obj.text

    def generate_news_id(self, raw_info):
        title = raw_info['title']
        url = raw_info['url']
        # salt = 'bryanhandsome'
        concat_str = title + str(url)
        hashed_id = hashlib.sha224(concat_str.encode('utf-8')).digest()
        return hashed_id


    def fill_object_with_news_please(self):
        if not self.article_obj:
            self.get_article_obj()
        pass
