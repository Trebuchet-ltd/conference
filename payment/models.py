from django.db import models

# Create your models here.
class Payments(models.Model):
    p_id=models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=255)
