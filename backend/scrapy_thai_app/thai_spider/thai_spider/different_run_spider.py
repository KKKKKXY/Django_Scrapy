from .spiders.dbdcrawler_Thai1 import DbdcrawlerSpider1
from .spiders.dbdcrawler_Thai2 import DbdcrawlerSpider2
from .spiders.dbdcrawler_Thai3 import DbdcrawlerSpider3
from .spiders.dbdcrawler_Thai4 import DbdcrawlerSpider4
from .spiders.dbdcrawler_Thai5 import DbdcrawlerSpider5
from backend.data_reader.excel_reader import *
from backend.data_reader.pdf_reader import *

import scrapy.crawler as crawler
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.project import get_project_settings
# from crochet import setup
from multiprocessing import Process, Queue
from twisted.internet import reactor
import logging
from scrapy_thai_app.profile_models import DBDCompany_Thai

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
    # print(companies_id)
    return companies_id

# the wrapper to make it run more times
def run_1(selectThai):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            runner.crawl(DbdcrawlerSpider1, cid=random_company(selectThai))
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

def run_2(selectThai):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            runner.crawl(DbdcrawlerSpider1, cid=random_company(selectThai))
            runner.crawl(DbdcrawlerSpider2, cid=random_company(selectThai))
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

def run_3(selectThai):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            runner.crawl(DbdcrawlerSpider1, cid=random_company(selectThai))
            runner.crawl(DbdcrawlerSpider2, cid=random_company(selectThai))
            runner.crawl(DbdcrawlerSpider3, cid=random_company(selectThai))
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

def run_4(selectThai):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            runner.crawl(DbdcrawlerSpider1, cid=random_company(selectThai))
            runner.crawl(DbdcrawlerSpider2, cid=random_company(selectThai))
            runner.crawl(DbdcrawlerSpider3, cid=random_company(selectThai))
            runner.crawl(DbdcrawlerSpider4, cid=random_company(selectThai))
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

def run_5(selectThai):
    # https://datawarehouse.dbd.go.th/company/profile/2/0102563000172
    # cids=random_company(selectThai)
    # cidsss = []
    # for i in range(3000,len(cids),1):
    #     cidsss.append(cids[i])

    # print(len(cidsss))
    # qs = DBDCompany_Thai.objects.values('company_id')
    # result = []
    # count = 0

    # for id in cidsss:
    #     count = count+1
    #     logging.info('filter ->    ' + str(count))
    #     cid_qs = DBDCompany_Thai.objects.filter(company_id=id)
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



    # cids=random_company(selectThai)
    cids_1 = ['0115563023841']
    cids_2 = ['0123563004705']
    cids_3 = ['0253563001063']
    # cids_4 = []
    # cids_5 = []
    # for i in range(0,1493,1):
    #     cids_1.append(cids[i])
    #     cids_2.append(cids[i+1493])
    #     cids_3.append(cids[i+2896])
        # cids_4.append(cids[i])
        # cids_5.append(cids[i])
    # print(cids_1)
    # print()
    # print(cids_2)
    # print()
    # print(cids_3)
    # print()
    # print(cids_4)
    # print()
    # print(cids_5)
#     # ---------------------------------------

    # print(len(cids_1)+len(cids_2)+len(cids_3)+len(cids_4)+len(cids_5))

    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            # cid=random_company(selectThai)
            # runner.crawl(DbdcrawlerSpider1, cid=random_company(selectThai))
            # runner.crawl(DbdcrawlerSpider2, cid=random_company(selectThai))
            # runner.crawl(DbdcrawlerSpider3, cid=random_company(selectThai))
            # runner.crawl(DbdcrawlerSpider4, cid=random_company(selectThai))
            # runner.crawl(DbdcrawlerSpider5, cid=random_company(selectThai))
            runner.crawl(DbdcrawlerSpider1, cid=cids_1)
            runner.crawl(DbdcrawlerSpider2, cid=cids_2)
            runner.crawl(DbdcrawlerSpider3, cid=cids_3)
            # runner.crawl(DbdcrawlerSpider4, cid=cids_4)
            # runner.crawl(DbdcrawlerSpider5, cid=cids_5)
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