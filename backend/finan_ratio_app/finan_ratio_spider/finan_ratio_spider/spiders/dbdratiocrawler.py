# import needed lib
import os, time, pickle
import scrapy
from scrapy.spiders import CrawlSpider
import logging
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
# import own lib
from finan_ratio_app.finan_ratio_spider.finan_ratio_spider.items import *
from finan_ratio_app.models import *

class FinancialRatioCrawlerSpider(CrawlSpider):
    # scrapy basic setting
    name = 'dbdratiocrawler'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
    }
    allowed_domains = ["datawarehouse.dbd.go.th"]
    custom_settings = {
        'ITEM_PIPELINES': {'finan_ratio_app.finan_ratio_spider.finan_ratio_spider.pipelines.FinanRatioSpiderPipeline': 400,}
    }

    # before start to scrape, get companies' id which need to scrape
    def __init__(self, cid=None, id_start_num=None, *args, **kwargs):
        self.cid = cid
        self.id_start_num = id_start_num
        logging.info(self.cid)
        super(FinancialRatioCrawlerSpider, self).__init__(*args, **kwargs)

    # scrapy requests, the link is made up of company id
    def start_requests(self):
        companies_id = self.cid
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
            url = 'https://datawarehouse.dbd.go.th/fin/ratio/%s/%s' %(i[3],i)
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

    def parse(self, responese, raw_company_id, cookie, driver):
        print('Scrapy and store ratio year details for company: ' + raw_company_id + ' ...')
        logging.info('Scrapy and store ratio year details for company: ' + raw_company_id + ' ...')
        
        # check whether the company already scraped into ratio year info
        qs = RatioYear.objects.filter(company_id=raw_company_id)
        if qs.exists():
            # if scraped, delete and update info
            RatioYear.objects.filter(company_id=raw_company_id).delete()
            print('Deleting...')
            try:
                # use Selenium to get terminal website
                # get first page --> login
                driver.get("https://datawarehouse.dbd.go.th/")
                # send the cookie to login into website
                driver.add_cookie({'name':'JSESSIONID', 'value':cookie})
                # get terminal website
                driver.get('https://datawarehouse.dbd.go.th/fin/ratio/%s/%s' %(raw_company_id[3],raw_company_id))
                time.sleep(7)
                
                # start to scrape data
                raw_company_id = driver.find_element_by_xpath('//*[@id="finContent"]/div/div[1]/div/div[1]/p').text.strip()
                company_id = raw_company_id.rpartition(':')[-1]
                all_year = []
                for i in range(3,6):
                    year = driver.find_element_by_xpath('//*[@id="fixTable"]/thead[1]/tr[%s]/th[%s]'%(1,i)).text.strip()
                    if year == '':
                        year = 'N/A'
                    all_year.append(year)

                y_item = RatioYearItem()
                for i in range(3,6):
                    if i == 3:
                        year = all_year[0]
                    if i == 4:
                        year = all_year[1]
                    if i == 5:
                        year = all_year[2]
                    for j in range(1,6):
                        y_item['company_id']    = company_id.strip()
                        y_item['year']          = year
                        y_item['ratio']         = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody[1]/tr[%s]/td[%s]'%(j,i)).text.strip()
                        yield y_item 
                    for j in range(1,5):
                        y_item['company_id']    = company_id.strip()
                        y_item['year']          = year
                        y_item['ratio']         = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody[2]/tr[%s]/td[%s]'%(j,i)).text.strip()
                        yield y_item
                    for j in range(1,3):
                        y_item['company_id']    = company_id.strip()
                        y_item['year']          = year
                        y_item['ratio']         = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody[3]/tr[%s]/td[%s]'%(j,i)).text.strip()
                        yield y_item
                    for j in range(1,5):
                        y_item['company_id']    = company_id.strip()
                        y_item['year']          = year
                        y_item['ratio']         = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody[4]/tr[%s]/td[%s]'%(j,i)).text.strip()
                        yield y_item 
                    
            except Exception as e:
                print(e)

        else:
            # if not, scrape directly
            try:
                driver.get("https://datawarehouse.dbd.go.th/")
                driver.add_cookie({'name':'JSESSIONID', 'value':cookie})
                driver.get('https://datawarehouse.dbd.go.th/fin/ratio/%s/%s' %(raw_company_id[3],raw_company_id))
                time.sleep(7)
                
                raw_company_id = driver.find_element_by_xpath('//*[@id="finContent"]/div/div[1]/div/div[1]/p').text.strip()
                company_id = raw_company_id.rpartition(':')[-1]
                all_year = []
                for i in range(3,6):
                    year = driver.find_element_by_xpath('//*[@id="fixTable"]/thead[1]/tr[%s]/th[%s]'%(1,i)).text.strip()
                    if year == '':
                        year = 'N/A'
                    all_year.append(year)

                y_item = RatioYearItem()
                for i in range(3,6):
                    if i == 3:
                        year = all_year[0]
                    if i == 4:
                        year = all_year[1]
                    if i == 5:
                        year = all_year[2]
                    for j in range(1,6):
                        y_item['company_id']    = company_id.strip()
                        y_item['year']          = year
                        y_item['ratio']         = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody[1]/tr[%s]/td[%s]'%(j,i)).text.strip()
                        yield y_item 
                    for j in range(1,5):
                        y_item['company_id']    = company_id.strip()
                        y_item['year']          = year
                        y_item['ratio']         = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody[2]/tr[%s]/td[%s]'%(j,i)).text.strip()
                        yield y_item
                    for j in range(1,3):
                        y_item['company_id']    = company_id.strip()
                        y_item['year']          = year
                        y_item['ratio']         = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody[3]/tr[%s]/td[%s]'%(j,i)).text.strip()
                        yield y_item
                    for j in range(1,5):
                        y_item['company_id']    = company_id.strip()
                        y_item['year']          = year
                        y_item['ratio']         = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody[4]/tr[%s]/td[%s]'%(j,i)).text.strip()
                        yield y_item 
                    
            except Exception as e:
                print(e)
