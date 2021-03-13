# Define your item pipelines here
from itemadapter import ItemAdapter
import logging
from income_state_app.models import *

class IncomeSpiderPipeline:
    def close_spider(self, spider):
        cids_qs = IncomeYearDetail.objects.values('company_id').distinct()
        for i in range(cids_qs.count()):
            cid = cids_qs[i]['company_id']
            year_qs = IncomeYearDetail.objects.filter(company_id=cid)
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

            company_qs = IncomeStat.objects.filter(company_id=cid)
            print('Assign year detail value to each attribute =====================================')
            if company_qs.exists() and company_qs.count() == 1:
                print('the company ALREADY exist.')
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
                print('the company NOT exist.')
                fp = IncomeStat.objects.create(company_id=cid)
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

    def process_item(self, item, spider):        
        year = IncomeYearDetail()
        year.company_id     = item['company_id']
        year.year           = item['year']
        year.amount         = item['amount']
        year.change         = item['change']
        year.save()
        print('Store income year details finished -----------------------------------------------------')
        return item