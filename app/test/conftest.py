import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

@pytest.fixture
def URL():
    return 'http://127.0.0.1:5000' # URL of the program


@pytest.fixture
def driver():
    my_driver = webdriver.Edge()  # uncomment this line if you wish to run the test on your laptop    
    return my_driver
