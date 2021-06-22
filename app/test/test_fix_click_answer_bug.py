# -*- coding: utf-8 -*-
# Run the docker image using the following command:
# docker run -d -p 4444:4444 selenium/standalone-chrome
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
import random, time
import string

driver = webdriver.Remote('http://localhost:4444/wd/hub', DesiredCapabilities.CHROME)
driver.implicitly_wait(10)

HOME_PAGE = 'http://121.4.94.30:91/'


def has_punctuation(s):
    return [c for c in s if c in string.punctuation] != []


def test_fix_click_answer_bug():
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

        # get essay content
        elem = driver.find_element_by_xpath("/html/body/div/p[3]/font")
        ActionChains(driver).double_click(elem).perform()
        #find answer button, and click it twice
        answer = driver.find_element_by_xpath('/html/body/div/button')
        answer.click()
        answer.click()

        elem = driver.find_element_by_xpath('//form[1]//input[1]')  # 找到get所有词频按钮
        elem.click()

        preq = driver.find_element_by_xpath('/html/body/form/p[1]')
        assert preq.text.split()[2] == '(1)'
    finally:
        driver.quit()
