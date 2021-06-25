#! /usr/bin/python3
# -*- coding: utf-8 -*-

###########################################################################
# Copyright 2019 (C) Hui Lan <hui.lan@cantab.net>
# Written permission must be obtained from the author for commercial uses.
###########################################################################
from app import app
from app.Utils.WordFreq import WordFreq
from app.Utils.wordfreqCMD import youdao_link, sort_in_descending_order
from app.Utils.UseSqlite import InsertQuery, RecordQuery
from app.Utils import pickle_idea, pickle_idea2
import os
import random, glob
from datetime import datetime
from flask import Flask, request, redirect, render_template, url_for, session, abort, flash
from app.Utils.difficulty import get_difficulty_level, text_difficulty_level, user_difficulty_level

from app.Utils.utils import get_random_image, get_random_ads, load_freq_history, verify_user, add_user, check_username_availability, get_expiry_date, within_range, get_today_article, appears_in_test, get_time, get_question_part, get_answer_part

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './app/' # comment this line in deployment


@app.route("/<username>/reset", methods=['GET', 'POST'])
def user_reset(username):
    if request.method == 'GET':
        session['articleID'] = None
        return redirect(url_for('userpage', username=username))
    else:
        return 'Under construction'


@app.route("/mark", methods=['GET', 'POST'])
def mark_word():
    if request.method == 'POST':
        d = load_freq_history(path_prefix + 'static/frequency/frequency.p')
        lst_history = pickle_idea.dict2lst(d)
        lst = []
        for word in request.form.getlist('marked'):
            lst.append((word, 1))
        d = pickle_idea.merge_frequency(lst, lst_history)
        pickle_idea.save_frequency_to_pickle(d, path_prefix + 'static/frequency/frequency.p')
        return redirect(url_for('mainpage'))
    else:
        return 'Under construction'



