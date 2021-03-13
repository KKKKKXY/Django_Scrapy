from itemadapter import ItemAdapter
import logging
from finan_ratio_app.models import *

class FinanRatioSpiderPipeline:
    def close_spider(self, spider):
        cids_qs = RatioYearDetail.objects.values('company_id').distinct()
        for i in range(cids_qs.count()):
            cid = cids_qs[i]['company_id']
            year_qs = RatioYearDetail.objects.filter(company_id=cid)
            
            # PRDetail
            roa_years = []
            roe_years = []
            gpm_years = []
            oiorr_years = []
            npm_years = []
            # LRDetail
            cr_years = []
            art_years = []
            it_years = []
            apt_years = []
            # OERDetail
            tat_years = []
            oettrr_years = []
            # FPPRDetail
            aterfl_years = []
            dtar_years = []
            dter_years = []
            dtcr_years = []
            for x in range(0, year_qs.count(), 15):
                print('Assign All Ratio Details for year ------> ' + year_qs[x].year)
                roa_years.append(year_qs[x])
                roe_years.append(year_qs[x+1])
                gpm_years.append(year_qs[x+2])
                oiorr_years.append(year_qs[x+3])
                npm_years.append(year_qs[x+4])
                cr_years.append(year_qs[x+5])
                art_years.append(year_qs[x+6])
                it_years.append(year_qs[x+7])
                apt_years.append(year_qs[x+8])
                tat_years.append(year_qs[x+9])
                oettrr_years.append(year_qs[x+10])
                aterfl_years.append(year_qs[x+11])
                dtar_years.append(year_qs[x+12])
                dter_years.append(year_qs[x+13])
                dtcr_years.append(year_qs[x+14])

            # PRDetail
            print('<------ Assign Ratio Details for PR ------>')
            pr_detail_qs = PRDetail.objects.filter(company_id=cid)
            if pr_detail_qs.exists() and pr_detail_qs.count() == 1:
                pr_detail = pr_detail_qs.first()
                pr_detail.ret_on_asset.set(roa_years)
                pr_detail.ret_on_equity.set(roe_years)
                pr_detail.gross_profit_mar.set(gpm_years)
                pr_detail.opera_inc_on_reve_r.set(oiorr_years)
                pr_detail.net_profit_mar.set(npm_years)
            else:
                pr_detail = PRDetail.objects.create(company_id=cid)
                pr_detail.ret_on_asset.set(roa_years)
                pr_detail.ret_on_equity.set(roe_years)
                pr_detail.gross_profit_mar.set(gpm_years)
                pr_detail.opera_inc_on_reve_r.set(oiorr_years)
                pr_detail.net_profit_mar.set(npm_years)

            # # LRDetail
            print('<------ Assign Ratio Details for LR ------>')
            lr_detail_qs = LRDetail.objects.filter(company_id=cid)
            if lr_detail_qs.exists() and lr_detail_qs.count() == 1:
                lr_detail = lr_detail_qs.first()
                lr_detail.curr_r.set(cr_years)
                lr_detail.acco_recei_tur.set(art_years)
                lr_detail.invent_tur.set(it_years)
                lr_detail.acco_pay_tur.set(apt_years)
            else:
                lr_detail = LRDetail.objects.create(company_id=cid)
                lr_detail.curr_r.set(cr_years)
                lr_detail.acco_recei_tur.set(art_years)
                lr_detail.invent_tur.set(it_years)
                lr_detail.acco_pay_tur.set(apt_years)

            # # OERDetail
            print('<------ Assign Ratio Details for OER ------>')
            oer_detail_qs = OERDetail.objects.filter(company_id=cid)
            if oer_detail_qs.exists() and oer_detail_qs.count() == 1:
                oer_detail = oer_detail_qs.first()
                oer_detail.t_asset_tur.set(tat_years)
                oer_detail.opera_expe_to_t_reve_r.set(oettrr_years)
            else:
                oer_detail = OERDetail.objects.create(company_id=cid)
                oer_detail.t_asset_tur.set(tat_years)
                oer_detail.opera_expe_to_t_reve_r.set(oettrr_years)
 
            # # FPPRDetail
            print('<------ Assign Ratio Details for FPPR ------>')
            fppr_detail_qs = FPPRDetail.objects.filter(company_id=cid)
            if fppr_detail_qs.exists() and fppr_detail_qs.count() == 1:
                fppr_detail = fppr_detail_qs.first()
                fppr_detail.asse_to_equi_r_finan_lev.set(aterfl_years)
                fppr_detail.debt_to_asse_r.set(dtar_years)
                fppr_detail.debt_to_equi_r.set(dter_years)
                fppr_detail.debt_to_capi_r.set(dtcr_years)
            else:
                fppr_detail = FPPRDetail.objects.create(company_id=cid)
                fppr_detail.asse_to_equi_r_finan_lev.set(aterfl_years)
                fppr_detail.debt_to_asse_r.set(dtar_years)
                fppr_detail.debt_to_equi_r.set(dter_years)
                fppr_detail.debt_to_capi_r.set(dtcr_years)


            company_qs = FinancialRatio.objects.filter(company_id=cid)
            print('Assign year detail value to each attribute =====================================')
            if company_qs.exists() and company_qs.count() == 1:
                print('the company ALREADY exist.')
                fr = company_qs.first()
                fr.profit_r.add(pr_detail)
                fr.liquid_r.add(lr_detail)
                fr.operat_effici_r.add(oer_detail)
                fr.finan_posit_propo_r.add(fppr_detail)
            else:
                print('the company NOT exist.')
                fr = FinancialRatio.objects.create(company_id=cid)
                fr.profit_r.add(pr_detail)
                fr.liquid_r.add(lr_detail)
                fr.operat_effici_r.add(oer_detail)
                fr.finan_posit_propo_r.add(fppr_detail)
        
        print('Store company financial ratio information finished ========----------------------=======')
    
    def process_item(self, item, spider):
        year = RatioYearDetail()
        year.company_id     = item['company_id']
        year.year           = item['year']
        year.ratio         = item['ratio']
        year.save()
        print('Store ratio details finished -----------------------------------------------------')
        return item