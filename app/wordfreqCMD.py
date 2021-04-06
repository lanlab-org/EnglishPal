###########################################################################
# Copyright 2019 (C) Hui Lan <hui.lan@cantab.net>
# Written permission must be obtained from the author for commercial uses.
###########################################################################

import collections
import string
import operator
import os, sys # 引入模块sys，因为我要用里面的sys.argv列表中的信息来读取命令行参数。
import pickle_idea

def freq(fruit):
    '''
    功能： 把字符串转成列表。 目的是得到每个单词的频率。
    输入： 字符串
    输出： 列表， 列表里包含一组元组，每个元组包含单词与单词的频率。 比如 [('apple', 2), ('banana', 1)]
    注意事项： 首先要把字符串转成小写。原因是。。。
    '''

    result = []
    
    fruit = fruit.lower() # 字母转小写
    flst = fruit.split()  # 字符串转成list
    c = collections.Counter(flst)
    result = c.most_common()
    return result


def youdao_link(s): # 有道链接
    link = 'http://youdao.com/w/eng/' + s + '/#keyfrom=dict2.index'# 网址
    return link


def file2str(fname):#文件转字符
    f = open(fname) #打开
    s = f.read()    #读取
    f.close()       #关闭
    return s


def remove_punctuation(s): # 这里是s是形参 (parameter)。函数被调用时才给s赋值。
    special_characters = '_©~=+[]*&$%^@.,?!:;#()"“”—‘’' # 把里面的字符都去掉
    for c in special_characters:
        s = s.replace(c, ' ') # 防止出现把 apple,apple 移掉逗号后变成 appleapple 情况
    s = s.replace('--', ' ')
    s = s.strip() # 去除前后的空格
    
    if '\'' in s:
        n = len(s)
        t = '' # 用来收集我需要保留的字符
        for i in range(n): # 只有单引号前后都有英文字符，才保留
            if s[i] == '\'':
                i_is_ok = i - 1 >= 0 and i + 1 < n
                if i_is_ok and s[i-1] in string.ascii_letters and s[i+1] in string.ascii_letters:
                    t += s[i]
            else:
                t += s[i]
        return t
    else:
        return s


def sort_in_descending_order(lst):# 单词按频率降序排列
    lst2 = sorted(lst, reverse=True, key=lambda x: (x[1], x[0]))
    return lst2


def sort_in_ascending_order(lst):# 单词按频率降序排列
    lst2 = sorted(lst, reverse=False, key=lambda x: (x[1], x[0]))
    return lst2


def make_html_page(lst, fname):
    '''
    功能：把lst的信息存到fname中，以html格式。
    '''
    s = ''
    count = 1
    for x in lst:
        # <a href="">word</a>
        s += '<p>%d <a href="%s">%s</a> (%d)</p>' % (count, youdao_link(x[0]), x[0], x[1])
        count += 1
    f = open(fname, 'w')
    f.write(s)
    f.close()


## main（程序入口）
if __name__ == '__main__':
    num = len(sys.argv)

    if num == 1: # 从键盘读入字符串
        s = input()
    elif num == 2: # 从文件读入字符串
        fname = sys.argv[1]
        s = file2str(fname)
    else:
        print('I can accept at most 2 arguments.')
        sys.exit()# 结束程序运行， 下面的代码不会被执行了。

    s = remove_punctuation(s) # 这里是s是实参(argument)，里面有值
    L = freq(s)
    for x in sort_in_descending_order(L):
        print('%s\t%d\t%s' % (x[0], x[1], youdao_link(x[0])))#函数导出

    # 把频率的结果放result.html中
    make_html_page(sort_in_descending_order(L), 'result.html') 

    print('\nHistory:\n')
    if os.path.exists('frequency.p'):
        d = pickle_idea.load_record('frequency.p')
    else:
        d = {}

    print(sort_in_descending_order(pickle_idea.dict2lst(d)))

    # 合并频率
    lst_history = pickle_idea.dict2lst(d)
    d = pickle_idea.merge_frequency(L, lst_history)
    pickle_idea.save_frequency_to_pickle(d, 'frequency.p')



