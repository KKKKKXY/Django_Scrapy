# import all profile crawlers
from .spiders.dbdcrawler_Eng1 import DbdcrawlerSpider1
from .spiders.dbdcrawler_Eng2 import DbdcrawlerSpider2
from .spiders.dbdcrawler_Eng3 import DbdcrawlerSpider3
from .spiders.dbdcrawler_Eng4 import DbdcrawlerSpider4
from .spiders.dbdcrawler_Eng5 import DbdcrawlerSpider5
# import all financial crawlers
from finan_posit_app.finan_posit_spider.finan_posit_spider.spiders.dbdfinanpositcrawler import FinancialPositionCrawlerSpider
from finan_ratio_app.finan_ratio_spider.finan_ratio_spider.spiders.dbdratiocrawler import FinancialRatioCrawlerSpider
from income_state_app.income_spider.income_spider.spiders.dbdincomecrawler import IncomeStatementCrawlerSpider
# import file reader to get companies id
from backend.data_reader.excel_reader import *
from backend.data_reader.pdf_reader import *
# import needed lib
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
import logging
from django.core.files.storage import default_storage
# import own lib
# from scrapy_eng_app.models import *
# from finan_posit_app.models import *
# from finan_ratio_app.models import *
# from income_state_app.models import *


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
def run_1(selectEng):
    # get all ids from file
    cids_1=all_companies_id(selectEng)
    print('There are total: ' + str(len(cids_1)) + ' companies need to scrape')
    logging.info('There are total: ' + str(len(cids_1)) + ' companies need to scrape')
    
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            # pass cid and run profile and financial crawlers
            runner.crawl(DbdcrawlerSpider1, cid=cids_1)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_1, id_start_num=0)
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_1, id_start_num=0)
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_1, id_start_num=0)

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
def run_2(selectEng):
    # get all ids from file
    cids=all_companies_id(selectEng)
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
            # pass cid and run 1st crawlers incuding profile and financial part
            runner.crawl(DbdcrawlerSpider1, cid=cids_1)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_1, id_start_num=len(cids_2))
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_1, id_start_num=len(cids_2))
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_1, id_start_num=len(cids_2))
            # pass cid and run 2nd crawlers incuding profile and financial part
            runner.crawl(DbdcrawlerSpider2, cid=cids_2)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_2, id_start_num=0)
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_2, id_start_num=0)
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_2, id_start_num=0)

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
def run_3(selectEng):
    # get all ids from file
    cids=all_companies_id(selectEng)
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
            # pass cid and run 1st crawlers
            runner.crawl(DbdcrawlerSpider1, cid=cids_1)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_1, id_start_num=len(cids_2)+len(cids_3))
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_1, id_start_num=len(cids_2)+len(cids_3))
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_1, id_start_num=len(cids_2)+len(cids_3))
            # pass cid and run 2nd crawlers
            runner.crawl(DbdcrawlerSpider2, cid=cids_2)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_2, id_start_num=len(cids_3))
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_2, id_start_num=len(cids_3))
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_2, id_start_num=len(cids_3))
            # pass cid and run 3rd crawlers
            runner.crawl(DbdcrawlerSpider3, cid=cids_3)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_3, id_start_num=0)
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_3, id_start_num=0)
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_3, id_start_num=0)

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
def run_4(selectEng):
    # get all ids from file
    cids=all_companies_id(selectEng)
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
            # pass cid and run 1st crawlers
            runner.crawl(DbdcrawlerSpider1, cid=cids_1)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_1, id_start_num=len(cids_2)+len(cids_3)+len(cids_4))
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_1, id_start_num=len(cids_2)+len(cids_3)+len(cids_4))
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_1, id_start_num=len(cids_2)+len(cids_3)+len(cids_4))
            # pass cid and run 2nd crawlers
            runner.crawl(DbdcrawlerSpider2, cid=cids_2)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_2, id_start_num=len(cids_3)+len(cids_4))
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_2, id_start_num=len(cids_3)+len(cids_4))
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_2, id_start_num=len(cids_3)+len(cids_4))
            # pass cid and run 3rd crawlers
            runner.crawl(DbdcrawlerSpider3, cid=cids_3)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_3, id_start_num=len(cids_4))
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_3, id_start_num=len(cids_4))
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_3, id_start_num=len(cids_4))
            # pass cid and run 4th crawlers
            runner.crawl(DbdcrawlerSpider4, cid=cids_4)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_4, id_start_num=0)
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_4, id_start_num=0)
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_4, id_start_num=0)

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
def run_5(selectEng):
    # get all ids from file
    cids=all_companies_id(selectEng)
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
            # pass cid and run 1st crawlers
            runner.crawl(DbdcrawlerSpider1, cid=cids_1)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_1, id_start_num=len(cids_2)+len(cids_3)+len(cids_4)+len(cids_5))
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_1, id_start_num=len(cids_2)+len(cids_3)+len(cids_4)+len(cids_5))
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_1, id_start_num=len(cids_2)+len(cids_3)+len(cids_4)+len(cids_5))
            # pass cid and run 2nd crawlers
            runner.crawl(DbdcrawlerSpider2, cid=cids_2)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_2, id_start_num=len(cids_3)+len(cids_4)+len(cids_5))
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_2, id_start_num=len(cids_3)+len(cids_4)+len(cids_5))
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_2, id_start_num=len(cids_3)+len(cids_4)+len(cids_5))
            # pass cid and run 3rd crawlers
            runner.crawl(DbdcrawlerSpider3, cid=cids_3)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_3, id_start_num=len(cids_4)+len(cids_5))
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_3, id_start_num=len(cids_4)+len(cids_5))
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_3, id_start_num=len(cids_4)+len(cids_5))
            # pass cid and run 4th crawlers
            runner.crawl(DbdcrawlerSpider4, cid=cids_4)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_4, id_start_num=len(cids_5))
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_4, id_start_num=len(cids_5))
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_4, id_start_num=len(cids_5))
            # pass cid and run 5th crawlers
            runner.crawl(DbdcrawlerSpider5, cid=cids_5)
            runner.crawl(FinancialPositionCrawlerSpider, cid=cids_5, id_start_num=0)
            runner.crawl(FinancialRatioCrawlerSpider, cid=cids_5, id_start_num=0)
            runner.crawl(IncomeStatementCrawlerSpider, cid=cids_5, id_start_num=0)
   
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




    # cids=all_companies_id(selectEng)

    # result = []
    # a = []
    # count = 0
    # cidsss = []
    # for i in range(len(cids)-1,len(cids)-8,-1):
    #     cidsss.append(cids[i])

    # for id in cidsss:
    # #     count = count+1
    # #     logging.info('Check ->    ' + str(count))
    # #     # cid_qs = FinancialPosition.objects.filter(company_id=id)
    # #     # cid_qs = FinancialRatio.objects.filter(company_id=id)
    # #     # cid_qs = PRatio.objects.filter(company_id=id)
    # #     # cid_qs = LRatio.objects.filter(company_id=id)
    # #     # cid_qs = OERatio.objects.filter(company_id=id)
    # #     # cid_qs = FPPRatio.objects.filter(company_id=id)
    # #     cid_qs = IncomeStatement.objects.filter(company_id=id)
    # #     if not cid_qs.exists():
    # #         logging.info('Company not exists --> ' + id)
    # #         print('Company not exists --> ' + id)
    # #         # print(cid_qs)
    # #         a.append(id)
    # #     else:
    # #         # accounts_receive = cid_qs.values('accounts_receive').count()
    # #         # inventory = cid_qs.values('inventory').count()
    # #         # t_curr_asset = cid_qs.values('t_curr_asset').count()
    # #         # proper_plant_equip = cid_qs.values('proper_plant_equip').count()
    # #         # t_nonCurr_asset = cid_qs.values('t_nonCurr_asset').count()
    # #         # t_assets = cid_qs.values('t_assets').count()
    # #         # t_curr_liab = cid_qs.values('t_curr_liab').count()
    # #         # t_nonCurr_liab = cid_qs.values('t_nonCurr_liab').count()
    # #         # t_liab = cid_qs.values('t_liab').count()
    # #         # equity = cid_qs.values('equity').count()
    # #         # t_liab_and_equity = cid_qs.values('t_liab_and_equity').count()

    # #         # profit_r = cid_qs.values('profit_r').count()
    # #         # liquid_r = cid_qs.values('liquid_r').count()
    # #         # operat_effici_r = cid_qs.values('operat_effici_r').count()
    # #         # finan_posit_propo_r = cid_qs.values('finan_posit_propo_r').count()

    # #         # ret_on_asset = cid_qs.values('ret_on_asset').count()
    # #         # ret_on_equity = cid_qs.values('ret_on_equity').count()
    # #         # gross_profit_mar = cid_qs.values('gross_profit_mar').count()
    # #         # opera_inc_on_reve_r = cid_qs.values('opera_inc_on_reve_r').count()
    # #         # net_profit_mar = cid_qs.values('net_profit_mar').count()

    # #         # curr_r = cid_qs.values('curr_r').count()
    # #         # acco_recei_tur = cid_qs.values('acco_recei_tur').count()
    # #         # invent_tur = cid_qs.values('invent_tur').count()
    # #         # acco_pay_tur = cid_qs.values('acco_pay_tur').count()

    # #         # t_asset_tur = cid_qs.values('t_asset_tur').count()
    # #         # opera_expe_to_t_reve_r = cid_qs.values('opera_expe_to_t_reve_r').count()

    # #         # asse_to_equi_r_finan_lev = cid_qs.values('asse_to_equi_r_finan_lev').count()
    # #         # debt_to_asse_r = cid_qs.values('debt_to_asse_r').count()
    # #         # debt_to_equi_r = cid_qs.values('debt_to_equi_r').count()
    # #         # debt_to_capi_r = cid_qs.values('debt_to_capi_r').count()

    # #         reve_from_sale_serv = cid_qs.values('reve_from_sale_serv').count()
    # #         t_reve = cid_qs.values('t_reve').count()
    # #         cost_of_goods_sold = cid_qs.values('cost_of_goods_sold').count()
    # #         gross_profit = cid_qs.values('gross_profit').count()
    # #         sell_admin_expe = cid_qs.values('sell_admin_expe').count()
    # #         t_expe = cid_qs.values('t_expe').count()
    # #         intere_expe = cid_qs.values('intere_expe').count()
    # #         profit_before_income_tax = cid_qs.values('profit_before_income_tax').count()
    # #         income_tax_expe = cid_qs.values('income_tax_expe').count()
    # #         net_profit = cid_qs.values('net_profit').count()
            
    # #         # if accounts_receive != 3 and inventory != 3 and t_curr_asset != 3 and proper_plant_equip != 3 and t_nonCurr_asset != 3 and t_assets != 3 and t_curr_liab != 3 and t_nonCurr_liab != 3 and t_liab != 3 and equity != 3 and t_liab_and_equity != 3:
    # #         # if profit_r != 1 and liquid_r != 1 and operat_effici_r != 1 and finan_posit_propo_r != 1:
    # #         # if curr_r != 3 and ret_on_equity != 3 and gross_profit_mar != 3 and opera_inc_on_reve_r != 3 and net_profit_mar != 3:
    # #         # if curr_r != 3 and acco_recei_tur != 3 and invent_tur != 3 and acco_pay_tur != 3:
    # #         # if t_asset_tur != 3 and opera_expe_to_t_reve_r != 3:
    # #         # if asse_to_equi_r_finan_lev != 3 and debt_to_asse_r != 3 and debt_to_equi_r != 3 and debt_to_capi_r != 3:
    # #         if reve_from_sale_serv != 3 and t_reve != 3 and cost_of_goods_sold != 3 and gross_profit != 3 and sell_admin_expe != 3 and t_expe != 3 and intere_expe != 3 and profit_before_income_tax != 3 and income_tax_expe != 3 and net_profit != 3:
    # #             logging.info(True)
    # #             logging.info(id)
    # #             # logging.info(accounts_receive)
    # #             # logging.info(inventory)
    # #             # logging.info(t_curr_asset)
    # #             # logging.info(proper_plant_equip)
    # #             # logging.info(t_nonCurr_asset)
    # #             # logging.info(t_assets)
    # #             # logging.info(t_curr_liab)
    # #             # logging.info(t_nonCurr_liab)
    # #             # logging.info(t_liab)
    # #             # logging.info(equity)
    # #             # logging.info(t_liab_and_equity)

    # #             # logging.info(profit_r)
    # #             # logging.info(liquid_r)
    # #             # logging.info(operat_effici_r)
    # #             # logging.info(finan_posit_propo_r)

    # #             # logging.info(ret_on_asset)
    # #             # logging.info(ret_on_equity)
    # #             # logging.info(gross_profit_mar)
    # #             # logging.info(opera_inc_on_reve_r)
    # #             # logging.info(net_profit_mar)

    # #             # logging.info(curr_r)
    # #             # logging.info(acco_recei_tur)
    # #             # logging.info(invent_tur)
    # #             # logging.info(acco_pay_tur)

    # #             # logging.info(t_asset_tur)
    # #             # logging.info(opera_expe_to_t_reve_r)

    # #             # logging.info(asse_to_equi_r_finan_lev)
    # #             # logging.info(debt_to_asse_r)
    # #             # logging.info(debt_to_equi_r)
    # #             # logging.info(debt_to_capi_r)

    # #             logging.info(reve_from_sale_serv)
    # #             logging.info(t_reve)
    # #             logging.info(cost_of_goods_sold)
    # #             logging.info(gross_profit)
    # #             logging.info(sell_admin_expe)
    # #             logging.info(t_expe)
    # #             logging.info(intere_expe)
    # #             logging.info(profit_before_income_tax)
    # #             logging.info(income_tax_expe)
    # #             logging.info(net_profit)

    # #             result.append(id)

    # # print('Length of a ->    ' + str(len(a)))
    # # logging.info('Length of a ->    ' + str(len(a)))
    # # logging.info(a)
    # # logging.info('---------------------------------------')


    # # print('Length of result ->    ' + str(len(result)))
    # # logging.info('Length of result ->    ' + str(len(result)))
    # # logging.info(result)
    # # logging.info('---------------------------------------')



    # # cids=all_companies_id(selectEng)
    # cids_1 = ['0963563000788']
    # cids_2 = ['0963563000770','0963563000796']
    # cids_3 = ['0965563000461']
    # cids_4 = ['0963563000800']
    # cids_5 = ['0963563000761','0965563000453']
    

    # for i in range(490,500,1):
    #     cids_1.append(cids[i])
        # cids_2.append(cids[i+20])
        # cids_3.append(cids[i+20])
        # cids_4.append(cids[i+30])
        # cids_5.append(cids[i+40])
    # print(cids_1)
    # print()
    # print(cids_2)
    # print()
    # print(cids_3)
    # print()
    # print(cids_4)
    # print()
    # print(cids_5)
    # # qs = PositYear.objects.all().count()
    # # print(qs)

    # print(len(cids_1)+len(cids_2)+len(cids_3)+len(cids_4)+len(cids_5))