'''
Docuemt:
utility functions to handle user related tasks.
'''
from database.mongo_db_util import Mongo_conn
from bson.objectid import ObjectId



def quick_check_user_account(user_id, mongo_conn):
    # user_id = str.encode(user_id)
    query = {"_id": ObjectId(str(user_id))}
    return mongo_conn.find_one('Users', query)



if __name__ == "__main__":
    user_id = "5dcf83cc89d63e295d03da12"
    mongo_conn = Mongo_conn()
    json_obj = quick_check_user_account(user_id, mongo_conn)
    print(json_obj)