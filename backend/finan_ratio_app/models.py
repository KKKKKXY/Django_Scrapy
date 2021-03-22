from django.db import models

# Financial Ratio Models
# Ratio Year
class RatioYear(models.Model):
    company_id      = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    year            = models.CharField(db_column='year', max_length=20, blank=True, null=True)
    ratio           = models.CharField(db_column='ratio', max_length=20, blank=True, null=True)

    def __str__(self):
        return self.company_id + ' - ' + self.year + '(' + self.ratio + ')'

    class Meta:
        managed = True
        db_table = 'ratio_year_detail'
        verbose_name = 'Scraped Ratio Year Detail'
        verbose_name_plural = 'Scraped Ratio Year Details'

# Different Ratio
# Profitability Ratio
class PRatio(models.Model):
    company_id              = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    ret_on_asset            = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='ret_on_asset',  db_column='ret_on_asset')      
    ret_on_equity           = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='ret_on_equity',  db_column='ret_on_equity')
    gross_profit_mar        = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='gross_profit_mar',  db_column='gross_profit_mar')  
    opera_inc_on_reve_r     = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='opera_inc_on_reve_r',  db_column='opera_inc_on_reve_r')
    net_profit_mar          = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='net_profit_mar',  db_column='net_profit_mar')
    
    def __str__(self):
        return 'profitability ratio for: ' + self.company_id

    class Meta:
        managed = True
        db_table = 'profit_ratio'
        verbose_name = 'Scraped Profit Ratio'
        verbose_name_plural = 'Scraped Profit Ratios'

# Liquidity Ratio
class LRatio(models.Model):
    company_id          = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    curr_r              = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='curr_r',  db_column='curr_r')      
    acco_recei_tur      = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='acco_recei_tur',  db_column='acco_recei_tur')
    invent_tur          = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='invent_tur',  db_column='invent_tur')  
    acco_pay_tur        = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='acco_pay_tur',  db_column='acco_pay_tur')

    def __str__(self):
        return 'liquidity ratio for: ' + self.company_id

    class Meta:
        managed = True
        db_table = 'liquid_ratio'
        verbose_name = 'Scraped Liquid Ratio'
        verbose_name_plural = 'Scraped Liquid Ratios'

# Operation Efficiency Ratio
class OERatio(models.Model):
    company_id                  = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    t_asset_tur                 = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='t_asset_tur',  db_column='t_asset_tur')      
    opera_expe_to_t_reve_r      = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='opera_expe_to_t_reve_r',  db_column='opera_expe_to_t_reve_r')

    def __str__(self):
        return 'operation efficiency ratio for: ' + self.company_id

    class Meta:
        managed = True
        db_table = 'operat_effici_ratio'
        verbose_name = 'Scraped Operat Effici Ratio'
        verbose_name_plural = 'Scraped Operat Effici Ratios'

# Financial Position Proportion Ratio
class FPPRatio(models.Model):
    company_id                  = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    asse_to_equi_r_finan_lev    = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='asse_to_equi_r_finan_lev',  db_column='asse_to_equi_r_finan_lev')      
    debt_to_asse_r              = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='debt_to_asse_r',  db_column='debt_to_asse_r')
    debt_to_equi_r              = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='debt_to_equi_r',  db_column='debt_to_equi_r')  
    debt_to_capi_r              = models.ManyToManyField(RatioYear, blank=True, max_length=255, related_name='debt_to_capi_r',  db_column='debt_to_capi_r')

    def __str__(self):
        return 'financial position proportion ratio for: ' + self.company_id

    class Meta:
        managed = True
        db_table = 'finan_posit_propo_ratio'
        verbose_name = 'Scraped Finan Posit Propo Ratio'
        verbose_name_plural = 'Scraped Finan Posit Propo Ratios'

# Financial Ratio
class FinancialRatio(models.Model):
    company_id              = models.CharField(db_column='company_id', max_length=20,  primary_key=True, unique = True, default='Null')
    profit_r                = models.ManyToManyField(PRatio, blank=True, max_length=255, related_name='profit_r',  db_column='profit_r')
    liquid_r                = models.ManyToManyField(LRatio, blank=True, max_length=255, related_name='liquid_r',  db_column='liquid_r')
    operat_effici_r         = models.ManyToManyField(OERatio, blank=True, max_length=255, related_name='operat_effici_r',  db_column='operat_effici_r')
    finan_posit_propo_r     = models.ManyToManyField(FPPRatio, blank=True, max_length=255, related_name='finan_posit_propo_r',  db_column='finan_posit_propo_r')

    def __str__(self):
        return self.company_id

    class Meta:
        managed = True
        db_table = 'dbd_finian_ratio'
        verbose_name = 'Scraped Financial Ratio'
        verbose_name_plural = 'Scraped Financial Ratios'