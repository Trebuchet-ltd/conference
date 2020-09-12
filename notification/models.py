from django.db import models

# Create your models here.
class Notification(models.Model):
    user_id = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    link = models.CharField(max_length=255)