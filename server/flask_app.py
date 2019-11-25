# -*- coding: utf-8 -*-
"""
@author: bryan chen
"""

import pickle
from flask import Flask, request
from config import Config
# from flasgger import Swagger
import os, sys
# from users import  User
import numpy as np
import pandas as pd

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir)

app = Flask(__name__)
app.config.from_object(Config)
# swagger = Swagger(app)

@app.route('/asknews', methods=["POST"])
def get_newsfeed():
    if request.method == 'POST':
        user_id = request.form['user_id']
        cur_time = request.form['time']
        cur_page = request.form['cur_page']
        return 'user_id'.format(user_id) + " at:{}".format(cur_time) + "page_at: {}".format(cur_page)

if __name__ == '__main__':
    print(Config.NEWS_API_KEY)
    app.run(host='localhost', port=8080)