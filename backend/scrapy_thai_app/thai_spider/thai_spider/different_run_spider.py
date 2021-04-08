# import all profile crawlers
from .spiders.dbdcrawler_Thai1 import DbdcrawlerSpider1
from .spiders.dbdcrawler_Thai2 import DbdcrawlerSpider2
from .spiders.dbdcrawler_Thai3 import DbdcrawlerSpider3
from .spiders.dbdcrawler_Thai4 import DbdcrawlerSpider4
from .spiders.dbdcrawler_Thai5 import DbdcrawlerSpider5
# import file reader to get companies id
from backend.data_reader.excel_reader import *
from backend.data_reader.pdf_reader import *
# import needed lib
import scrapy.crawler as crawler
from django.core.files.storage import default_storage
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.project import get_project_settings
# from crochet import setup
from multiprocessing import Process, Queue
from twisted.internet import reactor
import logging
# import own lib
# from scrapy_thai_app.models import *


# select all companies' id from file
def all_companies_id(file_name):
    file_type = file_name.rpartition('.')[-1]
    print('file_type is: '+ file_type)
    companies_id = []
    # excel_path
    if file_type == 'xlsx' or file_type == 'csv':
        excel_path = '/backend/media/xlsx/'+file_name
        companies_id = get_cid_from_excel(excel_path)
    # pdf_path
    elif file_type == 'pdf':
        pdf_path = '/backend/media/pdf/'+file_name
        pdf_name = file_name.rpartition('.')[0]
        pdf_to_excel_path = '/backend/media/pdf_to_excel/'+pdf_name+'.xlsx'
        check_pdf_1 = default_storage.exists(pdf_path)
        check_pdf_2 = default_storage.exists(pdf_to_excel_path)
        if check_pdf_1==True:
            if check_pdf_2==False:
                convert_pdf_to_excel(pdf_path, pdf_to_excel_path)
            companies_id = get_cid_from_pdf(pdf_to_excel_path)
        else:
            logging.error('No such file in database: ' + file_name)
    elif len(companies_id)==0:
        logging.error('No companies id find from file: ' + file_name) 
    else:
        logging.error('No such file in database: ' + file_name)
    
    return companies_id

# the wrapper to make it run more times
# open one browser
def run_1(selectThai):
    # get all ids from file
    cids_1=all_companies_id(selectThai)
    print('There are total: ' + str(len(cids_1)) + ' companies need to scrape')
    logging.info('There are total: ' + str(len(cids_1)) + ' companies need to scrape')

    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            # pass cid and run profile crawlers
            runner.crawl(DbdcrawlerSpider1, cid=cids_1)

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

# open two browsers
def run_2(selectThai):
    # get all ids from file
    cids=all_companies_id(selectThai)
    cids_1 = []
    cids_2 = []
    print('There are total: ' + str(len(cids)) + ' companies need to scrape')
    logging.info('There are total: ' + str(len(cids)) + ' companies need to scrape')

    # get the minimum amount of id for each browser
    until_num = len(cids) // 2
    print('Each browser need to scrape: ' + str(until_num) + ' companies')
    logging.info('Each browser need to scrape: ' + str(until_num) + ' companies')

    # get the extra amount of id append to last browser
    modulus_num = len(cids) % 2
    print('The last browser need to scrape more ' + str(modulus_num) + ' companies')
    logging.info('The last browser need to scrape more ' + str(modulus_num) + ' companies')

    # let all ids separate into lists
    for i in range(0,until_num,1):
        cids_1.append(cids[i])
        cids_2.append(cids[i+until_num])
    # append the extra amount of id to last browser
    for i in range(modulus_num,0,-1):
        cids_2.append(cids[len(cids)-i])

    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            # pass cid and run 1st profile crawlers
            runner.crawl(DbdcrawlerSpider1, cid=cids_1)
            # pass cid and run 2nd profile crawlers
            runner.crawl(DbdcrawlerSpider2, cid=cids_2)

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

