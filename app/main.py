#! /usr/bin/python3
# -*- coding: utf-8 -*-

###########################################################################
# Copyright 2019 (C) Hui Lan <hui.lan@cantab.net>
# Written permission must be obtained from the author for commercial uses.
###########################################################################

from Login import *
from Article import *
import Yaml
from user_service import userService
from account_service import accountService
app = Flask(__name__)
app.secret_key = 'lunch.time!'

# 将蓝图注册到Lab app
app.register_blueprint(userService)
app.register_blueprint(accountService)

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './'  # comment this line in deployment


def get_random_image(path):
    '''
    返回随机图
    :param path: 图片文件(JPEG格式)，不包含后缀名
    :return:
    '''
    img_path = random.choice(glob.glob(os.path.join(path, '*.jpg')))

    return img_path[img_path.rfind('/static'):]


def get_random_ads():
    '''
    返回随机广告
    :return: 一个广告(包含HTML标签)
    '''
    ads = random.choice(['个性化分析精准提升', '你的专有单词本', '智能捕捉阅读弱点，针对性提高你的阅读水平'])
    return ads + '。 <a href="/signup">试试</a>吧！'


def appears_in_test(word, d):
    '''
    如果字符串里没有指定的单词，则返回逗号加单词
    :param word: 指定单词
    :param d: 字符串
    :return: 逗号加单词
    '''
    if not word in d:
        return ''
    else:
        return ','.join(d[word])


@app.route("/mark", methods=['GET', 'POST'])
def mark_word():
    '''
    标记单词
    :return: 重定位到主界面
    '''
    if request.method == 'POST':
        d = load_freq_history(path_prefix + 'static/frequency/frequency.p')
        lst_history = pickle_idea.dict2lst(d)
        lst = []
        for word in request.form.getlist('marked'):
            lst.append((word, 1))
        d = pickle_idea.merge_frequency(lst, lst_history)
        pickle_idea.save_frequency_to_pickle(d, path_prefix + 'static/frequency/frequency.p')
        return redirect(url_for('mainpage'))
    else: # 不回应GET请求
        return 'Under construction'


@app.route("/", methods=['GET', 'POST'])
def mainpage():
    '''
    根据GET或POST方法来返回不同的主界面
    :return: 主界面
    '''
    if request.method == 'POST':  # when we submit a form
        content = request.form['content']
        f = WordFreq(content)
        lst = f.get_freq()
        # save history
        d = load_freq_history(path_prefix + 'static/frequency/frequency.p')
        lst_history = pickle_idea.dict2lst(d)
        d = pickle_idea.merge_frequency(lst, lst_history)
        pickle_idea.save_frequency_to_pickle(d, path_prefix + 'static/frequency/frequency.p')
        return render_template('mainpage_post.html', lst=lst, yml=Yaml.yml)

    elif request.method == 'GET':  # when we load a html page
        random_ads = get_random_ads()
        number_of_essays = total_number_of_essays()
        d = load_freq_history(path_prefix + 'static/frequency/frequency.p')
        d_len = len(d)
        lst = sort_in_descending_order(pickle_idea.dict2lst(d))
        return render_template('mainpage_get.html', random_ads=random_ads, number_of_essays=number_of_essays,
                               d_len=d_len, lst=lst, yml=Yaml.yml)



if __name__ == '__main__':
    '''
    运行程序
    '''
    # app.secret_key = os.urandom(16)
    # app.run(debug=False, port='6000')
    app.run(debug=True)
    # app.run(debug=True, port='6000')
    # app.run(host='0.0.0.0', debug=True, port='6000')
    # print(mod5('123'))
