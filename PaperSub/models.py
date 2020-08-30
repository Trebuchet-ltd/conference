from django.db import models


class Paper(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=255, default='pending')
    comment = models.CharField(max_length=255, null=True)
    keyword = models.CharField(max_length=255)
    file = models.FileField(upload_to='papers/', null=True)
