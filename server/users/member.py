from users.user import User
from datetime import datetime, timedelta
from database.mongo_db_util import Mongo_conn
from database.firebase_db_util import Firebase_conn, Firestore_order, Firestore_query
import hashlib, random, string
from ranker.ranking_util import *
from users.user_utility import *

class Member(User):
    # Unit is hours
    EXPIRED_DURATION = 2
    NEWS_BATCH_SIZE = 40

    def __init__(self, db_conn, user_id, user_name=None, auth_token=None, time = None, location = None, page_id = 1):
        self.db_conn = db_conn
        self.user_id = user_id
        self.user_name = user_name
        self.is_member = quick_check_user_account(self.user_name, self.user_id, self.db_conn)
        self.auth_token = auth_token
        self.has_loggin = quick_check_login_status(self.user_id, self.auth_token, self.db_conn)
        self.firestore_obj = None
        try:
            self.firestore_obj = self.db_conn.find_one(doc_id=self.user_id, collection='users')._data
        except Exception as e:
            self.firestore_obj = None
        if time:
            self.cur_time = time
        else:
            self.cur_time = datetime.utcnow()

    def validate_expiration(self, cache, duration = 3):
        # Disable time validation for testing purpose
        # if cache['created']  < datetime.utcnow()- timedelta(hours=duration):
        #     return  False
        # else:
        #     return  True
        return True


    def retreive_from_cache(self, page_id):
        try:
            # if self.is_member and self.has_loggin:
            #     query = {'user_id': ObjectId(self.user_id), 'auth_token': self.auth_token, "is_deleted": False}
            #     user_cache = self.mongo_db.find_one('Users_caches', query)
            #     if user_cache and self.validate_expiration(user_cache, duration=  timedelta(hours=Member.EXPIRED_DURATION)):
            #         total_page = len(user_cache['ranked_page']) -1
            #         page_cache = user_cache['ranked_page'][str(page_id)]
            #         return  page_cache, total_page
            return [], 0
        except Exception:
            return [], 0

    def generate_new_auth_token(self, digits = 12):
        now_str = datetime.utcnow().strftime("%m/%d/%YT%H:%M:%S")
        concat_str = self.user_id + now_str + random.choice(string.ascii_letters)+ random.choice(string.ascii_letters)
        hashed_id = hashlib.sha224(concat_str.encode('utf-8')).hexdigest()
        id_str = hashed_id[:digits]
        return id_str

    # def retreive_news_ids_from_cache(self, page_id):

    def create_news_cache(self, reset = True):
        # self.auth_token = self.generate_new_auth_token()
        cur_news = []
        cur_news = self.firestore_obj['news_caches']['ranked_news']
        number_of_news_required = self.NEWS_BATCH_SIZE + len(cur_news)
        query = self.prepare_news_query()
        order = Firestore_order(field='publishedAt')
        all_news = self.db_conn.find_many('news_articles', query, order_by = order, limit=number_of_news_required)
        ranked_news = self.simple_rank(all_news, insert_article_content=True, cur_news = cur_news, quota = number_of_news_required, reset = reset)
        if not reset:
            ranked_news = cur_news + ranked_news
        return ranked_news

    def update_news_cache(self, ranked_news):
        cache = {'created': datetime.utcnow(), 'ranked_news': {}, 'is_deleted': False, 'ranked_news_ref':{}}
        if self.firestore_obj and ranked_news:
            cache['ranked_news'] = ranked_news
            cache['ranked_news_ref'] = self.generate_news_ref(ranked_news)
            cache['ranked_news_id_only'] = self.generate_news_id_only(ranked_news)
            self.firestore_obj['news_caches'] = cache
            self.db_conn.insert(data = self.firestore_obj, collection = 'users', doc_id = self.user_id)
            del cache['ranked_news_ref']
            del cache['ranked_news_id_only']

    def generate_news_ref(self, ranked_news):
        refs = []
        for news in ranked_news:
            n_id = news['news_id']
            ref = self.db_conn.cli.collection('news_article').document(n_id)
            refs.append({'news_id': news['news_id'], 'rank': news['rank'], 'reference':ref})
        return refs

    def generate_news_id_only(self, ranked_news):
        news_id_only = []
        for news in ranked_news:
            news_id_only.append({'news_id': news['news_id'], 'rank': news['rank']})
        return news_id_only

    def prepare_news_query(self, days = 3):
        queries = []
        end = datetime.utcnow()
        start = end - timedelta(days=days)
        queries.append(Firestore_query('publishedAt', '>', start))
        return queries

    def simple_rank(self, news, insert_article_content = False, cur_news = None, variation=5, quota = 40, reset=True):
        cur_rank = 0
        cur_news_id = []
        ranked_news = []
        if not reset:
            cur_rank = max(cur_news, key = lambda x: x['rank'])['rank']
        else:
            quota = self.NEWS_BATCH_SIZE
        cur_news_id = list(map(lambda x: x['news_id'], cur_news))
        news = [(doc.id, doc.to_dict()) for doc in news]
        news = sorted(news, key = lambda x: x[1]['publishedAt'])
        if variation >0:
            news = introduce_variation(news, variation = variation)
        for n in news:
            n_id = n[0]
            content = n[1]
            if n_id in cur_news_id: continue
            cur_rank += 1
            if cur_rank > quota: break
            single_news = {'news_id': n_id, 'rank': cur_rank}
            if insert_article_content:
                single_news['content'] = content
            ranked_news.append(single_news)
        return ranked_news

    def return_non_loggin_info(self):
        return "Guest mode still under development"