from .spiders.dbdcrawler_Eng1 import DbdcrawlerSpider1
from .spiders.dbdcrawler_Eng2 import DbdcrawlerSpider2
from .spiders.dbdcrawler_Eng3 import DbdcrawlerSpider3
from .spiders.dbdcrawler_Eng4 import DbdcrawlerSpider4
from .spiders.dbdcrawler_Eng5 import DbdcrawlerSpider5
from backend.data_reader.excel_reader import *
from backend.data_reader.pdf_reader import *

import scrapy.crawler as crawler
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.project import get_project_settings
# from crochet import setup
from multiprocessing import Process, Queue
from twisted.internet import reactor

from scrapy_eng_app.models import DBDCompany_Eng
import logging

from finan_posit_app.finan_posit_spider.finan_posit_spider.spiders.dbdfinanpositcrawler import FinancialPositionCrawlerSpider
from finan_ratio_app.finan_ratio_spider.finan_ratio_spider.spiders.dbdratiocrawler import FinancialRatioCrawlerSpider
from income_state_app.income_spider.income_spider.spiders.dbdincomecrawler import IncomeStatementCrawlerSpider

# backend/finan_posit_app/finan_posit_spider/finan_posit_spider/spiders/dbdfinanpositcrawler.py
# backend/finan_ratio_app/finan_ratio_spider/finan_ratio_spider/spiders/dbdratiocrawler.py
# backend/income_state_app/income_spider/income_spider/spiders/dbdincomecrawler.py


# Select random companies to scrape
def random_company(file_name):
    file_type = file_name.rpartition('.')[-1]
    print('file_type is: '+ file_type)
    # excel_path
    if file_type == 'xlsx' or file_type == 'csv':
        excel_path = '/backend/media/xlsx/'+file_name
        print(excel_path)
        companies_id = get_cid_from_excel(excel_path)
    # pdf_path
    elif file_type == 'pdf':
        pdf_path = '/backend/media/pdf/'+file_name
        print(pdf_path)
        pdf_to_excel_path = '/backend/media/pdf_convert_excel/dbd_from_pdf_thai.xlsx'
        # convert_pdf_to_excel(pdf_path, pdf_to_excel_path)
        companies_id = get_cid_from_pdf(pdf_to_excel_path)
    else:
        print('Invaid')
    return companies_id

# the wrapper to make it run more times
def run_1(selectEng):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            runner.crawl(DbdcrawlerSpider1, cid=random_company(selectEng))
            deferred = runner.join()
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()
    if result is not None:
        raise result

def run_2(selectEng):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            runner.crawl(DbdcrawlerSpider1, cid=random_company(selectEng))
            runner.crawl(DbdcrawlerSpider2, cid=random_company(selectEng))
            deferred = runner.join()
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()
    if result is not None:
        raise result

def run_3(selectEng):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            runner.crawl(DbdcrawlerSpider1, cid=random_company(selectEng))
            runner.crawl(DbdcrawlerSpider2, cid=random_company(selectEng))
            runner.crawl(DbdcrawlerSpider3, cid=random_company(selectEng))
            deferred = runner.join()
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()
    if result is not None:
        raise result

def run_4(selectEng):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            runner.crawl(DbdcrawlerSpider1, cid=random_company(selectEng))
            runner.crawl(DbdcrawlerSpider2, cid=random_company(selectEng))
            runner.crawl(DbdcrawlerSpider3, cid=random_company(selectEng))
            runner.crawl(DbdcrawlerSpider4, cid=random_company(selectEng))
            deferred = runner.join()
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()
    if result is not None:
        raise result

def run_5(selectEng):
    # cids=random_company(selectEng)
    # cidsss = []
    # for i in range(3000,len(cids),1):
    #     cidsss.append(cids[i])

    # print(len(cidsss))
    # qs = DBDCompany_Eng.objects.values('company_id')
    # result = []
    # count = 0

    # for id in cidsss:
    #     count = count+1
    #     logging.info('filter ->    ' + str(count))
    #     cid_qs = DBDCompany_Eng.objects.filter(company_id=id)
    #     if not cid_qs.exists():
    #         logging.info(True)
    #         logging.info(id)
    #         print('True:    ' + id)
    #         # print(cid_qs)
    #         result.append(id)

    # # ---------------------------------------

    # print('Length of result ->    ' + str(len(result)))
    # logging.info('Length of result ->    ' + str(len(result)))
    # # print('---------------------------------------')
    # logging.info('---------------------------------------')
    # # print(result)
    # logging.info(result)


    cids=random_company(selectEng)
    cids_1 = []
    cids_2 = []
    cids_3 = []
    cids_4 = []
    cids_5 = []
    # for i in range(0,1493,1):
    #     cids_1.append(cids[i])
    #     cids_2.append(cids[i+1493])
    #     cids_3.append(cids[i+2896])
    for i in range(100,500,1):
        cids_1.append(cids[i])
        # cids_2.append(cids[i+2])
        # cids_3.append(cids[i+4])
        # cids_4.append(cids[i+6])
        # cids_5.append(cids[i+8])
    # print(cids_1)
    print(len(cids_1))
    # print()
    # print(cids_2)
    # print()
    # print(cids_3)
    # print()
    # print(cids_4)
    # print()
    # print(cids_5)



    # print(len(cids_1)+len(cids_2)+len(cids_3)+len(cids_4)+len(cids_5))

    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            # runner.crawl(DbdcrawlerSpider1, cid=cids_1)
            # runner.crawl(DbdcrawlerSpider2, cid=cids_2)
            # runner.crawl(DbdcrawlerSpider3, cid=cids_3)
            # runner.crawl(DbdcrawlerSpider4, cid=cids_4)
            # runner.crawl(DbdcrawlerSpider5, cid=cids_5)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_1)
            # runner.crawl(FinancialRatioCrawlerSpider, cid=cids_1)
            # runner.crawl(IncomeStatementCrawlerSpider, cid=cids_1)

            # runner.crawl(FinancialPositionCrawlerSpider, cid=cids_2)
            # runner.crawl(FinancialRatioCrawlerSpider, cid=cids_2)
            # runner.crawl(IncomeStatementCrawlerSpider, cid=cids_2)

            # runner.crawl(FinancialPositionCrawlerSpider, cid=cids_3)
            # runner.crawl(FinancialRatioCrawlerSpider, cid=cids_3)
            # runner.crawl(IncomeStatementCrawlerSpider, cid=cids_3)

            # runner.crawl(FinancialPositionCrawlerSpider, cid=cids_4)
            # runner.crawl(FinancialRatioCrawlerSpider, cid=cids_4)
            # runner.crawl(IncomeStatementCrawlerSpider, cid=cids_4)

            # runner.crawl(FinancialPositionCrawlerSpider, cid=cids_5)
            # runner.crawl(FinancialRatioCrawlerSpider, cid=cids_5)
            # runner.crawl(IncomeStatementCrawlerSpider, cid=cids_5)
            deferred = runner.join()
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()
    if result is not None:
        raise result