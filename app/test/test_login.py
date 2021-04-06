# -*- coding: utf-8 -*-
# Run the docker image using the following command:
# docker run -d -p 4444:4444 selenium/standalone-chrome
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import random, string

driver = webdriver.Remote('http://localhost:4444/wd/hub', DesiredCapabilities.CHROME)
driver.implicitly_wait(10)

HOME_PAGE = 'http://121.4.94.30:91/'



def test_login():
    try:
        driver.get(HOME_PAGE)
        driver.save_screenshot('./app/test/test_login_pic0.png')
        
        assert 'English Pal -' in driver.page_source
    
        elem = driver.find_element_by_link_text('成为会员')
        elem.click()
    
        uname = ''.join ( [random.choice (string.ascii_letters) for x in range (8)] )
        elem = driver.find_element_by_name('username')
        elem.send_keys(uname)
    
        elem = driver.find_element_by_name('password')
        elem.send_keys('iamc00l!')
    
        driver.save_screenshot('./app/test/test_login_pic1.png')
        
        elem = driver.find_element_by_xpath('//form[1]/p[3]/input[1]') # 找到注册按钮
        elem.click()
    
        driver.save_screenshot('./app/test/test_login_pic2.png')
        
        assert '恭喜，你已成功注册' in driver.page_source
        assert uname in driver.page_source
    
        # logout
        driver.get(HOME_PAGE + 'logout')
        driver.save_screenshot('./app/test/test_login_pic3.png')
        
        # login
        elem = driver.find_element_by_link_text('登录')
        elem.click()
    
        elem = driver.find_element_by_name('username')
        elem.send_keys(uname)
    
        elem = driver.find_element_by_name('password')
        elem.send_keys('iamc00l!')
        
        elem = driver.find_element_by_xpath('//form[1]/p[3]/input[1]') # 找到登录按钮
        elem.click()
    
        driver.save_screenshot('./app/test/test_login_pic4.png')    
        assert 'EnglishPal Study Room for ' + uname in  driver.title
    finally:
        driver.quit()
