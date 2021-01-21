import os, time, re, pickle, signal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import scrapy

# Selenium Part
# Setting driver
driver = webdriver.Chrome('/backend/chromedriver')
driver.maximize_window()
screenshot_path =  '/backend/scrapy/crawler/crawler/spiders/temp/screenshot.png'
login_page_url = 'https://datawarehouse.dbd.go.th/login'
cookie_path = '/backend/scrapy/crawler/crawler/spiders/temp/cookie.json'

# Access login page
driver.get(login_page_url)
print(driver.title)

# get and verify captcha, then access 'https://datawarehouse.dbd.go.th/index' page 
def getAndStoreCookieAfterLogin():
    for i in range(10):
        time.sleep(10)
        if 'Home' in driver.title:
            # load cookie
            cookies = driver.get_cookies()
            # find token 'JSESSIONID' and store it into cookie_path
            for i in cookies:
                # print(i)
                if i['name'] == 'JSESSIONID':
                    
                    with open(cookie_path, 'wb') as f:
                        pickle.dump(cookies, f)
                    print(i['value'])
                    break
                else:
                    print('no JSESSIONID in this page!')
            break
        else:
            driver.refresh()

# check whether access 'https://datawarehouse.dbd.go.th/index' page successfully
getAndStoreCookieAfterLogin()