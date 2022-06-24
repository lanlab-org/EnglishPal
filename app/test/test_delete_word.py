# -*- coding: utf-8 -*-
# Run the docker image using the following command:
# docker run -d -p 4444:4444 selenium/standalone-chrome
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import random, time
import string

# 调用本地chromedriver
# driver = webdriver.Chrome(executable_path="D:\ChromeDriver\chromedriver.exe")
# driver.get("http://127.0.0.1:5000/")
driver = webdriver.Remote('http://localhost:4444/wd/hub', DesiredCapabilities.FIREFOX)
driver.implicitly_wait(10)
# driver.maximize_window()
# HOME_PAGE = "http://127.0.0.1:5000/"


HOME_PAGE = 'http://121.4.94.30:91/'


def test_delete_word():
    try:
        driver.get(HOME_PAGE)
        assert 'English Pal -' in driver.page_source
        # login
        elem = driver.find_element_by_link_text('登录')
        elem.click()

        uname = 'lanhui'
        password = 'l0ve1t'
        elem = driver.find_element_by_name('username')
        elem.send_keys(uname)

        elem = driver.find_element_by_name('password')
        elem.send_keys(password)

        elem = driver.find_element_by_xpath('//form[1]/p[3]/input[1]')  # 找到登录按钮
        elem.click()

        assert 'EnglishPal Study Room for ' + uname in driver.title

        # delete
        elems = driver.find_element_by_class_name('new-word')
        # 移动到元素elems对象的“顶端”与当前窗口的“顶部”对齐
        driver.execute_script("arguments[0].scrollIntoView();", elems)
        driver.save_screenshot('test_delete_pic1.png')
        current_2 = elems.text
        elem = driver.find_element_by_link_text("删除")
        elem.click()
        elems = driver.find_element_by_class_name('new-word')
        driver.execute_script("arguments[0].scrollIntoView();", elems)
        driver.save_screenshot('test_delete_pic2.png')
        now_2 = elems.text

        assert current_2 != now_2

    finally:
        driver.quit()

# test_delete_word()