# open three browsers
def run_3(selectThai):
    # get all ids from file
    cids=all_companies_id(selectThai)
    cids_1 = []
    cids_2 = []
    cids_3 = []
    print('There are total: ' + str(len(cids)) + ' companies need to scrape')
    logging.info('There are total: ' + str(len(cids)) + ' companies need to scrape')

    # get the minimum amount of id for each browser
    until_num = len(cids) // 3
    print('Each browser need to scrape: ' + str(until_num) + ' companies')
    logging.info('Each browser need to scrape: ' + str(until_num) + ' companies')

    # get the extra amount of id append to last browser
    modulus_num = len(cids) % 3
    print('The last browser need to scrape more ' + str(modulus_num) + ' companies')
    logging.info('The last browser need to scrape more ' + str(modulus_num) + ' companies')

    # let all ids separate into lists
    for i in range(0,until_num,1):
        cids_1.append(cids[i])
        cids_2.append(cids[i+until_num])
        cids_3.append(cids[i+until_num*2])
    # append the extra amount of id to last browser
    for i in range(modulus_num,0,-1):
        cids_3.append(cids[len(cids)-i])

    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            # pass cid and run 1st profile crawlers
            runner.crawl(DbdcrawlerSpider1, cid=cids_1)
            # pass cid and run 2nd profile crawlers
            runner.crawl(DbdcrawlerSpider2, cid=cids_2)
            # pass cid and run 3rd profile crawlers
            runner.crawl(DbdcrawlerSpider3, cid=cids_3)

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

# open four browsers
def run_4(selectThai):
    # get all ids from file
    cids=all_companies_id(selectThai)
    cids_1 = []
    cids_2 = []
    cids_3 = []
    cids_4 = []
    print('There are total: ' + str(len(cids)) + ' companies need to scrape')
    logging.info('There are total: ' + str(len(cids)) + ' companies need to scrape')

    # get the minimum amount of id for each browser
    until_num = len(cids) // 4
    print('Each browser need to scrape: ' + str(until_num) + ' companies')
    logging.info('Each browser need to scrape: ' + str(until_num) + ' companies')

    # get the extra amount of id append to last browser
    modulus_num = len(cids) % 4
    print('The last browser need to scrape more ' + str(modulus_num) + ' companies')
    logging.info('The last browser need to scrape more ' + str(modulus_num) + ' companies')

    # let all ids separate into lists
    for i in range(0,until_num,1):
        cids_1.append(cids[i])
        cids_2.append(cids[i+until_num])
        cids_3.append(cids[i+until_num*2])
        cids_4.append(cids[i+until_num*3])
    # append the extra amount of id to last browser
    for i in range(modulus_num,0,-1):
        cids_4.append(cids[len(cids)-i])

    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            # pass cid and run 1st profile crawlers
            runner.crawl(DbdcrawlerSpider1, cid=cids_1)
            # pass cid and run 2nd profile crawlers
            runner.crawl(DbdcrawlerSpider2, cid=cids_2)
            # pass cid and run 3rd profile crawlers
            runner.crawl(DbdcrawlerSpider3, cid=cids_3)
            # pass cid and run 4th profile crawlers
            runner.crawl(DbdcrawlerSpider4, cid=cids_4)

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

# open five browsers
def run_5(selectThai):
    # https://datawarehouse.dbd.go.th/company/profile/2/0102563000172
    # get all ids from file
    cids=all_companies_id(selectThai)
    cids_1 = []
    cids_2 = []
    cids_3 = []
    cids_4 = []
    cids_5 = []
    print('There are total: ' + str(len(cids)) + ' companies need to scrape')
    logging.info('There are total: ' + str(len(cids)) + ' companies need to scrape')

    # get the minimum amount of id for each browser
    until_num = len(cids) // 5
    print('Each browser need to scrape: ' + str(until_num) + ' companies')
    logging.info('Each browser need to scrape: ' + str(until_num) + ' companies')

    # get the extra amount of id append to last browser
    modulus_num = len(cids) % 5
    print('The last browser need to scrape more ' + str(modulus_num) + ' companies')
    logging.info('The last browser need to scrape more ' + str(modulus_num) + ' companies')

    # let all ids separate into lists
    for i in range(0,until_num,1):
        cids_1.append(cids[i])
        cids_2.append(cids[i+until_num])
        cids_3.append(cids[i+until_num*2])
        cids_4.append(cids[i+until_num*3])
        cids_5.append(cids[i+until_num*4])
    # append the extra amount of id to last browser
    for i in range(modulus_num,0,-1):
        cids_5.append(cids[len(cids)-i])

    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            # pass cid and run 1st profile crawlers
            runner.crawl(DbdcrawlerSpider1, cid=cids_1)
            # pass cid and run 2nd profile crawlers
            runner.crawl(DbdcrawlerSpider2, cid=cids_2)
            # pass cid and run 3rd profile crawlers
            runner.crawl(DbdcrawlerSpider3, cid=cids_3)
            # pass cid and run 4th profile crawlers
            runner.crawl(DbdcrawlerSpider4, cid=cids_4)
            # pass cid and run 5th profile crawlers
            runner.crawl(DbdcrawlerSpider5, cid=cids_5)

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
