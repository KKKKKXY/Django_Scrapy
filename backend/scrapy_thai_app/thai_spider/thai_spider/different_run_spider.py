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
        print('def f(q):')
        try:
            runner = crawler.CrawlerRunner()
            runner.crawl(DbdcrawlerSpider1, cid=random_company(selectThai))
            runner.crawl(DbdcrawlerSpider2, cid=random_company(selectThai))
            deferred = runner.join()
            # deferred = runner.crawl(spider, cid=random_company(selectThai))
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
            print('q.put(None)')
        except Exception as e:
            q.put(e)
            print('q.put(e)')

    q = Queue()
    print('q = Queue()')
    p = Process(target=f, args=(q,))
    print('p = Process(target=f, args=(q,))')
    p.start()
    print('p.start()')
    result = q.get()
    print('result = q.get()')
    p.join()
    print('p.join()')
    
    if result is not None:
        print('if result is not None:')
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
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            runner.crawl(DbdcrawlerSpider1, cid=random_company(selectThai))
            runner.crawl(DbdcrawlerSpider2, cid=random_company(selectThai))
            runner.crawl(DbdcrawlerSpider3, cid=random_company(selectThai))
            runner.crawl(DbdcrawlerSpider4, cid=random_company(selectThai))
            runner.crawl(DbdcrawlerSpider5, cid=random_company(selectThai))
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