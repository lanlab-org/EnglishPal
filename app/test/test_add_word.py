# -*- coding: utf-8 -*-
# Run the docker image using the following command:
# docker run -d -p 4444:4444 selenium/standalone-chrome
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import random, time
import string

driver = webdriver.Remote('http://localhost:4444/wd/hub', DesiredCapabilities.CHROME)
driver.implicitly_wait(10)

HOME_PAGE = 'http://121.4.94.30:91/'


def has_punctuation(s):
    return [c for c in s if c in string.punctuation] != []
    
def test_add_word():
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
        
        elem = driver.find_element_by_xpath('//form[1]/p[3]/input[1]') # 找到登录按钮
        elem.click()
    
        assert 'EnglishPal Study Room for ' + uname in  driver.title
    
        # get essay content
        elem = driver.find_element_by_id('text-content')
        essay_content = elem.text
    
        elem = driver.find_element_by_id('selected-words')
        word = random.choice(essay_content.split())
        while 'font>' in word or 'br>' in word or 'p>' in word or len(word) < 5 or has_punctuation(word):
            word = random.choice(essay_content.split())        

        elem.send_keys(word)

        elem = driver.find_element_by_xpath('//form[1]//input[1]') # 找到get所有词频按钮
        elem.click()
    
        elems = driver.find_elements_by_xpath("//input[@type='checkbox']")
        for elem in elems:
            if elem.get_attribute('name') == 'marked':
                elem.click()
    
        elem = driver.find_element_by_name('add-btn') # 找到加入我的生词簿按钮
        elem.click()

        driver.refresh()
        driver.refresh()
        driver.refresh()        
        elems = driver.find_elements_by_xpath("//p[@class='new-word']/a")
    
        found = 0
        for elem in elems:
            if word in elem.text:
                found = 1
                break
    
        assert found == 1
    finally:    
        driver.quit()
