from django.db import models
from django.utils import timezone

# Company Profile Models
class DBDCompany_Thai(models.Model):
    company_id                      = models.CharField(db_column='company_id', max_length=20,  primary_key=True, unique = True, default='Null')
    company_name                    = models.CharField(db_column='company_name', max_length=255, default='Null')
    company_type                    = models.CharField(db_column='company_type', max_length=255, default='Null')
    company_status                  = models.CharField(db_column='company_status', max_length=255, default='Null')
    company_objective               = models.TextField(db_column='company_objective', default='Null')
    company_directors               = models.TextField(db_column='company_directors')
    company_bussiness_type          = models.TextField(db_column='company_bussiness_type', default='Null')
    company_bussiness_type_code     = models.CharField(db_column='company_bussiness_code', max_length=20, default='Null')
    company_street                  = models.TextField(db_column='company_street', default='Null')
    company_subdistrict             = models.CharField(db_column='company_subdistrict', max_length=255, default='Null')
    company_district                = models.CharField(db_column='company_district', max_length=255, default='Null')
    company_province                = models.CharField(db_column='company_province', max_length=255, default='Null')
    company_address                 = models.TextField(db_column='company_address', default='Null')
    company_tel                     = models.CharField(db_column='company_tel', max_length=255, default='Null')
    company_fax                     = models.CharField(db_column='company_fax', max_length=255, default='Null')
    company_website                 = models.CharField(db_column='company_website', max_length=255, default='Null')
    company_email                   = models.CharField(db_column='company_email', max_length=255, default='Null')
    company_last_registered_id      = models.CharField(db_column='company_last_registered_id', max_length=20, default='Null')
    company_fiscal_year             = models.CharField(db_column='company_fiscal_year', max_length=255, default='Null')
    created                         = models.DateTimeField(auto_now_add=True)
    is_changed                      = models.BooleanField(default=False)

    def __str__(self):
        return self.company_id + ": " + self.company_name

    class Meta:
        managed = True
        db_table = 'dbd_scraped_thai'
        verbose_name = 'Scraped Thai Company'
        verbose_name_plural = 'Scraped Thai Companies'