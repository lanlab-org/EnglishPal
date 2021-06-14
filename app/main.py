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

app = Flask(__name__)
app.secret_key = 'lunch.time!'

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './' # comment this line in deployment

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
    rq.instructions("INSERT INTO user Values ('%s', '%s', '%s', '%s')" % (username, password, start_date, expiry_date))
    rq.do()

    
def check_username_availability(username):
    rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
    rq.instructions("SELECT * FROM user WHERE name='%s'" % (username))
    rq.do()
    result = rq.get_results()
    return  result == []

def get_expiry_date(username):
    rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
    rq.instructions("SELECT expiry_date FROM user WHERE name='%s'" % (username))
    rq.do()
    result = rq.get_results()
    if len(result) > 0:
        return  result[0]['expiry_date']
    else:
        return '20191024'
    


def within_range(x, y, r):
    return x > y and abs(x - y) <= r 


def get_today_article(user_word_list, articleID):

    rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
    if articleID == None:    
        rq.instructions("SELECT * FROM article")
    else:
        rq.instructions('SELECT * FROM article WHERE article_id=%d' % (articleID))
    rq.do()
    result = rq.get_results()
    
    # Choose article according to reader's level
    d1 = load_freq_history(path_prefix + 'static/frequency/frequency.p')
    d2 = load_freq_history(path_prefix + 'static/words_and_tests.p')
    d3 = get_difficulty_level(d1, d2)

    d = {}
    d_user = load_freq_history(user_word_list)
    user_level = user_difficulty_level(d_user, d3) # more consideration as user's behaviour is dynamic. Time factor should be considered.
    random.shuffle(result) # shuffle list
    d = random.choice(result)
    text_level = text_difficulty_level(d['text'], d3)
    if articleID == None:
        for reading in result:
            text_level = text_difficulty_level(reading['text'], d3)
            #print('TEXT_LEVEL %4.2f' % (text_level))
            if within_range(text_level, user_level, 0.5):
                d = reading
                break
            
    s = '<p><i>According to your word list, your level is <b>%4.2f</b> and we have chosen an article with a difficulty level of <b>%4.2f</b> for you.</i></p>' % (user_level, text_level)
    s += '<p><b>%s</b></p>' % (d['date'])
    s += '<p><font id="article" size=+2>%s</font></p>' % (d['text'])
    s += '<p><i>%s</i></p>' % (d['source'])
    s += '<p><b>%s</b></p>' % (get_question_part(d['question']))
    s = s.replace('\n', '<br/>')    
    s += '%s' % (get_answer_part(d['question']))
    session['articleID'] = d['article_id']
    return s


def appears_in_test(word, d):
    if not word in d:
        return ''
    else:
        return ','.join(d[word])


def get_time():
    return datetime.now().strftime('%Y%m%d%H%M') # upper to minutes


def get_question_part(s):
    s = s.strip()
    result = []
    flag = 0
    for line in s.split('\n'):
        line = line.strip()
        if line == 'QUESTION':
            result.append(line)
            flag = 1
        elif line == 'ANSWER':
            flag = 0
        elif flag == 1:
            result.append(line)
    return '\n'.join(result)


def get_answer_part(s):
    s = s.strip()
    result = []
    flag = 0
    for line in s.split('\n'):
        line = line.strip()
        if line == 'ANSWER':
            flag = 1
        elif flag == 1:
            result.append(line)
    # https://css-tricks.com/snippets/javascript/showhide-element/
    js = '''
<script type="text/javascript">

    function toggle_visibility(id) {
       var e = document.getElementById(id);
       if(e.style.display == 'block')
          e.style.display = 'none';
       else
          e.style.display = 'block';
    }
</script>   
    '''
    html_code = js
    html_code += '\n'
    html_code += '<button onclick="toggle_visibility(\'answer\');">ANSWER</button>\n'
    html_code += '<div id="answer" style="display:none;">%s</div>\n' % ('\n'.join(result))
    return html_code



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



