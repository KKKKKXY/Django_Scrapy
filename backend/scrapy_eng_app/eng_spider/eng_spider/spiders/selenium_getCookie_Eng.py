# import os, time, re, pickle, signal
# from selenium import webdriver
# import pytesseract
# from PIL import Image
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import TimeoutException
# import scrapy
# from string import Template
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# # Selenium Part
# # Setting driver
# CHROME_DRIVER = os.path.expanduser('/usr/bin/chromedriver')
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu') # applicable to windows os only
# chrome_options.add_argument('--no-sandbox') # Bypass OS security model
# chrome_options.add_argument('--disable-dev-shm-usage') # overcome limited resource problems
# driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=chrome_options)

# driver.maximize_window()
# screenshot_path =  '/backend/temp/screenshot.png'
# login_page_url = 'https://datawarehouse.dbd.go.th/login'
# cookie_path = '/backend/temp/cookie.json'

# # Access login page
# driver.get(login_page_url)
# print(driver.title)

# # get and verify captcha, then access 'https://datawarehouse.dbd.go.th/index' page 
# def getCaptchaAndLogin():
#     print('Getting Screenshot...')
#     # Screenshot captcha code and store into 'screenshot_path'
#     for i in range(100):
#         sshot = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/div[2]/div/div[2]/form/div[1]/span/img')
#         sshot.screenshot(screenshot_path)
#         time.sleep(2)

#         captchaCode = ''
#         # user input 
#         user_input = input("Enter captcha code: ")
#         captchaCode = user_input
#         print ("The captcha code you entered is: ", captchaCode)

#         if len(captchaCode) == 5 and re.match('^[A-Za-z0-9]+$',captchaCode): 
#             # Send captcha code in input box and access 'https://datawarehouse.dbd.go.th/index' page
#             driver.find_element_by_xpath('//*[@id="captchaCode"]').send_keys(captchaCode) 
#             driver.find_element_by_xpath('//*[@id="signinBtn"]').click()
#             if 'Home' in driver.title:
#                 print('Login Success!!!')
#                 message_template = read_template('/backend/email_msg/login_sucess.txt')
#                 message = Mail(
#                     from_email='myaploy@gmail.com',
#                     to_emails='xingyuan_kang@elearning.cmu.ac.th',
#                     subject='Inform: Login success!',
#                     html_content=message_template.substitute(CAPTCHACODE=captchaCode)
#                 )
#                 try:
#                     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#                     response = sg.send(message)
#                     print('The server response code is: ' + str(response.status_code))
#                     print('Message Send.')
#                     print('Start scrapying...')
#                     time.sleep(3)
#                 except Exception as e:
#                     print(e)
#                 break
#             else:
#                 print('Oops!!! The capcha code is expired, please check your inbox message!')
#                 driver.get(login_page_url)
#                 message_template = read_template('/backend/email_msg/cookie_expired.txt')
#                 message = Mail(
#                     from_email='myaploy@gmail.com',
#                     to_emails='xingyuan_kang@elearning.cmu.ac.th',
#                     subject='Warning: Captcha code expired!',
#                     html_content=message_template.substitute(CAPTCHACODE=captchaCode)
#                 )
#                 try:
#                     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#                     response = sg.send(message)
#                     print('The server response code is: ' + str(response.status_code))
#                     print('Message Send.')
#                 except Exception as e:
#                     print(e)
#         else:
#             print('The capcha code is invalid, please check your inbox message!')
#             driver.refresh()
#             message_template = read_template('/backend/email_msg/cookie_invalid.txt')
#             message = Mail(
#                     from_email='myaploy@gmail.com',
#                     to_emails='xingyuan_kang@elearning.cmu.ac.th',
#                     subject='Warning: Invalid Captcha code!',
#                     html_content=message_template.substitute(CAPTCHACODE=captchaCode)
#             ) 
#             try:
#                 sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#                 response = sg.send(message)
#                 print('The server response code is: ' + str(response.status_code))
#                 print('Message Send.')
#             except Exception as e:
#                 print(e)

# def storeCookie():
#     # load cookie
#     cookies = driver.get_cookies()
#     # find token 'JSESSIONID' and store it into cookie_path
#     for i in cookies:
#         if i['name'] == 'JSESSIONID':
#             with open(cookie_path, 'wb') as f:
#                 pickle.dump(cookies, f)
#             print('Current website token is: ' + i['value'])
#             break
#         else:
#             print('no JSESSIONID in this page!')

# def read_template(filename):
#     with open(filename, 'r', encoding='utf-8') as template_file:
#         template_file_content = template_file.read()
#     return Template(template_file_content)

# # check whether access 'https://datawarehouse.dbd.go.th/index' page successfully
# getCaptchaAndLogin()
# storeCookie()

# # Change language
# driver.find_element_by_xpath('//*[@id="lang"]').click()