import json
from django.db import models
from django.utils import timezone

# Create your models here.
class ScrapyItem(models.Model):
    company_name                = models.CharField(max_length=240)
    company_id                  = models.CharField(max_length=240)
    company_type                = models.CharField(max_length=240)
    status                      = models.CharField(max_length=240)
    address                     = models.TextField()
    objective                   = models.CharField(max_length=240)
    directors                   = models.TextField()
    bussiness_type              = models.CharField(max_length=240)
    bussiness_type_code         = models.CharField(max_length=240)
    street                      = models.TextField()
    subdistrict                 = models.CharField(max_length=240)
    district                    = models.CharField(max_length=240)
    province                    = models.CharField(max_length=240)
    tel                         = models.CharField(max_length=240)
    fax                         = models.CharField(max_length=240)
    website                     = models.TextField()
    email                       = models.CharField(max_length=240)
    date                        = models.DateTimeField(default=timezone.now)

    @property
    def to_dict(self):
        data = {
            'company_name': json.loads(self.company_name),
            'company_id': json.loads(self.company_id),
            'company_type': json.loads(self.company_type),
            'status': json.loads(self.status),
            'address': json.loads(self.address),
            'objective': json.loads(self.objective),
            'directors': json.loads(self.directors),
            'bussiness_type': json.loads(self.bussiness_type),
            'bussiness_type_code': json.loads(self.bussiness_type_code),
            'street': json.loads(self.street),
            'subdistrict': json.loads(self.subdistrict),
            'district': json.loads(self.district),
            'province': json.loads(self.province),
            'tel': json.loads(self.tel),
            'fax': json.loads(self.fax),
            'website': json.loads(self.website),
            'email': json.loads(self.email),
            'date': self.date
        }
        return data

    def __str__(self):
        # return self.company_id
        return "%s : %s" %(self.company_id, self.company_name)