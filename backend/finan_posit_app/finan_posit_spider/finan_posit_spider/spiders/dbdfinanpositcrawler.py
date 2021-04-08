# import needed lib
import os, time, pickle
import scrapy
from scrapy.spiders import CrawlSpider
import logging
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
# import own lib
from finan_posit_app.finan_posit_spider.finan_posit_spider.items import *
# from scrapy_thai_app.thai_spider.thai_spider.items import *
from finan_posit_app.models import *

class FinancialPositionCrawlerSpider(CrawlSpider):
    # scrapy basic setting
    name = 'dbdfinanpositcrawler'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
    }
    allowed_domains = ["datawarehouse.dbd.go.th"]
    custom_settings = {
        'ITEM_PIPELINES': {'finan_posit_app.finan_posit_spider.finan_posit_spider.pipelines.FinanPositSpiderPipeline': 400,}
    }

    # before start to scrape, get companies' id which need to scrape
    def __init__(self, cid=None, id_start_num=None, *args, **kwargs):
        self.cid = cid
        self.id_start_num = id_start_num
        logging.info(self.cid)
        super(FinancialPositionCrawlerSpider, self).__init__(*args, **kwargs)

    # scrapy requests, the link is made up of company id
    def start_requests(self):
        companies_id = self.cid
        # for i in ['0105554123553', '0135563023787']:
        # setting driver
        try:
            CHROME_DRIVER = os.path.expanduser('/usr/bin/chromedriver')
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu') # applicable to windows os only
            chrome_options.add_argument('--no-sandbox') # Bypass OS security model
            chrome_options.add_argument('--disable-dev-shm-usage') # overcome limited resource problems
            chrome_options.add_argument("--window-size=1920,1080")
            driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=chrome_options)
        except Exception as e:
            print(e)

        for i in companies_id:
            url = 'https://datawarehouse.dbd.go.th/fin/balancesheet/%s/%s' %(i[3],i)
            cookie = self.getCookie()
            # request url and pass argument
            yield scrapy.Request(url=url, 
                                cookies={"JSESSIONID":cookie},
                                callback=self.parse,
                                cb_kwargs=dict(raw_company_id=i, cookie=cookie, driver=driver),
                                encoding='utf-8')

    # get cookie permission from 'cookie.json' file
    def getCookie(self):
        cookie_path = '/backend/temp/cookie.json'
        if os.path.isfile(cookie_path):
            try:
                with open(cookie_path, 'rb') as f: 
                    cookies = pickle.load(f)
            except EOFError:
                cookies = None

        for i in cookies:
            if i['name']=='JSESSIONID':
                cookies= i['value']
                break
        return cookies

    def parse(self, response, raw_company_id, cookie, driver):
        print('Scrapy and store financial year details for company: ' + raw_company_id + ' ...')
        logging.info('Scrapy and store financial year details for company: ' + raw_company_id + ' ...')
        
        # check whether the company already scraped into position year info
        qs = PositYear.objects.filter(company_id=raw_company_id)
        if qs.exists():
            # if scraped, delete and update info
            PositYear.objects.filter(company_id=raw_company_id).delete()
            print('Deleting...')
            try:
                # use Selenium to get terminal website
                # get first page --> login
                driver.get("https://datawarehouse.dbd.go.th/")
                # send the cookie to login into website
                driver.add_cookie({'name':'JSESSIONID', 'value':cookie})
                # get terminal website
                driver.get('https://datawarehouse.dbd.go.th/fin/balancesheet/%s/%s' %(raw_company_id[3],raw_company_id))
                time.sleep(7)
                
                # start to scrape data
                raw_company_id = driver.find_element_by_xpath('//*[@id="finContent"]/div/div[1]/div/div[1]/p').text.strip()
                company_id = raw_company_id.rpartition(':')[-1]
                all_year = []
                for i in range(2,5):
                    year = driver.find_element_by_xpath('//*[@id="fixTable"]/thead/tr[%s]/th[%s]'%(1,i)).text.strip()
                    if year == '':
                        year = 'N/A'
                    all_year.append(year)

                y_item = PositYearItem()
                for i in range(1,12):
                    y_item['company_id']    = company_id.strip()
                    y_item['year']          = all_year[0]
                    y_item['amount']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,2)).text.strip()
                    y_item['change']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,3)).text.strip()
                    yield y_item
                for i in range(1,12):
                    y_item['company_id']    = company_id.strip()
                    y_item['year']          = all_year[1]
                    y_item['amount']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,4)).text.strip()
                    y_item['change']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,5)).text.strip()
                    yield y_item
                for i in range(1,12):
                    y_item['company_id']    = company_id.strip()
                    y_item['year']          = all_year[2]
                    y_item['amount']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,6)).text.strip()
                    y_item['change']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,7)).text.strip()
                    yield y_item
                    
            except Exception as e:
                print(e)
        else:
            # if not, scrape directly
            try:
                driver.get("https://datawarehouse.dbd.go.th/")
                driver.add_cookie({'name':'JSESSIONID', 'value':cookie})
                driver.get('https://datawarehouse.dbd.go.th/fin/balancesheet/%s/%s' %(raw_company_id[3],raw_company_id))
                time.sleep(7)
                
                raw_company_id = driver.find_element_by_xpath('//*[@id="finContent"]/div/div[1]/div/div[1]/p').text.strip()
                company_id = raw_company_id.rpartition(':')[-1]
                all_year = []
                for i in range(2,5):
                    year = driver.find_element_by_xpath('//*[@id="fixTable"]/thead/tr[%s]/th[%s]'%(1,i)).text.strip()
                    if year == '':
                        year = 'N/A'
                    all_year.append(year)

                y_item = PositYearItem()
                for i in range(1,12):
                    y_item['company_id']    = company_id.strip()
                    y_item['year']          = all_year[0]
                    y_item['amount']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,2)).text.strip()
                    y_item['change']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,3)).text.strip()
                    yield y_item
                for i in range(1,12):
                    y_item['company_id']    = company_id.strip()
                    y_item['year']          = all_year[1]
                    y_item['amount']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,4)).text.strip()
                    y_item['change']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,5)).text.strip()
                    yield y_item
                for i in range(1,12):
                    y_item['company_id']    = company_id.strip()
                    y_item['year']          = all_year[2]
                    y_item['amount']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,6)).text.strip()
                    y_item['change']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,7)).text.strip()
                    yield y_item
                    
            except Exception as e:
                print(e)


        # # driver.maximize_window()
        # # driver.execute_script("window.open()")
        # # print(driver.window_handles)
        # time.sleep(10)
        # driver.get_screenshot_as_file('aaaaaaaaaa.png')

        # # print(driver.window_handles)
        # # driver.add_cookie({'name':'JSESSIONID', 'value':'OTJjODE0NWEtZGUyOC00OTM4LTgwMDYtOGI5MmMxODQzMzk0'})
        # # driver.get("https://datawarehouse.dbd.go.th/company/profile/5/0105554123553")

        # sshot = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/div[2]/div/div[2]/form/div[1]/span/img')
        # sshot.screenshot('s.png')
        # print('Enter your cap code:')
        # cap = input()
        # driver.find_element_by_xpath('//*[@id="captchaCode"]').send_keys(cap)
        # driver.find_element_by_xpath('//*[@id="signinBtn"]').click()
        # time.sleep(10)
        # driver.get_screenshot_as_file('bbbbbbbbbb.png')

        # driver.find_element_by_name('textStr').send_keys('0105554123553')
        # driver.find_element_by_xpath('//*[@id="form"]/div[2]/div/div/div[2]/button').click()
        # time.sleep(10)
        # driver.get_screenshot_as_file('cccccccccc.png')

        # driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr/td[2]').click()
        # # time.sleep(10)
        # # driver.get_screenshot_as_file('dddddddddd.png')

        # driver.switch_to_window(driver.window_handles[0])
        # driver.get("https://datawarehouse.dbd.go.th/fin/balancesheet/5/0105554123553")
        # # driver.find_element_by_xpath('//*[@id="navsidebar"]/ul/li[2]/a').click()
        # time.sleep(10)
        # driver.get_screenshot_as_file('eeeeeeeeee.png')