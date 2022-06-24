import hashlib
from datetime import datetime
from UseSqlite import InsertQuery, RecordQuery

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './'  # comment this line in deployment


def verify_user(username, password):
    rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
    password = md5(username + password)
    rq.instructions_with_parameters("SELECT * FROM user WHERE name=:username AND password=:password", dict(
        username=username, password=password))  # the named style https://docs.python.org/3/library/sqlite3.html
    rq.do_with_parameters()
    result = rq.get_results()
    return result != []


def add_user(username, password):
    start_date = datetime.now().strftime('%Y%m%d')
    expiry_date = '20221230'
    # 将用户名和密码一起加密，以免暴露不同用户的相同密码
    password = md5(username + password)
    rq = InsertQuery(path_prefix + 'static/wordfreqapp.db')
    rq.instructions_with_parameters("INSERT INTO user VALUES (:username, :password, :start_date, :expiry_date)", dict(
        username=username, password=password, start_date=start_date, expiry_date=expiry_date))
    rq.do_with_parameters()


def check_username_availability(username):
    rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
    rq.instructions_with_parameters(
        "SELECT * FROM user WHERE name=:username", dict(username=username))
    rq.do_with_parameters()
    result = rq.get_results()
    return result == []


def change_password(username, old_password, new_password):
    '''
    修改密码
    :param username: 用户名
    :param old_password: 旧的密码
    :param new_password: 新密码
    :return: 修改成功:True 否则:False
    '''
    if not verify_user(username, old_password):  # 旧密码错误
        return False
    # 将用户名和密码一起加密，以免暴露不同用户的相同密码
    password = md5(username + new_password)
    rq = InsertQuery(path_prefix + 'static/wordfreqapp.db')
    rq.instructions_with_parameters("UPDATE user SET password=:password WHERE name=:username", dict(
        password=password, username=username))
    rq.do_with_parameters()
    return True


def get_expiry_date(username):
    rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
    rq.instructions_with_parameters(
        "SELECT expiry_date FROM user WHERE name=:username", dict(username=username))
    rq.do_with_parameters()
    result = rq.get_results()
    if len(result) > 0:
        return result[0]['expiry_date']
    else:
        return '20191024'


def md5(s):
    '''
    MD5摘要
    :param str: 字符串
    :return: 经MD5以后的字符串
    '''
    h = hashlib.md5(s.encode(encoding='utf-8'))
    return h.hexdigest()
