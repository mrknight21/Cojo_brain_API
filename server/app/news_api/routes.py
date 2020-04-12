from flask import Blueprint
from flask import Flask, request, Response
from config import Config
# from flasgger import Swagger
import os, sys, json
from users import  *
from users.user_utility import *
from news_processes.newsretreiver import NewsRetreiver
from app.news_api import bp, frb_bd as db_conn


# @bp.route('/', methods=["GET"])
# def test_connection():
#     return 'testing connection: {}'.format(' pass')

@bp.route('/update', methods=["POST"])
def update_newscache():
    auth_token = None
    user_name = request.form.get('user_name', 'default')
    user_id = request.form.get('user_id', 'guest')
    cur_page = 1
    total_page = 0
    cur_user = None
    news_retreiver = NewsRetreiver(db_conn)
    user_status = determine_user_status(user_name, user_id, auth_token, db_conn)
    resp = {'user_id':user_id, 'complete': False, 'total_page': 0, 'message':""}
    if user_status == 'auth_member':
        cur_user = Member(db_conn, user_id, user_name, auth_token)
        page_cache, total_page = cur_user.create_news_cache()
        # news = news_retreiver.construct_news_page(page_cache)
        if page_cache:
            resp['complete'] = True
            resp['total_page'] = total_page
    else:
        resp['message'] = "Please loggin or register"
    return json.dumps(resp)

# @bp.route('/get', methods=["POST"])
# def get_newsfeed():
#     user_name = request.form.get('user_name', 'default')
#     user_id = request.form.get('user_id', '0'*24)
#     auth_token = request.form.get('auth_token', None)
#     cur_time = request.form.get('time', None)
#     cur_page = request.form.get('cur_page', 1)
#     cur_user = None
#     total_page = 0
#     news_retreiver = NewsRetreiver(db_conn)
#     resp = {'user_name': user_name, 'user_id': user_id, 'auth_token': auth_token, 'cur_page': cur_page, 'news_api': [],
#             'total_page': total_page, 'message': ""}
#     user_status = determine_user_status(user_name, user_id, auth_token, db_conn)
#     if user_status == 'auth_member':
#         cur_user = Member(db_conn, user_name, user_id, auth_token)
#         page_cache, total_page = cur_user.retreive_from_cache(page_id=cur_page)
#         if not page_cache:
#             page_cache, total_page = cur_user.create_news_cache()
#             cur_page = 1
#         if page_cache:
#             news = news_retreiver.construct_news_page(page_cache)
#             if news:
#                 resp['news_api'] = news
#             resp['auth_token'] = cur_user.auth_token
#             resp['total_page'] = total_page
#         else:
#             resp['message'] = "No news_api available, please wait for freshly collected news_api."
#     else:
#         resp['message'] = "Please loggin or register"
#     return json.dumps(resp)
