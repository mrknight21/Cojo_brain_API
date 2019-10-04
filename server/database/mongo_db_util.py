import pymongo
from config import Config
import sys, os

class Mongo_conn(object):
    default_connection_string = Config.MONGO_DATABASE_URL

    def __init__(self, db_names, connection_string = None):
        if connection_string:
            self.client = pymongo.MongoClient(connection_string)
        else:
            self.client = pymongo.MongoClient(Mongo_conn.default_connection_string)
        self.databases = {}
        for db in db_names:
            self.databases[db] = self.client[db]


    def insert(self, db,collection, data):
        return self.databases[db][collection].insert(data)

    def find_one(self, db, collection, query):
        return self.databases[db][collection].find_one(query)

def mongo_db_test():

    print(Config.NEWS_API_KEY)
    print(Config.MONGO_DATABASE_URL)
    mongo_conn = Mongo_conn(['news_store', 'sample_airbnb'])
    info = mongo_conn.find_one('sample_airbnb', 'listingsAndReviews', {"_id": '10006546'})
    print(info)



if __name__ == "__main__":
    mongo_db_test()

    # print(Config.NEWS_API_KEY)