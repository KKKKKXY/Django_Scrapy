import os, time, re, pickle, signal
from selenium import webdriver
import pytesseract
from PIL import Image
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import scrapy

# Selenium Part
# Setting driver
CHROME_DRIVER = os.path.expanduser('/usr/bin/chromedriver')
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=chrome_options)
# driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.maximize_window()
screenshot_path =  '/backend/temp/screenshot.png'
login_page_url = 'https://datawarehouse.dbd.go.th/login'
cookie_path = '/backend/temp/cookie.json'

# Access login page
driver.get(login_page_url)
print(driver.title)

# get and verify captcha, then access 'https://datawarehouse.dbd.go.th/index' page 
def getCaptchaAndLogin():
    # Screenshot captcha code and store into 'screenshot_path'
    for i in range(100):
        time.sleep(3)
        sshot = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/div[2]/div/div[2]/form/div[1]/span/img')
        sshot.screenshot(screenshot_path)

        # Convert image to string
        captchaCode = pytesseract.image_to_string(Image.open(screenshot_path)).strip().replace(" ","")
        print(captchaCode)
        print("Length is " + str(len(captchaCode)))

        if len(captchaCode) == 5 and re.match('^[A-Za-z0-9]+$',captchaCode): 
            # Send captcha code in input box and access 'https://datawarehouse.dbd.go.th/index' page
            driver.find_element_by_xpath('//*[@id="captchaCode"]').send_keys(captchaCode) 
            # driver.find_element_by_xpath('//*[@id="captchaCode"]').send_keys(u'\ue007') 
            driver.find_element_by_xpath('//*[@id="signinBtn"]').click()
            if 'Home' in driver.title: 
                break
            driver.refresh()
        else:
            driver.refresh()

def storeCookie():
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
            # return(i)
        else:
            print('no JSESSIONID in this page!')

# def getAndStoreCookieAfterLogin():
#     for i in range(10):
#         time.sleep(10)
#         if 'Home' in driver.title:
#             # load cookie
#             cookies = driver.get_cookies()
#             # find token 'JSESSIONID' and store it into cookie_path
#             for i in cookies:
#                 # print(i)
#                 if i['name'] == 'JSESSIONID':
                    
#                     with open(cookie_path, 'wb') as f:
#                         pickle.dump(cookies, f)
#                     print(i['value'])
#                     break
#                 else:
#                     print('no JSESSIONID in this page!')
#             break
#         else:
#             driver.refresh()

# check whether access 'https://datawarehouse.dbd.go.th/index' page successfully
# getAndStoreCookieAfterLogin()
getCaptchaAndLogin()
storeCookie()