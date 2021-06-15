from UseSqlite import InsertQuery, RecordQuery
from datetime import datetime

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './' # comment this line in deployment

def get_time():
    return datetime.now().strftime('%Y%m%d%H%M') # upper to minutes


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