@app.route("/<username>", methods=['GET', 'POST'])
def userpage(username):
    
    if not session.get('logged_in'):
        return '<p>请先<a href="/login">登录</a>。</p>'

    user_expiry_date = session.get('expiry_date')
    if datetime.now().strftime('%Y%m%d') > user_expiry_date:
        return '<p>账号 %s 过期。</p><p>为了提高服务质量，English Pal 收取会员费用， 每天0元。</p> <p>请决定你要试用的时间长度，扫描下面支付宝二维码支付。 支付时请注明<i>English Pal Membership Fee</i>。 我们会于12小时内激活账号。</p><p><img src="static/donate-the-author-hidden.jpg" width="120px" alt="支付宝二维码" /></p><p>如果有问题，请加开发者微信 torontohui。</p> <p><a href="/logout">登出</a></p>' % (username)

    
    username = session.get('username')

    user_freq_record = path_prefix + 'static/frequency/' +  'frequency_%s.pickle' % (username)
    
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
            page += '<p><font color="grey">%d</font>: <a href="%s" title="%s">%s</a> (%d)  <input type="checkbox" name="marked" value="%s"></p>\n' % (count, youdao_link(x[0]), appears_in_test(x[0], words_tests_dict), x[0], x[1], x[0])
            count += 1
        page += '</form>\n'
        return page
    
    elif request.method == 'GET': # when we load a html page
        page = '<meta charset="UTF8">\n'
        page += '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=3.0, user-scalable=yes" />\n'
        page += '<meta name="format-detection" content="telephone=no" />\n' # forbid treating numbers as cell numbers in smart phones
        page += '<title>EnglishPal Study Room for %s</title>' % (username)
        page += '<p><b>English Pal for <font color="red">%s</font></b> <a href="/logout">登出</a></p>' % (username)
        page += '<p><a href="/%s/reset">下一篇</a></p>' % (username)
        page += '<p><b>阅读文章并回答问题</b></p>\n'
        page += '<div id="text-content">%s</div>'  % (get_today_article(user_freq_record, session['articleID']))
        page += '<p><b>收集生词吧</b> （可以在正文中划词，也可以复制黏贴）</p>'
        page += '<form method="post" action="/%s">' % (username)
        page += ' <textarea name="content" id="selected-words" rows="10" cols="120"></textarea><br/>'
        page += ' <input type="submit" value="get 所有词的频率"/>'
        page += ' <input type="reset" value="清除"/>'
        page += '</form>\n'
        page += '<script type="text/javascript">'
        page += '   function getWord(){ \n'
        page += '      var word = window.getSelection?window.getSelection():document.selection.createRange().text;\n'
        page += '      return word;\n'
        page += '   }\n'
        page += '   function highLight(){ \n'
        page += '      var txt=document.getElementById("article").innerText\n'
        page += '      var list=document.getElementById("selected-words").value.split(" ");\n'
        page += '      console.log(list.length);\n'
        page += '      for(var i=0;i<list.length;++i){\n'
        page += '      console.log(list[i]);\n'
        page += '          list[i]=list[i].replace(/(^\s*)|(\s*$)/g, "");\n'
        page += '          if(list[i]!=""&&"<mark>".indexOf(list[i])==-1&&"</mark>".indexOf(list[i])==-1)txt=txt.replace(new RegExp(list[i],"g"),"<mark>"+list[i]+"</mark>");\n'
        #page += '         while(txt.indexOf(list[i])>-1){\n'
        #page += '          var pos=txt.indexOf(list[i]);\n'
        #page += '          if(pos!=-1){\n'
        #page += '              console.log(pos);;\n'
        #page += '              txt=""+(txt.substring(0,pos)+"<mark>"+list[i]+"</mark>"+txt.substring((pos+list[i].length),txt.length));\n'
        #page += '           };\n'
        page += '      }\n'
        page += '      document.getElementById("article").innerHTML=txt;\n'
        page += '   }\n'
        page += '   function fillinWord(){\n'
        page += '      var element = document.getElementById("selected-words");\n'
        page += '      element.value = element.value + " " + getWord();\n'
        page += '      highLight();\n'
        page += '   }\n'
        page += '   document.getElementById("text-content").addEventListener("click", fillinWord, false);\n'
        page += '   document.getElementById("text-content").addEventListener("touchstart", fillinWord, false);\n'
        page += '   window.setInterval("highLight()", 10000);\n'
        page += '</script>\n'
        
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
                if isinstance(d[word], list): # d[word] is a list of dates
                    if freq > 1:
                        page += '<p class="new-word"> <a href="%s">%s</a>                     (<a title="%s">%d</a>) </p>\n' % (youdao_link(word), word, '; '.join(d[word]), freq)
                    else:
                        page += '<p class="new-word"> <a href="%s">%s</a> <font color="white">(<a title="%s">%d</a>)</font> </p>\n' % (youdao_link(word), word, '; '.join(d[word]), freq)
                elif isinstance(d[word], int): # d[word] is a frequency. to migrate from old format.
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


if __name__ == '__main__':
    #app.secret_key = os.urandom(16)
    #app.run(debug=False, port='6000')
    app.run(debug=True)        
    #app.run(debug=True, port='6000')
    #app.run(host='0.0.0.0', debug=True, port='6000')

