


class User(object):

    def __init__(self, user_id, time = None, location = None, page_index = 1):
        self.user_id = user_id
        self.auth = self.authenticate_user(user_id)

    def authenticate_user(self, user_id):
        pass