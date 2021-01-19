from django.db import models
from django.utils import timezone

# Create your models here.


class DBDCompany(models.Model):

    company_id = models.CharField(
        db_column='company_id', max_length=20,  primary_key=True)
    company_name = models.CharField(db_column='company_name', max_length=255)
    company_type = models.CharField(db_column='company_type', max_length=255)
    company_objective = models.CharField(
        db_column='company_objective', max_length=240)

    def __str__(self):
        return self.company_id + " " + self.company_name

    class Meta:
        managed = True
        db_table = 'dbd_scraped_company'
        verbose_name = 'Scraped Company'
        verbose_name_plural = 'Scraped Companies'
