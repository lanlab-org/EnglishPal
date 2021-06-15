# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random, time, string

driver = webdriver.Remote('http://localhost:4444/wd/hub', DesiredCapabilities.CHROME)
driver.implicitly_wait(10)
HOME_PAGE = 'http://121.4.94.30:91/'
#driver = webdriver.Chrome(executable_path="D:\GeckoDriver\chromedriver")
#driver.get("http://127.0.0.1:5000/")
driver.maximize_window()


def has_punctuation(s):
    return [c for c in s if c in string.punctuation] != []

def test_familiar_unfamiliar():
    try:
        driver.get("http://121.4.94.30:91/")
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

        # 熟悉
        elems = driver.find_element_by_class_name('new-word')
        driver.execute_script("arguments[0].scrollIntoView();",elems)
        current = elems.text
        time.sleep(4)
        driver.save_screenshot('test_familiar_pic1.png')
        elem = driver.find_element_by_link_text('熟悉')
        elem.click()
        elems = driver.find_element_by_class_name('new-word')
        now = elems.text
        driver.execute_script("arguments[0].scrollIntoView();",elems)
        driver.save_screenshot('test_familiar_pic2.png')
        time.sleep(4)
        assert current != now

        driver.refresh()
        # 不熟悉
        elems = driver.find_element_by_class_name('new-word')
        driver.execute_script("arguments[0].scrollIntoView();",elems)
        driver.save_screenshot('test_unfamiliar_pic1.png')
        current_2 = elems.text
        elem = driver.find_element_by_link_text("不熟悉")
        elem.click()
        elems = driver.find_element_by_class_name('new-word')
        driver.execute_script("arguments[0].scrollIntoView();",elems)
        driver.save_screenshot('test_unfamiliar_pic2.png')
        now_2 = elems.text
        time.sleep(4)
        assert current_2 != now_2

    finally:
        driver.quit()