@app.route("/", methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':  # when we submit a form
        content = request.form['content']
        f = WordFreq(content)
        lst = f.get_freq()
        page = '<form method="post" action="/mark">\n'
        count = 1
        for x in lst:
            page += '<p><font color="grey">%d</font>: <a href="%s">%s</a> (%d)  <input type="checkbox" name="marked" value="%s"></p>\n' % (count, youdao_link(x[0]), x[0], x[1], x[0])
            count += 1
        page += ' <input type="submit" value="确定并返回"/>\n'
        page += '</form>\n'
        # save history 
        d = load_freq_history(path_prefix + 'static/frequency/frequency.p')
        lst_history = pickle_idea.dict2lst(d)
        d = pickle_idea.merge_frequency(lst, lst_history)
        pickle_idea.save_frequency_to_pickle(d, path_prefix + 'static/frequency/frequency.p')
        
        return page
    elif request.method == 'GET': # when we load a html page
        page = '''
             <html lang="zh">
               <head>
               <meta charset="utf-8">
               <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=3.0, user-scalable=yes" />
                 <title>EnglishPal 英文单词高效记</title>

               </head>
               <body>
        '''
        page += '<p><b><font size="+3" color="red">English Pal - Learn English in a smart way!</font></b></p>'
        if session.get('logged_in'):
            page += ' <a href="%s">%s</a></p>\n' % (session['username'], session['username'])
        else:
            page += '<p><a href="/login">登录</a>  <a href="/signup">成为会员</a> <a href="/static/usr/instructions.html">使用说明</a></p>\n'
        #page += '<p><img src="%s" width="400px" alt="advertisement"/></p>' % (get_random_image(path_prefix + 'static/img/'))
        page += '<p><b>%s</b></p>' % (get_random_ads())
        page += '<p>粘帖1篇文章 (English only)</p>'
        page += '<form method="post" action="/">'
        page += ' <textarea name="content" rows="10" cols="120"></textarea><br/>'
        page += ' <input type="submit" value="get文章中的词频"/>'
        page += ' <input type="reset" value="清除"/>'
        page += '</form>'
        d = load_freq_history(path_prefix + 'static/frequency/frequency.p')
        if len(d) > 0:
            page += '<p><b>最常见的词</b></p>'
            for x in sort_in_descending_order(pickle_idea.dict2lst(d)):
                if x[1] <= 99:
                    break
                page += '<a href="%s">%s</a> %d\n' % (youdao_link(x[0]), x[0], x[1])

        page += '</body></html>'
        return page


@app.route("/<username>/mark", methods=['GET', 'POST'])
def user_mark_word(username):
    username = session[username]
    user_freq_record = path_prefix + 'static/frequency/' +  'frequency_%s.pickle' % (username)
    if request.method == 'POST':
        d = load_freq_history(user_freq_record)
        lst_history = pickle_idea2.dict2lst(d)
        lst = []
        for word in request.form.getlist('marked'):
            lst.append((word, [get_time()]))
        d = pickle_idea2.merge_frequency(lst, lst_history)
        pickle_idea2.save_frequency_to_pickle(d, user_freq_record)
        return redirect(url_for('userpage', username=username))
    else:
        return 'Under construction'


@app.route("/<username>/<word>/unfamiliar", methods=['GET', 'POST'])
def unfamiliar(username,word):
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea.unfamiliar(user_freq_record,word)
    session['thisWord'] = word  # 1. put a word into session
    return redirect(url_for('userpage', username=username))

@app.route("/<username>/<word>/familiar", methods=['GET', 'POST'])
def familiar(username,word):
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea.familiar(user_freq_record,word)
    session['thisWord'] = word  # 1. put a word into session
    return redirect(url_for('userpage', username=username))


@app.route("/<username>", methods=['GET', 'POST'])
def userpage(username):
    if not session.get('logged_in'):
        return '<p>请先<a href="/login">登录</a>。</p>'

    user_expiry_date = session.get('expiry_date')
    if datetime.now().strftime('%Y%m%d') > user_expiry_date:
        return '<p>账号 %s 过期。</p><p>为了提高服务质量，English Pal 收取会员费用， 每天0元。</p> <p>请决定你要试用的时间长度，扫描下面支付宝二维码支付。 支付时请注明<i>English Pal Membership Fee</i>。 我们会于12小时内激活账号。</p><p><img src="static/donate-the-author-hidden.jpg" width="120px" alt="支付宝二维码" /></p><p>如果有问题，请加开发者微信 torontohui。</p> <p><a href="/logout">登出</a></p>' % (
            username)

    username = session.get('username')

    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)

    if request.method == 'POST':  # when we submit a form
        content = request.form['content']
        f = WordFreq(content)
        lst = f.get_freq()
        page = '<meta charset="UTF8">'
        page += '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=3.0, user-scalable=yes" />'
        page += '<p>勾选不认识的单词</p>'
        page += '<form method="post" action="/%s/mark">\n' % (username)
        page += ' <input type="submit" name="add-btn" value="加入我的生词簿"/>\n'
        count = 1
        words_tests_dict = pickle_idea.load_record(path_prefix + 'static/words_and_tests.p')
        for x in lst:
            page += '<p><font color="grey">%d</font>: <a href="%s" title="%s">%s</a> (%d)  <input type="checkbox" name="marked" value="%s"></p>\n' % (
            count, youdao_link(x[0]), appears_in_test(x[0], words_tests_dict), x[0], x[1], x[0])
            count += 1
        page += '</form>\n'
        return page

    elif request.method == 'GET':  # when we load a html page
        page = '<meta charset="UTF8">\n'
        page += '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=3.0, user-scalable=yes" />\n'
        page += '<meta name="format-detection" content="telephone=no" />\n'  # forbid treating numbers as cell numbers in smart phones
        page += '<title>EnglishPal Study Room for %s</title>' % (username)
        page += '<p><b>English Pal for <font color="red">%s</font></b> <a href="/logout">登出</a></p>' % (username)
        page += '<p><a href="/%s/reset">下一篇</a></p>' % (username)
        page += '<p><b>阅读文章并回答问题</b></p>\n'
        page += '<div id="text-content">%s</div>' % (get_today_article(user_freq_record, session['articleID']))
        page += '<p><b>收集生词吧</b> （可以在正文中划词，也可以复制黏贴）</p>'
        page += '<form method="post" action="/%s">' % (username)
        page += ' <textarea name="content" id="selected-words" rows="10" cols="120"></textarea><br/>'
        page += ' <input type="submit" value="get 所有词的频率"/>'
        page += ' <input type="reset" value="清除"/>'
        page += '</form>\n'
        page += ''' 
                 <script>
                   function getWord(){ 
                       var word = window.getSelection?window.getSelection():document.selection.createRange().text;
                       return word;
                   }
                   function fillinWord(){
                       var element = document.getElementById("selected-words");
                       element.value = element.value + " " + getWord();
                   }
                   document.getElementById("text-content").addEventListener("click", fillinWord, false);
                   document.getElementById("text-content").addEventListener("touchstart", fillinWord, false);
                 </script>
                 '''
        if session.get('thisWord'):
            page += '''
                   <script type="text/javascript">
                       location.href = "#aaa"  // 2. define a anchor URL and point to the anchor in the page whose id is aaa
                   </script> 
                   '''

        d = load_freq_history(user_freq_record)
        if len(d) > 0:
            page += '<p><b>我的生词簿</b></p>'
            lst = pickle_idea2.dict2lst(d)
            lst2 = []
            for t in lst:
                lst2.append((t[0], len(t[1])))
            for x in sort_in_descending_order(lst2):
                word = x[0]
                freq = x[1]
                if session.get('thisWord') == x[0]:
                    page += '<a name="aaa"></a>'  # 3. anchor
                if isinstance(d[word], list):  # d[word] is a list of dates
                    if freq > 1:
                        page += '<p class="new-word"> <a href="%s">%s</a>(<a title="%s">%d</a>) <a href="%s/%s/familiar">熟悉</a> <a href="%s/%s/unfamiliar">不熟悉</a>  </p>\n' % (
                        youdao_link(word), word, '; '.join(d[word]), freq, username, word, username, word)
                    else:
                        page += '<p class="new-word"> <a href="%s">%s</a>(<a title="%s">%d</a>) <a href="%s/%s/familiar">熟悉</a> <a href="%s/%s/unfamiliar">不熟悉</a>   </p>\n' % (
                        youdao_link(word), word, '; '.join(d[word]), freq, username, word, username, word)
                elif isinstance(d[word], int):  # d[word] is a frequency. to migrate from old format.
                    page += '<a href="%s">%s</a>%d\n' % (youdao_link(word), word, freq)
        return page

### Sign-up, login, logout ###
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        available = check_username_availability(username)
        if not available:
            flash('用户名 %s 已经被注册。' % (username))
            return render_template('signup.html')
        elif len(password.strip()) < 4:
            return '密码过于简单。'
        else:
            add_user(username, password)
            verified = verify_user(username, password)
            if verified:
                session['logged_in'] = True
                session[username] = username
                session['username'] = username
                return '<p>恭喜，你已成功注册， 你的用户名是 <a href="%s">%s</a>。</p>\
                <p><a href="/%s">开始使用</a> <a href="/">返回首页</a><p/>' % (username, username, username)
            else:
                return '用户名密码验证失败。'


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return '你已登录 <a href="/%s">%s</a>。 登出点击<a href="/logout">这里</a>。' % (session['username'], session['username'])
    elif request.method == 'POST':
        # check database and verify user
        username = request.form['username']
        password = request.form['password']
        verified = verify_user(username, password)
        if verified:
            session['logged_in'] = True
            session[username] = username
            session['username'] = username
            user_expiry_date = get_expiry_date(username)
            session['expiry_date'] = user_expiry_date
            session['articleID'] = None
            return redirect(url_for('userpage', username=username))
        else:
            return '无法通过验证。'


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('mainpage'))