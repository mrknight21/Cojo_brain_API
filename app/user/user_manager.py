from firebase_admin import auth
from firebase_admin import db



def user_setup(uid):
    user = auth.get_user(uid)
    ref = db.reference("/user_perm")
    ref.update({uid:{"profile":"Null", "collection":"Null", "self_pref":{"author":"self", "name":"self", "preference":{"size":{"w":1,"l":0.7,"m":0.2,"s":0.1}}}}})

    {
        "collection": {
            "1434134": {
                "author": "jojo",
                "name": "healthy",
                "preference": {
                    "size": {
                        "l": 0.4,
                        "m": 0.3,
                        "s": 0.3,
                        "w": 1
                    }
                }
            }
        },
        "profile": {
            "gender": "male"
        },
        "self_pref": {
            "author": "self",
            "name": "self",
            "preference": {
                "size": {
                    "l": 0.7,
                    "m": 0.2,
                    "s": 0.1,
                    "w": 1
                }
            }
        }
    }