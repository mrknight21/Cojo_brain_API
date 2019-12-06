from users.user import User
from datetime import datetime, timedelta
from database.mongo_db_util import Mongo_conn
import hashlib, random, string


class Member(User):

    def __init__(self, mongo_db, user_id, auth_token, time = None, location = None, page_id = 1):
        self.mongo_db = mongo_db
        self.user_id = user_id
        self.auth = self.authenticate_user()
        self.auth_token = auth_token
        self.has_loggin = self.check_loggin(user_id, auth_token)
        if time:
            self.cur_time = time
        else:
            self.cur_time = datetime.utcnow()

    def authenticate_user(self):
        return True

    def check_loggin(self, user_id, auth_token):
        return True

    def generate_new_auth_token(self, digits = 12):
        now_str = datetime.utcnow().strftime("%m/%d/%YT%H:%M:%S")
        concat_str = self.user_id + now_str + random.choice(string.ascii_letters)+ random.choice(string.ascii_letters)
        hashed_id = hashlib.sha224(concat_str.encode('utf-8')).hexdigest()
        id_str = hashed_id[:digits]
        return id_str



    def retreive_news_ids_from_cache(self, page_id):
        pass

    def create_news_cache(self):
        self.auth_token = self.generate_new_auth_token()
        cache = {'created': datetime.utcnow(), 'auth_token':self.auth_token, 'ranked_page':{}}
        query = self.prepare_news_query()
        all_news = self.mongo_db.find_many('News_pool', query)
        ranked_news = self.rank_and_page(all_news)
        cache['ranked_page'] = ranked_news
        return cache

    def prepare_news_query(self, days = 3):
        end = datetime.utcnow()
        start = end - timedelta(days=days)
        q = {
            'publishedAt':{'$gte': start, '$lt': end}
        }
        return q

    def rank_and_page(self, news, news_per_page = 50):
        ranked_news_in_page = {}
        news = sorted(news, key = lambda x: x['publishedAt'])
        news_count = len(news)
        number_pages = news_count // news_per_page +1
        for p in range(number_pages):
            page_id = p+1
            page_list = []
            end_index = news_per_page * page_id
            if end_index > news_count:
                end_index = news_count
            start_index = (page_id -1)* news_per_page
            batch_news = news[start_index:end_index]
            for n in batch_news:
                n_id = n['_id']
                interaction = {'read': False}
                single_news = {'_id': n_id , 'interaction': interaction}
                page_list.append(single_news)
            ranked_news_in_page[page_id] =page_list
        return ranked_news_in_page




if __name__ == "__main__":
    mongo_db = Mongo_conn()
    m = Member(mongo_db, 1, 1)
    news = m.create_news_cache()
    print(list(news))