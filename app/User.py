from WordFreq import WordFreq
from wordfreqCMD import youdao_link, sort_in_descending_order
from UseSqlite import InsertQuery, RecordQuery
import pickle_idea, pickle_idea2
import os
import random, glob
from datetime import datetime
from flask import Flask, request, redirect, render_template, url_for, session, abort, flash
from difficulty import get_difficulty_level, text_difficulty_level, user_difficulty_level

from User import *

app = Flask(__name__)
app.secret_key = 'lunch.time!'

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './' # comment this line in deployment


class User:
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
        rq.instructions("INSERT INTO user Values ('%s', '%s', '%s', '%s')" % (username, password, start_date, expiry_date))
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
