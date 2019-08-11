import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



firekey = "your token"


db_url = "https://cojo-74668.firebaseio.com/"

class db_connect:

    def __init__(self):
        self.firekey = firekey
        self.db = db_url
        self.cred = credentials.Certificate(firekey)
        self.access = firebase_admin.initialize_app(self.cred, {
            'databaseURL': self.db
        })
