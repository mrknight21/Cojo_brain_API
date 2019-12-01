import pymongo
from config import Config

class Mongo_conn(object):
    CONNECTION_STRING = Config.MONGO_DATABASE_URL
    COJODATABASE = 'news_store'

    def __init__(self, db_name = None, connection_string = None):
        if connection_string:
            self.client = pymongo.MongoClient(connection_string)
        else:
            self.client = pymongo.MongoClient(Mongo_conn.CONNECTION_STRING)
        if db_name:
            self.db_name = db_name
            self.db_conn = self.client[db_name]
        else:
            self.db_name = Mongo_conn.COJODATABASE
            self.db_conn = self.client[Mongo_conn.COJODATABASE]

    def insert(self, db, collection, data):
        self.db_conn[collection].insert(data)

    def bulk_insert(self, collection, data_list):
        self.db_conn[collection].insert_many(data_list)

    def find_one(self, collection, query):
        return self.db_conn[collection].find_one(query)

    def check_existence(self, collection, query):
        pass

def mongo_db_test():

    print(Config.NEWS_API_KEY)
    print(Config.MONGO_DATABASE_URL)
    mongo_conn = Mongo_conn(['news_store', 'sample_airbnb'])
    info = mongo_conn.find_one('sample_airbnb', 'listingsAndReviews', {"_id": '10006546'})
    print(info)



if __name__ == "__main__":
    mongo_db_test()

    # print(Config.NEWS_API_KEY)