from django.db import models

# Create your models here.
class IncomeYearDetail(models.Model):
    company_id      = models.CharField(db_column='company_id', max_length=20, blank=True, null=True)
    year            = models.CharField(db_column='year', max_length=20, blank=True, null=True)
    amount          = models.CharField(db_column='amount', max_length=40, blank=True, null=True)
    change          = models.CharField(db_column='change', max_length=40, blank=True, null=True)

    def __str__(self):
        return self.company_id + ' - ' + self.year + '(' + self.amount + ' , ' + self.change + ')'

    class Meta:
        managed = True
        db_table = 'income_year_detail_eng'
        verbose_name = 'Income Year Details'
        verbose_name_plural = 'Scraped Eng Income Year Detail'

class IncomeStat(models.Model):
    company_id                      = models.CharField(db_column='company_id', max_length=20,  primary_key=True, unique = True, default='Null')
    reve_from_sale_serv             = models.ManyToManyField(IncomeYearDetail, blank=True, max_length=255, related_name='reve_from_sale_serv',  db_column='reve_from_sale_serv')
    t_reve                          = models.ManyToManyField(IncomeYearDetail, blank=True, max_length=255, related_name='t_reve',  db_column='t_reve')
    cost_of_goods_sold              = models.ManyToManyField(IncomeYearDetail, blank=True, max_length=255, related_name='cost_of_goods_sold',  db_column='cost_of_goods_sold')
    gross_profit                    = models.ManyToManyField(IncomeYearDetail, blank=True, max_length=255, related_name='gross_profit',  db_column='gross_profit')
    sell_admin_expe                 = models.ManyToManyField(IncomeYearDetail, blank=True, max_length=255, related_name='sell_admin_expe',  db_column='sell_admin_expe')
    t_expe                          = models.ManyToManyField(IncomeYearDetail, blank=True, max_length=255, related_name='t_expe',  db_column='t_expe')
    intere_expe                     = models.ManyToManyField(IncomeYearDetail, blank=True, max_length=255, related_name='intere_expe',  db_column='intere_expe')
    profit_before_income_tax        = models.ManyToManyField(IncomeYearDetail, blank=True, max_length=255, related_name='profit_before_income_tax',  db_column='profit_before_income_tax')
    income_tax_expe                 = models.ManyToManyField(IncomeYearDetail, blank=True, max_length=255, related_name='income_tax_expe',  db_column='income_tax_expe')
    net_profit                      = models.ManyToManyField(IncomeYearDetail, blank=True, max_length=255, related_name='net_profit',  db_column='net_profit')

    def __str__(self):
        return self.company_id

    class Meta:
        managed = True
        db_table = 'income_statement_eng'
        verbose_name = 'Income Statements'
        verbose_name_plural = 'Scraped Eng Income Statement'