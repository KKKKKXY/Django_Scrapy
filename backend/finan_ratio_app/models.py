from django.db import models

# Create your models here.
# Year Ratio
class RatioYearDetail(models.Model):
    company_id      = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    year            = models.CharField(db_column='year', max_length=20, blank=True, null=True)
    ratio           = models.CharField(db_column='ratio', max_length=20, blank=True, null=True)

    def __str__(self):
        return self.company_id + ' - ' + self.year + '(' + self.ratio + ')'

    class Meta:
        managed = True
        db_table = 'ratio_year_detail_eng'
        verbose_name = 'Ratio Year Details'
        verbose_name_plural = 'Scraped Eng Ratio Year Detail'

# Different Ratio
class PRDetail(models.Model):
    company_id              = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    ret_on_asset            = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='ret_on_asset',  db_column='ret_on_asset')      
    ret_on_equity           = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='ret_on_equity',  db_column='ret_on_equity')
    gross_profit_mar        = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='gross_profit_mar',  db_column='gross_profit_mar')  
    opera_inc_on_reve_r     = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='opera_inc_on_reve_r',  db_column='opera_inc_on_reve_r')
    net_profit_mar          = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='net_profit_mar',  db_column='net_profit_mar')
    
    def __str__(self):
        return 'profitability ratio for: ' + self.company_id

    class Meta:
        managed = True
        db_table = 'profit_ratio_detail_eng'
        verbose_name = 'Profit Ratio Details'
        verbose_name_plural = 'Scraped Eng Profit Ratio Detail'

class LRDetail(models.Model):
    company_id          = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    curr_r              = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='curr_r',  db_column='curr_r')      
    acco_recei_tur      = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='acco_recei_tur',  db_column='acco_recei_tur')
    invent_tur          = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='invent_tur',  db_column='invent_tur')  
    acco_pay_tur        = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='acco_pay_tur',  db_column='acco_pay_tur')

    def __str__(self):
        return 'liquidity ratio for: ' + self.company_id

    class Meta:
        managed = True
        db_table = 'liquid_ratio_detail_eng'
        verbose_name = 'Liquid Ratio Details'
        verbose_name_plural = 'Scraped Eng Liquid Ratio Detail'

class OERDetail(models.Model):
    company_id                  = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    t_asset_tur                 = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='t_asset_tur',  db_column='t_asset_tur')      
    opera_expe_to_t_reve_r      = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='opera_expe_to_t_reve_r',  db_column='opera_expe_to_t_reve_r')

    def __str__(self):
        return 'operation efficiency ratio for: ' + self.company_id

    class Meta:
        managed = True
        db_table = 'operat_effici_ratio_detail_eng'
        verbose_name = 'Operat Effici Ratio Details'
        verbose_name_plural = 'Scraped Eng Operat Effici Ratio Detail'

class FPPRDetail(models.Model):
    company_id                  = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    asse_to_equi_r_finan_lev    = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='asse_to_equi_r_finan_lev',  db_column='asse_to_equi_r_finan_lev')      
    debt_to_asse_r              = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='debt_to_asse_r',  db_column='debt_to_asse_r')
    debt_to_equi_r              = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='debt_to_equi_r',  db_column='debt_to_equi_r')  
    debt_to_capi_r              = models.ManyToManyField(RatioYearDetail, blank=True, max_length=255, related_name='debt_to_capi_r',  db_column='debt_to_capi_r')

    def __str__(self):
        return 'financial position proportion ratio for: ' + self.company_id

    class Meta:
        managed = True
        db_table = 'finan_posit_propo_ratio_detail_eng'
        verbose_name = 'Finan Posit Propo Ratio Details'
        verbose_name_plural = 'Scraped Eng Finan Posit Propo Ratio Detail'

# Financial Ratio
class FinancialRatio(models.Model):
    company_id              = models.CharField(db_column='company_id', max_length=20,  primary_key=True, unique = True, default='Null')
    profit_r                = models.ManyToManyField(PRDetail, blank=True, max_length=255, related_name='profit_r',  db_column='profit_r')
    liquid_r                = models.ManyToManyField(LRDetail, blank=True, max_length=255, related_name='liquid_r',  db_column='liquid_r')
    operat_effici_r         = models.ManyToManyField(OERDetail, blank=True, max_length=255, related_name='operat_effici_r',  db_column='operat_effici_r')
    finan_posit_propo_r     = models.ManyToManyField(FPPRDetail, blank=True, max_length=255, related_name='finan_posit_propo_r',  db_column='finan_posit_propo_r')

    def __str__(self):
        return self.company_id

    class Meta:
        managed = True
        db_table = 'finian_ratio_eng'
        verbose_name = 'Financial Ratios'
        verbose_name_plural = 'Scraped Eng Financial Ratio'