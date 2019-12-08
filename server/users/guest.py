from users.user import User

class Guest(User):

    def __init__(self, user_id, time = None, location = None, page_index = 1):
        super()._init_(user_id)

    def retreive_from_cache(self, user_id):
        pass


def main():
    print ('hello')


if __name__ == '__main__':
    main()