from django.db import models

# Create your models here.
class Payments(models.Model):
    p_id=models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

class Rate(models.Model):
    rate = models.CharField(max_length=255)
    updated_on = models.DateTimeField(auto_created=True)

