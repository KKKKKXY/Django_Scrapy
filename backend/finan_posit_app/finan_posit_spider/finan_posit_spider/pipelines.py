from itemadapter import ItemAdapter
import logging
from finan_posit_app.models import *

class FinanPositSpiderPipeline:
    def close_spider(self, spider):
        logging.critical('Store financial year details finished -----------------------------------------------------')
        
        # print()
        # print(spider.cid)
        # print('len(spider.cid): ' + str(len(spider.cid)))
        # print(spider.id_start_num)
        # request_page_num = len(spider.cid) + spider.id_start_num + 1
        # print('request_page_num: ' + str(request_page_num))
        # # get all companies' id from posit_year_detail table in database
        # cids_qs = PositYear.objects.values('company_id').distinct()
        # print('financial year COUNT is: ' + str(cids_qs.count()))


        # get the number of request pages
        request_page_num = len(spider.cid) + spider.id_start_num + 1
        # get all companies' id from posit_year_detail table in database
        cids_qs = PositYear.objects.values('company_id').distinct()
        print('financial year COUNT is: ' + str(cids_qs.count()))

        try:
            # assign years detail into each year list
            for i in range(cids_qs.count()-1-spider.id_start_num, cids_qs.count()-request_page_num, -1):
                cid = cids_qs[i]['company_id']
                year_qs = PositYear.objects.filter(company_id=cid)
                ar_years = []
                i_years = []
                tca_years = []
                ppe_years = []
                tna_years = []
                ta_years = []
                tcl_years = []
                tnl_years = []
                tl_years = []
                e_years = []
                tlae_years = []
                for x in range(0, year_qs.count(), 11):
                    logging.info('Assign All Position Details for year ------> ' + year_qs[x].year)
                    ar_years.append(year_qs[x])
                    i_years.append(year_qs[x+1])
                    tca_years.append(year_qs[x+2])
                    ppe_years.append(year_qs[x+3])
                    tna_years.append(year_qs[x+4])
                    ta_years.append(year_qs[x+5])
                    tcl_years.append(year_qs[x+6])
                    tnl_years.append(year_qs[x+7])
                    tl_years.append(year_qs[x+8])
                    e_years.append(year_qs[x+9])
                    tlae_years.append(year_qs[x+10])

                # check whether the company already exist in database
                company_qs = FinancialPosition.objects.filter(company_id=cid)
                if company_qs.exists() and company_qs.count() == 1:
                    # if exists, update year detail to the company
                    logging.info('Store financial position info for company: ' + company_qs.first().company_id)
                    fp = company_qs.first()
                    fp.accounts_receive.set(ar_years)
                    fp.inventory.set(i_years)
                    fp.t_curr_asset.set(tca_years)
                    fp.proper_plant_equip.set(ppe_years)
                    fp.t_nonCurr_asset.set(tna_years)
                    fp.t_assets.set(ta_years)
                    fp.t_curr_liab.set(tcl_years)
                    fp.t_nonCurr_liab.set(tnl_years)
                    fp.t_liab.set(tl_years)
                    fp.equity.set(e_years)
                    fp.t_liab_and_equity.set(tlae_years)
                else:
                    # if not, create a new company
                    logging.info('Create new company: ' + cid)
                    fp = FinancialPosition.objects.create(company_id=cid)
                    fp.accounts_receive.set(ar_years)
                    fp.inventory.set(i_years)
                    fp.t_curr_asset.set(tca_years)
                    fp.proper_plant_equip.set(ppe_years)
                    fp.t_nonCurr_asset.set(tna_years)
                    fp.t_assets.set(ta_years)
                    fp.t_curr_liab.set(tcl_years)
                    fp.t_nonCurr_liab.set(tnl_years)
                    fp.t_liab.set(tl_years)
                    fp.equity.set(e_years)
                    fp.t_liab_and_equity.set(tlae_years)
                    
            print('Store company financial position info finished ========----------------------=======')
            logging.critical('Store company financial position info finished ========----------------------=======')
            print()
        except Exception as e:
            print('Store financial position info error')
            print(e)
            logging.warning('Store financial position info error')
            logging.error(e)

    def process_item(self, item, spider):
        # store financial position year details into posit_year_detail table in database
        year = PositYear()
        year.company_id     = item['company_id']
        year.year           = item['year']
        year.amount         = item['amount']
        year.change         = item['change']
        year.save()
        return item