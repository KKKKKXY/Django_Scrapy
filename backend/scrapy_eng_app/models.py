from django.db import models
from django.utils import timezone

# Create your models here.
class DBDCompany_Eng(models.Model):
    company_id                      = models.CharField(db_column='company_id', max_length=20,  primary_key=True)
    company_name                    = models.CharField(db_column='company_name', max_length=255)
    company_type                    = models.CharField(db_column='company_type', max_length=255)
    company_status                  = models.CharField(db_column='company_status', max_length=255)
    company_objective               = models.TextField(db_column='company_objective')
    company_directors               = models.TextField(db_column='company_directors')
    company_bussiness_type          = models.TextField(db_column='company_bussiness_type')
    company_bussiness_type_code     = models.CharField(db_column='company_bussiness_code', max_length=20)
    company_street                  = models.TextField(db_column='company_street')
    company_subdistrict             = models.CharField(db_column='company_subdistrict', max_length=255)
    company_district                = models.CharField(db_column='company_district', max_length=255)
    company_province                = models.CharField(db_column='company_province', max_length=255)
    company_address                 = models.TextField(db_column='company_address')
    company_tel                     = models.CharField(db_column='company_tel', max_length=255)
    company_fax                     = models.CharField(db_column='company_fax', max_length=255)
    company_website                 = models.CharField(db_column='company_website', max_length=255)
    company_email                   = models.CharField(db_column='company_email', max_length=255)
    # company_zipcode         = models.CharField(db_column='company_zipcode', max_length=240)
    
    def __str__(self):
        return self.company_id + " " + self.company_name

    class Meta:
        managed = True
        db_table = 'dbd_scraped_company_eng'
        verbose_name = 'Scraped Company'
        verbose_name_plural = 'Scraped Eng Companies'