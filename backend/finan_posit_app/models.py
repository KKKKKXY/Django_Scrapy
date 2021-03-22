from django.db import models

# Financial Position Models
class PositYear(models.Model):
    company_id      = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    year            = models.CharField(db_column='year', max_length=20, blank=True, null=True)
    amount          = models.CharField(db_column='amount', max_length=40, blank=True, null=True)
    change          = models.CharField(db_column='change', max_length=40, blank=True, null=True)

    def __str__(self):
        return self.company_id + ' - ' + self.year + '(' + self.amount + ' , ' + self.change + ')'

    class Meta:
        managed = True
        db_table = 'posit_year_detail'
        verbose_name = 'Scraped Posit Year Detail'
        verbose_name_plural = 'Scraped Posit Year Details'

class FinancialPosition(models.Model):
    company_id              = models.CharField(db_column='company_id', max_length=20,  primary_key=True, unique = True, default='Null')
    accounts_receive        = models.ManyToManyField(PositYear, blank=True, max_length=255, related_name='accounts_receive',  db_column='accounts_receive')
    inventory               = models.ManyToManyField(PositYear, blank=True, max_length=255, related_name='inventory',  db_column='inventory')
    t_curr_asset            = models.ManyToManyField(PositYear, blank=True, max_length=255, related_name='t_curr_asset',  db_column='t_curr_asset')
    proper_plant_equip      = models.ManyToManyField(PositYear, blank=True, max_length=255, related_name='proper_plant_equip',  db_column='proper_plant_equip')
    t_nonCurr_asset         = models.ManyToManyField(PositYear, blank=True, max_length=255, related_name='t_nonCurr_asset',  db_column='t_nonCurr_asset')
    t_assets                = models.ManyToManyField(PositYear, blank=True, max_length=255, related_name='t_assets',  db_column='t_assets')
    t_curr_liab             = models.ManyToManyField(PositYear, blank=True, max_length=255, related_name='t_curr_liab',  db_column='t_curr_liab')
    t_nonCurr_liab          = models.ManyToManyField(PositYear, blank=True, max_length=255, related_name='t_nonCurr_liab',  db_column='t_nonCurr_liab')
    t_liab                  = models.ManyToManyField(PositYear, blank=True, max_length=255, related_name='t_liab',  db_column='t_liab')
    equity                  = models.ManyToManyField(PositYear, blank=True, max_length=255, related_name='equity',  db_column='equity')
    t_liab_and_equity       = models.ManyToManyField(PositYear, blank=True, max_length=255, related_name='t_liab_and_equity',  db_column='t_liab_and_equity')
    # accounts_receivable                     = models.ForeignKey(PositYear, on_delete=models.SET_NULL, blank=True, null=True, related_name='models', db_column='accounts_receivable', max_length=255)

    def __str__(self):
        return self.company_id

    class Meta:
        managed = True
        db_table = 'dbd_finian_posit'
        verbose_name = 'Scraped Financial Position'
        verbose_name_plural = 'Scraped Financial Postions'