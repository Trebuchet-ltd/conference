from django.db import models


# Create your models here.
class Stream(models.Model):
    track = models.IntegerField(primary_key=True)
    live_server1 = models.CharField(max_length=255)
    live_server2 = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    current_stream = models.CharField(max_length=255)
