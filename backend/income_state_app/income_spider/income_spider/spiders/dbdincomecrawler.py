import os, time, pickle
import scrapy
from scrapy.spiders import CrawlSpider
import logging
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from income_spider.items import *

class IncomeStatementCrawlerSpider(CrawlSpider):
    name = 'dbdincomecrawler'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
    }
    allowed_domains = ["datawarehouse.dbd.go.th"]
    # custom_settings = {
    #     'ITEM_PIPELINES': {'scrapy_thai_app.thai_spider.thai_spider.pipelines.ThaiSpiderPipeline': 400,}
    # }

    def __init__(self, cid=None, *args, **kwargs):
        self.cid = cid
        logging.info(self.cid)
        super(IncomeStatementCrawlerSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        companies_id = self.cid
        print(companies_id)
        for i in ['0105554123553', '0103563015316']:
            url = 'https://datawarehouse.dbd.go.th/fin/profitloss/%s/%s' %(i[3],i)
            cookie = 'YzJlMTZiYmQtYjc2ZC00MDQxLTgyZTAtMDg3NGU5ZmQ5ZjBj'
            yield scrapy.Request(url=url, 
                                cookies={"JSESSIONID":cookie},
                                callback=self.parse,
                                cb_kwargs=dict(raw_company_id=i, cookie=cookie),
                                encoding='utf-8')

    def parse(self, responese, raw_company_id, cookie):
        try:
            CHROME_DRIVER = os.path.expanduser('/usr/bin/chromedriver')
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu') # applicable to windows os only
            chrome_options.add_argument('--no-sandbox') # Bypass OS security model
            chrome_options.add_argument('--disable-dev-shm-usage') # overcome limited resource problems
            chrome_options.add_argument("--window-size=1920,1080")
            driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=chrome_options)

            driver.get("https://datawarehouse.dbd.go.th/")
            driver.add_cookie({'name':'JSESSIONID', 'value':cookie})
            driver.get('https://datawarehouse.dbd.go.th/fin/profitloss/%s/%s' %(raw_company_id[3],raw_company_id))
            time.sleep(5)

            with open('/backend/income_state_app/income_spider/income_state.json', 'w'):
                pass
            
            raw_company_id = driver.find_element_by_xpath('//*[@id="finContent"]/div/div[1]/div/div[1]/p').text.strip()
            company_id = raw_company_id.rpartition(':')[-1]
            all_year = []
            for i in range(2,5):
                year = driver.find_element_by_xpath('//*[@id="fixTable"]/thead/tr[%s]/th[%s]'%(1,i)).text.strip()
                if year == '':
                    year = 'N/A'
                all_year.append(year)

            y_item = IncomeYearDetailItem()
            for i in range(1,11):
                y_item['company_id']    = company_id.strip()
                y_item['year']          = all_year[0]
                y_item['amount']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,2)).text.strip()
                y_item['change']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,3)).text.strip()
                yield y_item
            for i in range(1,11):
                y_item['company_id']    = company_id.strip()
                y_item['year']          = all_year[1]
                y_item['amount']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,4)).text.strip()
                y_item['change']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,5)).text.strip()
                yield y_item
            for i in range(1,11):
                y_item['company_id']    = company_id.strip()
                y_item['year']          = all_year[2]
                y_item['amount']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,6)).text.strip()
                y_item['change']        = driver.find_element_by_xpath('//*[@id="fixTable"]/tbody/tr[%s]/td[%s]'%(i,7)).text.strip()
                yield y_item
                
        except Exception as e:
            print(e)