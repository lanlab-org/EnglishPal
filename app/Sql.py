from WordFreq import WordFreq
from wordfreqCMD import youdao_link, sort_in_descending_order
from UseSqlite import InsertQuery, RecordQuery
import pickle_idea, pickle_idea2
import os
import random, glob
from datetime import datetime
from flask import Flask, request, redirect, render_template, url_for, session, abort, flash
from difficulty import get_difficulty_level, text_difficulty_level, user_difficulty_level

app = Flask(__name__)
app.secret_key = 'lunch.time!'

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './'  # comment this line in deployment

class Sql:
    def get_random_image(path):
        img_path = random.choice(glob.glob(os.path.join(path, '*.jpg')))
        return img_path[img_path.rfind('/static'):]

    def get_random_ads():
        ads = random.choice(['个性化分析精准提升', '你的专有单词本', '智能捕捉阅读弱点，针对性提高你的阅读水平'])
        return ads + '。 <a href="/signup">试试</a>吧！'

    def load_freq_history(path):
        d = {}
        if os.path.exists(path):
            d = pickle_idea.load_record(path)
        return d

    def verify_user(username, password):
        rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
        rq.instructions("SELECT * FROM user WHERE name='%s' AND password='%s'" % (username, password))
        rq.do()
        result = rq.get_results()
        return result != []

    def add_user(username, password):
        start_date = datetime.now().strftime('%Y%m%d')
        expiry_date = '20211230'
        rq = InsertQuery(path_prefix + 'static/wordfreqapp.db')
        rq.instructions(
            "INSERT INTO user Values ('%s', '%s', '%s', '%s')" % (username, password, start_date, expiry_date))
        rq.do()

    def check_username_availability(username):
        rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
        rq.instructions("SELECT * FROM user WHERE name='%s'" % (username))
        rq.do()
        result = rq.get_results()
        return result == []

    def get_expiry_date(username):
        rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
        rq.instructions("SELECT expiry_date FROM user WHERE name='%s'" % (username))
        rq.do()
        result = rq.get_results()
        if len(result) > 0:
            return result[0]['expiry_date']
        else:
            return '20191024'