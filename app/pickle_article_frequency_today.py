# Purpose: dictionary & pickle as a simple means of database.
# Task: save the article frequency in order to manage the article frequency showing on a user's page.

import pickle
from datetime import datetime

def add_article_frequency(d, article_id):
    if article_id not in d:
        d[article_id] = []
        d[article_id].append(1)
        d[article_id].append(datetime.now().strftime('%Y%m%d'))
    else:
        d[article_id][0] += 1

def save_frequency_to_pickle(d, pickle_fname):
    f = open(pickle_fname, 'wb')
    pickle.dump(d, f)
    f.close()

def load_record(pickle_fname):
    f = open(pickle_fname, 'rb')
    d = pickle.load(f)
    f.close()
    return d
