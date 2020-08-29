from django.db import models


# Create your models here.
class Paper(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255)
    file = models.FileField(upload_to='papers/')
