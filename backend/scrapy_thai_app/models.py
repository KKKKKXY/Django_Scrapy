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
    
    # @property
    # def to_dict(self):
    #     data = {
    #         'company_id': json.loads(self.company_id),
    #         'company_name': json.loads(self.company_name),
    #         'company_type': json.loads(self.company_type),
    #         'company_status': json.loads(self.company_status),
    #         'company_objective': json.loads(self.company_objective),
    #         'company_directors': json.loads(self.company_directors),
    #         'company_bussiness_type': json.loads(self.company_bussiness_type),
    #         'company_bussiness_type_code': json.loads(self.company_bussiness_type_code),
    #         'company_street': json.loads(self.company_street),
    #         'company_subdistrict': json.loads(self.company_subdistrict),
    #         'company_district': json.loads(self.company_district),
    #         'company_province': json.loads(self.company_province),
    #         'company_address': json.loads(self.company_address),
    #         'company_tel': json.loads(self.company_tel),
    #         'company_fax': json.loads(self.company_fax),
    #         'company_website': json.loads(self.company_website),
    #         'company_email': json.loads(self.company_email),
    #         'company_last_registered_id': json.loads(self.company_last_registered_id),
    #         'company_fiscal_year': json.loads(self.company_fiscal_year),
    #         'date': self.date
    #     }
    #     return data