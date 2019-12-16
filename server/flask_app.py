# -*- coding: utf-8 -*-
"""
@author: bryan chen
"""

import pickle
from flask import Flask, request
from config import Config
# from flasgger import Swagger
import os, sys, json
from users import  *
from users.user_utility import *
from news_processes.newsretreiver import NewsRetreiver
from database.mongo_db_util import Mongo_conn

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir)

app = Flask(__name__)
app.config.from_object(Config)
mongo_db = Mongo_conn()
# swagger = Swagger(app)


# Argument for request.form:
# user_id : string
# time: 2019-11-30T16:14:00Z
#
# Return:
# array:
# [
#   news_json_objects
# ]
# logic:
# 1. classify user as member or guests
# 2. get user cache_news
# 3. If no cache_news or if news expire: create news cache, and set page_id to 1
# 4. If valid news cache retreived, then retreive news base on news id
# 5. return news after postprocessing

# The life cycle of a pages_cache:
# 1. Creation trigger onset(auth_token expire or user new login).
# 2. Retreive, filter, rank and pack news into page cache. Time stamp recorded.
# 3. If update request receive or auth_tok expire, creation will trigger and the older page cache will be soft deleted, and later digested by RI harvester.

# Q. What is a member?
# A: A user account that has already been registered in the system
#
# Q. How to check member?
# A: If the username provided in the request exist in the Users collection
#
# Q. What is an auth_token?
# A: User obtain an authenticated token once they have loggin. The token will be cache in their local device.
#
# Q. How to authenticate loggin?
# A: if the provided auth token exists in a non-deleted page cache.
#

@app.route('/updatenews', methods=["POST"])
def update_newscache():
    user_name = request.form.get('user_name', 'default')
    user_id = request.form.get('user_id', 'guest')
    auth_token = request.form.get('auth_token', None)
    cur_time = request.form.get('time', None)
    cur_page = 1
    total_page = 0
    cur_user = None
    news_retreiver = NewsRetreiver(mongo_db)
    user_status = determine_user_status(user_name, user_id, auth_token, mongo_db)
    resp = {'user_name': user_name, 'user_id':user_id, 'auth_token':auth_token, 'cur_page': 1, 'news': [], 'total_page': 0}
    if user_status == 'auth_member':
        cur_user = Member(mongo_db, user_name, user_id, auth_token)
        page_cache, total_page = cur_user.create_news_cache()
        news = news_retreiver.construct_news_page(page_cache)
        if news:
            resp['news'] = news
        resp['auth_token'] = cur_user.auth_token
        resp['total_page'] = total_page
        return json.dumps(resp)
    else:
        resp['message'] = "Please loggin or register"
        return json.dumps(resp)

@app.route('/asknews', methods=["POST"])
def get_newsfeed():
    user_name = request.form.get('user_name', 'default')
    user_id = request.form.get('user_id', 'guest')
    auth_token = request.form.get('auth_token', None)
    cur_time = request.form.get('time', None)
    cur_page = request.form.get('cur_page', 1)
    cur_user = None
    total_page = 0
    news_retreiver = NewsRetreiver(mongo_db)
    resp = {'user_name': user_name, 'user_id': user_id, 'auth_token': auth_token, 'cur_page': cur_page, 'news': [],
            'total_page': total_page, 'message': ""}
    user_status = determine_user_status(user_name, user_id, auth_token, mongo_db)
    if user_status == 'auth_member':
        cur_user = Member(mongo_db, user_name, user_id, auth_token)
        page_cache, total_page = cur_user.retreive_from_cache(page_id=cur_page)
        if not page_cache:
            page_cache, total_page = cur_user.create_news_cache()
            cur_page = 1
        if page_cache:
            news = news_retreiver.construct_news_page(page_cache)
            if news:
                resp['news'] = news
            resp['auth_token'] = cur_user.auth_token
            resp['total_page'] = total_page
            return json.dumps(resp)
        else:
            resp['message'] = "No news available, please wait for freshly collected news."
            return json.dumps(resp)
    else:
        resp['message'] = "Please loggin or register"
        return json.dumps(resp)

if __name__ == '__main__':
    print(Config.NEWS_API_KEY)
    app.run(host='localhost', port=8080)