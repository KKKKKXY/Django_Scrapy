from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
def upload_path(instance, filename):
    return '/'.join([str(instance.file_type), filename])

class File(models.Model):
    file_type = models.CharField(max_length=32, blank=False)
    file = models.FileField(blank=True, null=True, upload_to=upload_path)
    filename = models.CharField(max_length=32, blank=False)
    
    def __str__(self):
        return self.filename