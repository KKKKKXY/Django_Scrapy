import os, time, re, pickle, signal
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import scrapy
import json
from thai_spider.items import ThaiSpiderItem
from scrapy.spiders import CrawlSpider #, Rule

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('.'))))
from data_reader.excel_reader import *
from data_reader.pdf_reader import *

class DbdcrawlerSpider1(CrawlSpider):
    name = 'dbdcrawler_Thai1'
# ['0215563008523', '0735563007409', '0105563148288', '0133563004471', '0105563144444', '0105563152269', '0115563022152', '0205563032742', '0105563146757', '0105563153044']
# ['0135563023183', '0215563008451', '0515563001241', '0105563145441', '0105563156281', '0193563001811', '0145563003999', '0105563148873', '0105563161578', '0145563003930']
# ['0105563152188', '0205563032394', '0105563153044', '0105563157511', '0205563031428', '0343563003219', '0965563000411', '0105563152731', '0203563004275', '0105563158534']
# ['0343563003278', '0133563005043', '0503563006658', '0135563023183', '0575563003359', '0105563150045', '0815563001434', '0303563005394', '0805563003020', '0105563154431']
# ['0105563148393', '0105563147745', '0105563155039', '0245563003262', '0105563144703', '0133563004934', '0105563160148', '0145563003948', '0105563156434', '0205563031738']

    # def __init__(self, *args, **kwargs):
    #     # We are going to pass these args from our django view.
    #     # To make everything dynamic, we need to override them inside __init__ method
    #     self.url = kwargs.get('url')
    #     self.domain = kwargs.get('domain')
    #     self.start_urls = [self.url]
    #     self.allowed_domains = [self.domain]

    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    allowed_domains = ["datawarehouse.dbd.go.th"]

    def start_requests(self):
        companies_id = self.random_company()
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

    # def writeJsonFile(self, data):
    #     filePath = '/backend/temp/thaiVersion.json'
    #     a_file = open(filePath, "w", encoding='utf-8')
    #     line = json.dumps(data, ensure_ascii=False) + "\n"
    #     a_file.write(line)

    # def readLoadsFile(self):
    #     loadsfilePath = '/backend/temp/thaiVersion.json'
    #     print('------------Target Company Information------------')
    #     loadsdata = json.load(open(loadsfilePath))
    #     print(loadsdata)
    #     # print(loadsdata[0]['company_name'])
    #     return loadsdata

    def random_company(self):
        # excel_path = '/backend/data_files/dbd_oct2020.xlsx'
        # companies_id = get_cid_from_excel(excel_path)
        pdf_path = '/backend/data_files/dbd_oct2020.pdf'
        pdf_to_excel_path = '/backend/scrapy_thai_app/thai_spider/thai_spider/spiders/db/dbd_from_pdf_thai.xlsx'
        convert_pdf_to_excel(pdf_path, pdf_to_excel_path)
        companies_id = get_cid_from_pdf(pdf_to_excel_path)
        print(companies_id)
        return companies_id

    def parse(self, response):
        print('------------START SCRAPING BROWSER 1------------')
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
        if raw_bussiness_type == None:
            raw_bussiness_type = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[4]/div/p/text()').get().strip()
        else:
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

        last_registered_id_title = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[6]/td[1]/text()').get()
        if last_registered_id_title == 'เลขทะเบียนเดิม':
            last_registered_id = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[6]/td[2]/text()').get().strip()
        else:
            last_registered_id = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[8]/td[2]/text()').get().strip()

        fiscal_year_title = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[1]/text()').get()
        if fiscal_year_title == 'ปีที่ส่งงบการเงิน':
            fiscal_year = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[2]/text()').get().strip()
        else:
            fiscal_year = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[9]/td[2]/text()').get().strip()

        item = ThaiSpiderItem()
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

        # print('------------Target Target Target------------')
        # self.writeJsonFile(data)
        # # item = self.readLoadsFile()
        # print(item)
        return item

class DbdcrawlerSpider2(CrawlSpider):
    name = 'dbdcrawler_Thai2'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    allowed_domains = ["datawarehouse.dbd.go.th"]

    def start_requests(self):
        companies_id = self.random_company()
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

    def random_company(self):
        # excel_path = '/backend/data_files/dbd_oct2020.xlsx'
        # companies_id = get_cid_from_excel(excel_path)
        pdf_to_excel_path = '/backend/scrapy_thai_app/thai_spider/thai_spider/spiders/db/dbd_from_pdf_thai.xlsx'
        companies_id = get_cid_from_pdf(pdf_to_excel_path)
        print(companies_id)
        return companies_id

    def parse(self, response):
        print('------------START SCRAPING BROWSER 2------------')
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
        if raw_bussiness_type == None:
            raw_bussiness_type = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[4]/div/p/text()').get().strip()
        else:
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
            
        last_registered_id_title = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[6]/td[1]/text()').get()
        if last_registered_id_title == 'เลขทะเบียนเดิม':
            last_registered_id = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[6]/td[2]/text()').get().strip()
        else:
            last_registered_id = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[8]/td[2]/text()').get().strip()

        fiscal_year_title = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[1]/text()').get()
        if fiscal_year_title == 'ปีที่ส่งงบการเงิน':
            fiscal_year = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[2]/text()').get().strip()
        else:
            fiscal_year = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[9]/td[2]/text()').get().strip()

        item = ThaiSpiderItem()
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

