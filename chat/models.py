from django.db import models

# Create your models here.
class Chat(models.Model):
    class Meta:
        app_label = 'chat'

    timestamp = models.IntegerField(null=False,blank=False)
    uid = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    message = models.CharField(max_length=2048)
    stream = models.IntegerField(null=False,blank=False)

