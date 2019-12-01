# -*- coding: utf-8 -*-
"""
@author: bryan chen
"""

import pickle
from flask import Flask, request
from config import Config
# from flasgger import Swagger
import os, sys
from users import  *
from news_processes.newsretreiver import NewsRetreiver

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir)

app = Flask(__name__)
app.config.from_object(Config)
# swagger = Swagger(app)


@app.route('/asknews', methods=["POST"])
def get_newsfeed():
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

    is_member = False
    if request.method == 'POST':
        if 'user_id' in request.form and request.form['user_id']:
            user_id = request.form['user_id']
            auth_token = request.form['auth_token']
            cur_time = request.form['time']
            if 'cur_page' in request.form and request.form['cur_page']:
                cur_page = request.form['cur_page']
            else:
                cur_page = 1
            cur_user = Member(user_id, auth_token, cur_time)
            if cur_user.has_loggin:
                page_cache = cur_user.retreive_from_cache()
                if not page_cache or not cur_user.cache_validate(page_cache):
                    page_cache = cur_user.rank_news()
                news_retreiver = NewsRetreiver()
                news = news_retreiver.retreive_news(page_cache)
                return news
            else:
                return cur_user.return_non_loggin_info()






if __name__ == '__main__':
    print(Config.NEWS_API_KEY)
    app.run(host='localhost', port=8080)