class DbdcrawlerSpider3(CrawlSpider):
    name = 'dbdcrawler_Thai3'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    allowed_domains = ["datawarehouse.dbd.go.th"]

    def start_requests(self):
        companies_id = self.random_company()
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

    def random_company(self):
        # excel_path = '/backend/data_files/dbd_oct2020.xlsx'
        # companies_id = get_cid_from_excel(excel_path)
        pdf_to_excel_path = '/backend/scrapy_thai_app/thai_spider/thai_spider/spiders/db/dbd_from_pdf_thai.xlsx'
        companies_id = get_cid_from_pdf(pdf_to_excel_path)
        print(companies_id)
        return companies_id

    def parse(self, response):
        print('------------START SCRAPING BROWSER 3------------')
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
        if raw_bussiness_type == None:
            raw_bussiness_type = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[4]/div/p/text()').get().strip()
        else:
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
            
        last_registered_id_title = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[6]/td[1]/text()').get()
        if last_registered_id_title == 'เลขทะเบียนเดิม':
            last_registered_id = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[6]/td[2]/text()').get().strip()
        else:
            last_registered_id = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[8]/td[2]/text()').get().strip()

        fiscal_year_title = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[1]/text()').get()
        if fiscal_year_title == 'ปีที่ส่งงบการเงิน':
            fiscal_year = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[2]/text()').get().strip()
        else:
            fiscal_year = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[9]/td[2]/text()').get().strip()

        item = ThaiSpiderItem()
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

class DbdcrawlerSpider4(CrawlSpider):
    name = 'dbdcrawler_Thai4'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    allowed_domains = ["datawarehouse.dbd.go.th"]

    def start_requests(self):
        companies_id = self.random_company()
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

    def random_company(self):
        # excel_path = '/backend/data_files/dbd_oct2020.xlsx'
        # companies_id = get_cid_from_excel(excel_path)
        pdf_to_excel_path = '/backend/scrapy_thai_app/thai_spider/thai_spider/spiders/db/dbd_from_pdf_thai.xlsx'
        companies_id = get_cid_from_pdf(pdf_to_excel_path)
        print(companies_id)
        return companies_id

    def parse(self, response):
        print('------------START SCRAPING BROWSER 4------------')
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
        if raw_bussiness_type == None:
            raw_bussiness_type = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[4]/div/p/text()').get().strip()
        else:
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
            
        last_registered_id_title = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[6]/td[1]/text()').get()
        if last_registered_id_title == 'เลขทะเบียนเดิม':
            last_registered_id = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[6]/td[2]/text()').get().strip()
        else:
            last_registered_id = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[8]/td[2]/text()').get().strip()

        fiscal_year_title = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[1]/text()').get()
        if fiscal_year_title == 'ปีที่ส่งงบการเงิน':
            fiscal_year = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[2]/text()').get().strip()
        else:
            fiscal_year = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[9]/td[2]/text()').get().strip()

        item = ThaiSpiderItem()
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

class DbdcrawlerSpider5(CrawlSpider):
    name = 'dbdcrawler_Thai5'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    allowed_domains = ["datawarehouse.dbd.go.th"]

    def start_requests(self):
        companies_id = self.random_company()
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

    def random_company(self):
        # excel_path = '/backend/data_files/dbd_oct2020.xlsx'
        # companies_id = get_cid_from_excel(excel_path)
        pdf_to_excel_path = '/backend/scrapy_thai_app/thai_spider/thai_spider/spiders/db/dbd_from_pdf_thai.xlsx'
        companies_id = get_cid_from_pdf(pdf_to_excel_path)
        print(companies_id)
        return companies_id

    def parse(self, response):
        print('------------START SCRAPING BROWSER 5------------')
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
        if raw_bussiness_type == None:
            raw_bussiness_type = response.xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[4]/div/p/text()').get().strip()
        else:
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
            
        last_registered_id_title = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[6]/td[1]/text()').get()
        if last_registered_id_title == 'เลขทะเบียนเดิม':
            last_registered_id = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[6]/td[2]/text()').get().strip()
        else:
            last_registered_id = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[8]/td[2]/text()').get().strip()

        fiscal_year_title = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[1]/text()').get()
        if fiscal_year_title == 'ปีที่ส่งงบการเงิน':
            fiscal_year = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[7]/td[2]/text()').get().strip()
        else:
            fiscal_year = response.xpath('/html/body/div/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/table/tr[9]/td[2]/text()').get().strip()

        item = ThaiSpiderItem()
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