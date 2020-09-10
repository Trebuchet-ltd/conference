from django.db import models

# Create your models here.
class Participants(models.Model):
    title = models.CharField(max_length=255)
    speaker = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)
    paper_id= models.CharField(max_length=255)
    email = models.EmailField(unique=True)

class Session(models.Model):
    organiser = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=2048)
    participants = models.ForeignKey(to=Participants,on_delete=models.CASCADE,default=None)
