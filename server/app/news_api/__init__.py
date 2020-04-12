from flask import Blueprint
from database.firebase_db_util import Firebase_conn


bp = Blueprint('news_api', __name__)
frb_bd = Firebase_conn(base_collection='news_articles')

from app.news_api import routes