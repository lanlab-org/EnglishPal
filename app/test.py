#! /usr/bin/python3
# -*- coding: utf-8 -*-

###########################################################################
# Copyright 2019 (C) Hui Lan <hui.lan@cantab.net>
# Written permission must be obtained from the author for commercial uses.
###########################################################################

from WordFreq import WordFreq
from wordfreqCMD import youdao_link, sort_in_descending_order
from UseSqlite import InsertQuery, RecordQuery
import pickle_idea, pickle_idea2
import os
import random, glob
from datetime import datetime
from flask import Flask, request, redirect, render_template, url_for, session, abort, flash
from difficulty import get_difficulty_level, text_difficulty_level, user_difficulty_level
import EverydayArticle as today
import SqlWords as sql
app = Flask(__name__)
app.secret_key = 'lunch.time!'
def load_freq_history(path):
    d = {}
    if os.path.exists(path):
        d = pickle_idea.load_record(path)
    return d

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './' # comment this line in deployment
result={}
d={}
lst = sql.get_user()
x1=path_prefix + 'static/frequency/' + 'frequency_lanhui.pickle'
x2=path_prefix + 'static/frequency/' + 'frequency_lanhui.pickle'
d1 = load_freq_history(x1)
d2 = load_freq_history(x2)
lst1 = pickle_idea2.dict2lst(d1)
lst2 = pickle_idea2.dict2lst(d2)
pickle_idea2.lst2dict2(lst1,d)
print(d)
for xxx in d:
    print(xxx)
    print(d[xxx])
    print(type(d[xxx]))
# for x in lst1:
#     word = x[0]
#     dates = x[1]
#     if word in d:
#         print("1111")
#         d[word] += dates
#     else:
#         print("2222")
#         d[word] = dates
#
# for x in lst2:
#     word = x[0]
#     dates = x[1]
#     if word in d:
#         print("1111")
#         d[word] += dates
#     else:
#         print("2222")
#         d[word] = dates
# m=lst1[0]
# print(m)
# www = m[0]
# print(www)
# if www in lst2:
#     print("1111")
# for x in lst1:
#     word = x[0]
#     dates = x[1]
#     if word in lst2:
#         print(word)
#         if not word in d:
#             d[word] = dates
#         else:
#             d[word] += dates

#
# print(d1)
# for xx in lst_history:
#     print(xx)