import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
env_path = '/cojo.env'
load_dotenv(dotenv_path=basedir+env_path)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_DATABASE_URL = os.environ.get('MONGO_CONNECTION')
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
    NEWS_ID_HASH = os.environ.get('NEWS_ID_HASH')
    HASH_SECRET_SALT = os.environ.get('HASH_SECRET_SALT')



if __name__ == "__main__":
    print (basedir+env_path)
    print(Config.NEWS_API_KEY)

