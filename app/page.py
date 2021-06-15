from WordFreq import load_freq_history
from wordfreqCMD import youdao_link
from UseSqlite import RecordQuery
import pickle_article_frequency_today
import os
import random, glob
from datetime import datetime
from flask import session
from difficulty import get_difficulty_level, text_difficulty_level, user_difficulty_level,within_range
import page as Today_article_page
path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './' # comment this line in deployment

def userpage_get(username,article_id):
    page = '<meta charset="UTF8">\n'
    page += '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=3.0, user-scalable=yes" />\n'
    page += '<meta name="format-detection" content="telephone=no" />\n' # forbid treating numbers as cell numbers in smart phones
    page += '<title>EnglishPal Study Room for %s</title>' % (username)
    page += '<p><b>English Pal for <font color="red">%s</font></b> <a href="/logout">登出</a></p>' % (username)
    page += '<p><a href="/%s/reset">下一篇</a></p>' % (username)
    page += '<p><b>阅读文章并回答问题</b></p>\n'
    page += '<div id="text-content">%s</div>'  % (article_id)
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
    return page

def userpage_post(username):
    page = '<meta charset="UTF8">'
    page += '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=3.0, user-scalable=yes" />'
    page += '<p>勾选不认识的单词</p>'
    page += '<form method="post" action="/%s/mark">\n' % (username)
    page += ' <input type="submit" name="add-btn" value="加入我的生词簿"/>\n'
    return page

def mainpage_get(session,image,ads):
    page = '<p><b><font size="+3" color="red">English Pal - Learn English in a smart way!</font></b></p>'
    if session.get('logged_in'):
        page += ' <a href="%s">%s</a></p>\n' % (session['username'], session['username'])
    else:
        page += '<p><a href="/login">登录</a>  <a href="/signup">成为会员</a> <a href="/static/usr/instructions.html">使用说明</a></p>\n'
        page += '<p><img src="%s" width="400px" alt="advertisement"/></p>' % (image)
        page += '<p><b>%s</b></p>' % (ads)
        page += '<p>粘帖1篇文章 (English only)</p>'
        page += '<form method="post" action="/">'
        page += ' <textarea name="content" rows="10" cols="120"></textarea><br/>'
        page += ' <input type="submit" value="get文章中的词频"/>'
        page += ' <input type="reset" value="清除"/>'
        page += '</form>'
    return page

def mainpage_post(lst):
    page = '<form method="post" action="/mark">\n'
    count = 1
    for x in lst:
        page += '<p><font color="grey">%d</font>: <a href="%s">%s</a> (%d)  <input type="checkbox" name="marked" value="%s"></p>\n' % (
        count, youdao_link(x[0]), x[0], x[1], x[0])
        count += 1
    page += ' <input type="submit" value="确定并返回"/>\n'
    page += '</form>\n'
    return page

def article_s(d,user_level, text_level,question,answer):
    s = '<p><i>According to your word list, your level is <b>%4.2f</b> and we have chosen an article with a difficulty level of <b>%4.2f</b> for you.</i></p>' % (
    user_level, text_level)
    s += '<p><b>%s</b></p>' % (d['date'])
    s += '<p><font size=+2>%s</font></p>' % (d['text'])
    s += '<p><i>%s</i></p>' % (d['source'])
    s += '<p><b>%s</b></p>' % (question)
    s = s.replace('\n', '<br/>')
    s += '%s' % (answer)
    return s


def get_random_image(path):
    img_path = random.choice(glob.glob(os.path.join(path, '*.jpg')))
    return img_path[img_path.rfind('/static'):]


def get_random_ads():
    ads = random.choice(['个性化分析精准提升', '你的专有单词本', '智能捕捉阅读弱点，针对性提高你的阅读水平'])
    return ads + '。 <a href="/signup">试试</a>吧！'


def get_today_article(user_word_list, articleID):

    # make article_frequency directory if not exists
    user_arti_freq_directory = path_prefix + 'static/article_frequency'
    if not os.path.exists(user_arti_freq_directory):
        os.mkdir(user_arti_freq_directory)
    # get user_article_frequency
    username = session['username']
    user_arti_freq_filename = user_arti_freq_directory +  '/article_frequency_%s.pickle' % (username)


    rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
    if articleID == None:
        rq.instructions("SELECT * FROM article")
    else:
        rq.instructions('SELECT * FROM article WHERE article_id=%d' % (articleID))
    rq.do()
    result = rq.get_results()


    # set user_article_frequency as a empty dict if not exist
    if os.path.exists(user_arti_freq_filename):
        user_arti_freq_record = pickle_article_frequency_today.load_record(user_arti_freq_filename)
        # flush user_article_frequency if date is different
        if datetime.now().strftime('%Y%m%d') != user_arti_freq_record[list(user_arti_freq_record)[0]][1]:
            user_arti_freq_record = {}
        else:
            # delete articles from result that have already showed > 3 times
            index = 0
            for i in range(len(result)):
                article = result[index]
                if article["article_id"] in user_arti_freq_record and user_arti_freq_record[article["article_id"]][0] >= 3:
                    # 应对每个请求执行两次的“特性”
                    # 这里只有当articleID为None时才删去该article，因为当articleID非None 且 满足>=3的条件，只有两种情况：
                    # 1. 当前页面article正好到3次，所以刷新页面或从其他页面返回等操作时该article已不满足条件，但仍应显示此article.
                    # 2. 一篇article（例如10号article）之前为2次，这次正好挑到10号.
                    #    第一次请求（articleID为None）结束后，10号已变为3次（然而此时还不会显示10号article，还会有第二次请求）
                    #    第二次请求（articleID就指定为10）, 所以虽然此时10号article “已不满足条件”，但当然应该显示10号article.
                    if articleID == None:
                        result.pop(index)
                else:
                    index += 1
    else:
        user_arti_freq_record = {}


    # Choose article according to reader's level
    d1 = load_freq_history(path_prefix + 'static/frequency/frequency.p')
    d2 = load_freq_history(path_prefix + 'static/words_and_tests.p')
    d3 = get_difficulty_level(d1, d2)

    d = {}
    d_user = load_freq_history(user_word_list)
    user_level = user_difficulty_level(d_user, d3)  # more consideration as user's behaviour is dynamic. Time factor should be considered.
    random.shuffle(result)  # shuffle list
    d = random.choice(result)
    text_level = text_difficulty_level(d['text'], d3)
    if articleID == None:
        for reading in result:
            text_level = text_difficulty_level(reading['text'], d3)
            # print('TEXT_LEVEL %4.2f' % (text_level))
            if within_range(text_level, user_level, 0.5):
                d = reading
                break


    # incorporate this article in the user_article_frequency
    if articleID == None:
        pickle_article_frequency_today.add_article_frequency(user_arti_freq_record, d["article_id"])
        pickle_article_frequency_today.save_frequency_to_pickle(user_arti_freq_record, user_arti_freq_filename)


    question = get_question_part(d['question'])
    answer = get_answer_part(d['question'])
    s = Today_article_page.article_s(d, user_level, text_level, question, answer)
    session['articleID'] = d['article_id']
    return s


def appears_in_test(word, d):
    if not word in d:
        return ''
    else:
        return ','.join(d[word])


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
    js = ''' '''
    html_code = js
    html_code += '\n'
    html_code += '<button onclick="toggle_visibility(\'answer\');">ANSWER</button>\n'
    html_code += '<div id="answer" style="display:none;">%s</div>\n' % ('\n'.join(result))
    return html_code
