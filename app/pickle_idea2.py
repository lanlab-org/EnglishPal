###########################################################################
# Copyright 2019 (C) Hui Lan <hui.lan@cantab.net>
# Written permission must be obtained from the author for commercial uses.
###########################################################################


# Purpose: dictionary & pickle as a simple means of database.
# Task: incorporate the functions into wordfreqCMD.py such that it will also show cumulative frequency.
# Note: unlike pick_idea.py, now the second item is not frequency, but a list of dates.

import pickle
from datetime import datetime

def lst2dict(lst, d):
    ''' 
    Store the information in list lst to dictionary d. 
    Note: nothing is returned.

    '''
    for x in lst:
        word = x[0]
        dates = x[1]
        if not word in d:
            d[word] = dates
        else:
            d[word] += dates

def deleteRecord(path,word):
    with open(path, 'rb') as f:
        db = pickle.load(f)
    try:
        db.pop(word)
    except KeyError:
        print("sorry")
    with open(path, 'wb') as ff:
            pickle.dump(db, ff)

def dict2lst(d):
    if len(d) > 0:
        keys = list(d.keys())
        if isinstance(d[keys[0]], int):
            lst = []
            for k in d:
                lst.append((k, [datetime.now().strftime('%Y%m%d%H%M')]))
            return lst
        elif isinstance(d[keys[0]], list):
            return list(d.items()) # a list of (key, value) pairs

    return []

def merge_frequency(lst1, lst2):
    d = {}
    lst2dict(lst1, d)
    lst2dict(lst2, d)
    return d


def load_record(pickle_fname):
    f = open(pickle_fname, 'rb')
    d = pickle.load(f)
    f.close()
    return d


def save_frequency_to_pickle(d, pickle_fname):
    f = open(pickle_fname, 'wb')
    exclusion_lst = ['one', 'no', 'has', 'had', 'do', 'that', 'have', 'by', 'not', 'but', 'we', 'this', 'my', 'him', 'so', 'or', 'as', 'are', 'it', 'from', 'with', 'be', 'can', 'for', 'an', 'if', 'who', 'whom', 'whose', 'which', 'the', 'to', 'a', 'of', 'and', 'you', 'i', 'he', 'she', 'they', 'me', 'was', 'were', 'is', 'in', 'at', 'on', 'their', 'his', 'her', 's', 'said', 'all', 'did', 'been', 'w']
    d2 = {}
    for k in d:
        if not k in exclusion_lst and not k.isnumeric() and not len(k) < 2:
            d2[k] = list(sorted(set(d[k])))
    pickle.dump(d2, f)
    f.close()



if __name__ == '__main__':

    lst1 = [('apple',['201910251437', '201910251438']),  ('banana',['201910251439'])]
    d = {}
    lst2dict(lst1, d) # d will change
    save_frequency_to_pickle(d, 'frequency.p') # frequency.p is our database


    lst2 = [('banana',['201910251439']), ('orange', ['201910251440', '201910251439'])]
    d = load_record('frequency.p')
    lst1 = dict2lst(d)
    d = merge_frequency(lst2, lst1)
    print(d)
