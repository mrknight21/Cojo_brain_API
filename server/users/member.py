from users.user import User

class Member(User):

    def __init__(self, user_id, auth_token, time = None, location = None, page_id = 1):
        self.user_id = user_id
        self.auth = self.authenticate_user(user_id)
        self.has_loggin = self.check_loggin(user_id, auth_token)
        self.cur_time = time
        self.page_id = page_id

    def authenticate_user(self, user_id):
        return True

    def retreive_from_cache(self):
        pass

    def rank_news(self):
        pass

    def check_loggin(self, user_id, auth_token):
        return True