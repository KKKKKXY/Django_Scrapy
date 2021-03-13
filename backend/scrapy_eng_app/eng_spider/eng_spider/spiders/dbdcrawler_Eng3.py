import os, time, pickle
import scrapy
from scrapy.spiders import CrawlSpider
import logging

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('.'))))
from scrapy_eng_app.eng_spider.eng_spider.items import EngSpiderItem
from data_reader.excel_reader import *
from data_reader.pdf_reader import *

class DbdcrawlerSpider3(CrawlSpider):
    name = "dbdcrawler_Eng3"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    allowed_domains = ["datawarehouse.dbd.go.th"]
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_eng_app.eng_spider.eng_spider.pipelines.EngSpiderPipeline': 300,}
    }

    def __init__(self, cid=None, *args, **kwargs):
        self.cid = cid
        logging.info(self.cid)
        super(DbdcrawlerSpider3, self).__init__(*args, **kwargs)

    def start_requests(self):
        companies_id = self.cid
        print(companies_id)
        for i in companies_id:
            url = 'https://datawarehouse.dbd.go.th/company/profile/%s/%s' %(i[3],i)
            yield scrapy.Request(url=url, cookies={"JSESSIONID":self.getCookie()}, callback=self.parse, encoding='utf-8')

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

    def parse(self, response):
        print('------------START SCRAPING BROWSER 3------------')
        logging.warning('------------START SCRAPING BROWSER 3------------')
        time.sleep(5)
        objective = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[3]/div/p/text()').get()
        if objective == None:
            objective = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[5]/div/p/text()').get().strip()
        else:
            objective = objective.strip()

        director_list = []
        directors = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/ol/li/text()').getall()
        for i in directors:
            director_list.append(i.strip())

        raw_bussiness_type = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/div/p/text()').get()
        if raw_bussiness_type == None or raw_bussiness_type.strip() == 'No Data':
            # print(True)
            raw_bussiness_type = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/div/p/text()').get().strip()
        else:
            # print(False)
            raw_bussiness_type = raw_bussiness_type.strip()

        tel = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/table/tr[3]/td[2]/text()').get()
        if tel == None:
            tel = '-'
        else:
            tel = tel.strip()

        fax = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/table/tr[4]/td[2]/text()').get()
        if fax == None:
            fax = '-'
        else:
            fax = fax.strip()

        website = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/table/tr[5]/td[2]/text()').get()
        if website == None:
            website = '-'
        else:
            website = website.strip()

        email = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/table/tr[6]/td[2]/text()').get()
        if email == None:
            email = '-'
        else:
            email = email.strip()
            
        last_registered_id_title = response.xpath('/html/body/div/div[4]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[6]/td[1]/text()').get()
        if last_registered_id_title == 'Last Registered ID':
            last_registered_id = response.xpath('/html/body/div/div[4]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[6]/td[2]/text()').get().strip()
        else:
            last_registered_id = response.xpath('/html/body/div/div[4]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[2]/text()').get().strip()

        fiscal_year_title = response.xpath('/html/body/div/div[4]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[1]/text()').get()
        if fiscal_year_title == 'Fiscal Year (submitted financial statement)':
            fiscal_year = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[2]/a/text()').get().strip()
        else:
            fiscal_year = response.xpath('/html/body/div/div[4]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[8]/td[2]/a/text()').get().strip()

        item = EngSpiderItem()
        item['company_id']              = response.xpath('/html/body/div/div[4]/div[2]/div/div[2]/div[1]/div/div[1]/p/text()').get().strip()
        item['company_name']            = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[1]/h2/text()').get().strip()
        item['company_type']            = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[1]/th[2]/text()').get().strip()
        item['status']                  = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[3]/td[2]/text()').get().strip()
        item['objective']               = objective
        item['directors']               = director_list
        item['bussiness_type']          = raw_bussiness_type
        item['address']                 = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/table/tr[2]/td/text()').get().strip()   
        item['tel']                     = tel
        item['fax']                     = fax
        item['website']                 = website
        item['email']                   = email
        item['last_registered_id']      = last_registered_id
        item['fiscal_year']             = fiscal_year

        return item