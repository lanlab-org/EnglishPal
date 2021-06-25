###########################################################################
# Copyright 2019 (C) Hui Lan <hui.lan@cantab.net>
# Written permission must be obtained from the author for commercial uses.
###########################################################################

# Purpose: dictionary & pickle as a simple means of database.
# Task: incorporate the functions into wordfreqCMD.py such that it will also show cumulative frequency.

import pickle
from datetime import datetime


def lst2dict(lst, d):
    ''' 
    Store the information in list lst to dictionary d. 
    Note: nothing is returned.

    '''
    for x in lst:
        word = x[0]
        freq = x[1]
        if not word in d:
            d[word] = freq 
        else:
            d[word] += freq


def dict2lst(d):
    return list(d.items()) # a list of (key, value) pairs
        

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
    #exclusion_lst = ['one', 'no', 'has', 'had', 'do', 'that', 'have', 'by', 'not', 'but', 'we', 'this', 'my', 'him', 'so', 'or', 'as', 'are', 'it', 'from', 'with', 'be', 'can', 'for', 'an', 'if', 'who', 'whom', 'whose', 'which', 'the', 'to', 'a', 'of', 'and', 'you', 'i', 'he', 'she', 'they', 'me', 'was', 'were', 'is', 'in', 'at', 'on', 'their', 'his', 'her', 's', 'said', 'all', 'did', 'been', 'w']
    exclusion_lst = []
    d2 = {}
    for k in d:
        if not k in exclusion_lst and not k.isnumeric() and len(k) > 1:
            d2[k] = d[k]
    pickle.dump(d2, f)
    f.close()

def unfamiliar(path,word):
    f = open(path,"rb")
    dic = pickle.load(f)
    dic[word] += [datetime.now().strftime('%Y%m%d%H%M')]
    fp = open(path,"wb")
    pickle.dump(dic,fp)

def familiar(path,word):
    f = open(path,"rb")
    dic = pickle.load(f)
    if len(dic[word])>1:
        del dic[word][0]
    else:
        dic.pop(word)
    fp = open(path,"wb")
    pickle.dump(dic,fp)

if __name__ == '__main__':

    lst1 = [('apple',2),  ('banana',1)]
    d = {}
    lst2dict(lst1, d) # d will change
    save_frequency_to_pickle(d, 'frequency.p') # frequency.p is our database


    lst2 = [('banana',2), ('orange', 4)]
    d = load_record('frequency.p')
    lst1 = dict2lst(d)
    d = merge_frequency(lst2, lst1)
    print(d)
