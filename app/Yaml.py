'''
Yaml.py
配置文件包括:
    ./static/config.yml
    ./layout/partial/header.html
    ./layout/partial/footer.html
'''
import yaml as YAML
import os

path_prefix = './'  # comment this line in deployment

# YAML文件路径
ymlPath = path_prefix + 'static/config.yml'

# partial文件夹路径
partialPath = path_prefix + 'layout/partial/'
f = open(ymlPath, 'r', encoding='utf-8') # 以'UTF-8'格式打开YAML文件
cont = f.read()  # 以文本形式读取YAML

yml = YAML.load(cont, Loader=YAML.FullLoader)  # 加载YAML

with open(partialPath + 'header.html', 'r', encoding='utf-8') as f:
    yml['header'] = f.read() # header内的文本会被直接添加到所有页面的head标签内

with open(partialPath + 'footer.html', 'r', encoding='utf-8') as f:
    yml['footer'] = f.read() # footer内的文本会被直接添加到所有页面的最底部
