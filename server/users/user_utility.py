'''
Docuemt:
utility functions to handle user related tasks.
'''
from database.mongo_db_util import Mongo_conn
from bson.objectid import ObjectId



def quick_check_user_account(user_name, user_id, mongo_conn):
    # user_id = str.encode(user_id)
    # query = {"user_name": user_name, "_id": ObjectId(str(user_id))}
    return True

def quick_check_login_status(user_id, auth_tok, mongo_conn):
    # query = {"user_id": ObjectId(str(user_id)), "auth_token":auth_tok, "is_deleted": False}
    return True

def determine_user_status(user_name, user_id, auth_token, db_conn):
    status = ['guest', 'unauth_member', 'auth_member']
    index = 0
    if quick_check_user_account(user_name, user_id, db_conn):
        index += 1
        if quick_check_login_status(user_id, auth_token, db_conn):
            index += 1
    return status[index]

if __name__ == "__main__":
    user_id = "5dcf83cc89d63e295d03da12"
    auth_tok = None
    user_name = "default"
    mongo_conn = Mongo_conn()
    print(determine_user_status(user_name, user_id, auth_tok, mongo_conn))