# Define your item pipelines here
from itemadapter import ItemAdapter
import logging
from income_state_app.models import *

class IncomeSpiderPipeline:
    def close_spider(self, spider):
        print()
        print('Store income year details finished -----------------------------------------------------')
        logging.critical('Store income year details finished -----------------------------------------------------')
        cids_qs = IncomeYear.objects.values('company_id').distinct()
        print('income year details COUNT is: ' + str(cids_qs.count()))
        try:
            # for i in range(cids_qs.count()-1,-1,-1):
            for i in range(cids_qs.count()-1, cids_qs.count()-11, -1):
                # print(cids_qs[i]['company_id'])
                cid = cids_qs[i]['company_id']
                # print(cid)
                year_qs = IncomeYear.objects.filter(company_id=cid)
                rfss_years = []
                tr_years = []
                cogs_years = []
                gp_years = []
                sae_years = []
                te_years = []
                ie_years = []
                pbit_years = []
                ite_years = []
                np_years = []
                for x in range(0, year_qs.count(), 10):
                    print('Assign All Income Details for year ------> ' + year_qs[x].year)
                    logging.info('Assign All Income Details for year ------> ' + year_qs[x].year)
                    rfss_years.append(year_qs[x])
                    tr_years.append(year_qs[x+1])
                    cogs_years.append(year_qs[x+2])
                    gp_years.append(year_qs[x+3])
                    sae_years.append(year_qs[x+4])
                    te_years.append(year_qs[x+5])
                    ie_years.append(year_qs[x+6])
                    pbit_years.append(year_qs[x+7])
                    ite_years.append(year_qs[x+8])
                    np_years.append(year_qs[x+9])

                company_qs = IncomeStatement.objects.filter(company_id=cid)
                if company_qs.exists() and company_qs.count() == 1:
                    print('Store income statement info for company: ' + company_qs.first().company_id)
                    logging.info('Store income statement info for company: ' + company_qs.first().company_id)
                    fp = company_qs.first()
                    fp.reve_from_sale_serv.set(rfss_years)
                    fp.t_reve.set(tr_years)
                    fp.cost_of_goods_sold.set(cogs_years)
                    fp.gross_profit.set(gp_years)
                    fp.sell_admin_expe.set(sae_years)
                    fp.t_expe.set(te_years)
                    fp.intere_expe.set(ie_years)
                    fp.profit_before_income_tax.set(pbit_years)
                    fp.income_tax_expe.set(ite_years)
                    fp.net_profit.set(np_years)
                else:
                    print('Create new company: ' + cid)
                    logging.info('Create new company: ' + cid)
                    fp = IncomeStatement.objects.create(company_id=cid)
                    fp.reve_from_sale_serv.set(rfss_years)
                    fp.t_reve.set(tr_years)
                    fp.cost_of_goods_sold.set(cogs_years)
                    fp.gross_profit.set(gp_years)
                    fp.sell_admin_expe.set(sae_years)
                    fp.t_expe.set(te_years)
                    fp.intere_expe.set(ie_years)
                    fp.profit_before_income_tax.set(pbit_years)
                    fp.income_tax_expe.set(ite_years)
                    fp.net_profit.set(np_years)
        except Exception as e:
            print('Store income statement info error')
            print(e)
            logging.warning('Store income statement info error')
            logging.error(e)
        print('Store company income statement info finished ========----------------------=======')
        logging.critical('Store company income statement info finished ========----------------------=======')

    def process_item(self, item, spider):        
        year = IncomeYear()
        year.company_id     = item['company_id']
        year.year           = item['year']
        year.amount         = item['amount']
        year.change         = item['change']
        year.save()
        return item