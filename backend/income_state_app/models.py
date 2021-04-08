from django.db import models

# Income Statement Models
# Income Year
class IncomeYear(models.Model):
    company_id      = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    year            = models.CharField(db_column='year', max_length=20, blank=True, null=True)
    amount          = models.CharField(db_column='amount', max_length=40, blank=True, null=True)
    change          = models.CharField(db_column='change', max_length=40, blank=True, null=True)

    def __str__(self):
        return self.company_id + ' - ' + self.year + '(' + self.amount + ' , ' + self.change + ')'

    class Meta:
        managed = True
        db_table = 'income_year_detail'
        verbose_name = 'Scraped Income Year Detail'
        verbose_name_plural = 'Scraped Income Year Details'

# Income Statement
class IncomeStatement(models.Model):
    company_id                      = models.CharField(db_column='company_id', max_length=20,  primary_key=True, unique = True, default='Null')
    reve_from_sale_serv             = models.ManyToManyField(IncomeYear, blank=True, max_length=255, related_name='reve_from_sale_serv',  db_column='reve_from_sale_serv')
    t_reve                          = models.ManyToManyField(IncomeYear, blank=True, max_length=255, related_name='t_reve',  db_column='t_reve')
    cost_of_goods_sold              = models.ManyToManyField(IncomeYear, blank=True, max_length=255, related_name='cost_of_goods_sold',  db_column='cost_of_goods_sold')
    gross_profit                    = models.ManyToManyField(IncomeYear, blank=True, max_length=255, related_name='gross_profit',  db_column='gross_profit')
    sell_admin_expe                 = models.ManyToManyField(IncomeYear, blank=True, max_length=255, related_name='sell_admin_expe',  db_column='sell_admin_expe')
    t_expe                          = models.ManyToManyField(IncomeYear, blank=True, max_length=255, related_name='t_expe',  db_column='t_expe')
    intere_expe                     = models.ManyToManyField(IncomeYear, blank=True, max_length=255, related_name='intere_expe',  db_column='intere_expe')
    profit_before_income_tax        = models.ManyToManyField(IncomeYear, blank=True, max_length=255, related_name='profit_before_income_tax',  db_column='profit_before_income_tax')
    income_tax_expe                 = models.ManyToManyField(IncomeYear, blank=True, max_length=255, related_name='income_tax_expe',  db_column='income_tax_expe')
    net_profit                      = models.ManyToManyField(IncomeYear, blank=True, max_length=255, related_name='net_profit',  db_column='net_profit')

    def __str__(self):
        return self.company_id

    class Meta:
        managed = True
        db_table = 'dbd_income_statement'
        verbose_name = 'Scraped Income Statement'
        verbose_name_plural = 'Scraped Income Statements'