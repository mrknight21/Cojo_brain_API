from flask import request
from utility import general
# from flasgger import Swagger
import json
from users import  *
from users.user_utility import *
from news_processes.newsretreiver import NewsRetreiver
from app.news_api import bp, frb_bd as db_conn

@bp.route('/ping', methods=["POST", "GET"])
def ping():
    return "Echo: ping!"

@bp.route('/update', methods=["POST"])
def update_newscache():
    auth_token = None
    user_name = request.form.get('user_name', 'default')
    user_id = request.form.get('user_id', 'guest')
    return_cache = request.form.get('return_cache','False')
    if return_cache.lower() == 'True'.lower():
        return_cache = True
    else:
        return_cache = False
    reset = request.form.get('reset','True')
    if reset.lower() == 'False'.lower():
        reset = False
    else:
        reset = True
    cur_user = None
    news_retreiver = NewsRetreiver(db_conn)
    user_status = determine_user_status(user_name, user_id, auth_token, db_conn)
    resp = {'user_id':user_id, 'complete': False, 'total_news': 0, 'message':""}
    if user_status == 'auth_member':
        cur_user = Member(db_conn, user_id, user_name, auth_token)
        ranked_news = cur_user.create_news_cache(reset)
        cur_user.update_news_cache(ranked_news)
        # news = news_retreiver.construct_news_page(page_cache)
        if ranked_news:
            resp['complete'] = True
            resp['total_news'] = len(ranked_news)
            if return_cache:
                resp['ranked_news'] = ranked_news
    else:
        resp['message'] = "Please loggin or register"
    return json.dumps(resp, default=general.json_serial)