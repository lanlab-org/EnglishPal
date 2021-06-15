###########################################################################
# Copyright 2019 (C) Hui Lan <hui.lan@cantab.net>
# Written permission must be obtained from the author for commercial uses.
###########################################################################

from wordfreqCMD import remove_punctuation, freq, sort_in_descending_order
import string
import pickle_idea, pickle_idea2
import os

class WordFreq:
    def __init__(self, s):
        self.s = remove_punctuation(s)

    def get_freq(self):
        lst = []
        for t in freq(self.s):
            word = t[0]
            if len(word) > 0 and word[0] in string.ascii_letters:
                lst.append(t)
        return sort_in_descending_order(lst)


def load_freq_history(path):
    d = {}
    if os.path.exists(path):
        d = pickle_idea.load_record(path)
    return d

if __name__ == '__main__':
    f = WordFreq('BANANA; Banana, apple ORANGE Banana banana.')
    print(f.get_freq())

