# -*- coding: utf-8 -*-
# Run the docker image using the following command:
# docker run -d -p 4444:4444 selenium/standalone-chrome
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import random, string, time

driver = webdriver.Remote('http://localhost:4444/wd/hub', DesiredCapabilities.CHROME)
driver.implicitly_wait(10)

HOME_PAGE = 'http://121.4.94.30:91/'



def test_next():
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
        driver.save_screenshot('./app/test/test_next_essay_pic0.png')    
        elem = driver.find_element_by_id('text-content')
        essay_content = elem.text
    
        # click Next
        differ = 0
        for i in range(3):
            elem = driver.find_element_by_link_text('下一篇')
            elem.click()
            driver.save_screenshot('./app/test/test_next_essay_pic1.png')
            elem = driver.find_element_by_id('text-content')
            current_essay_content = elem.text
    
            if current_essay_content != essay_content:
                diff = 1
                break
    
        assert diff == 1
    finally:
        driver.quit()

