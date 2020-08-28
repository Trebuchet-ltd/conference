from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class ConferenceUser(models.Model):
    class Meta:
        db_table='users'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField()
    name = models.CharField(max_length=255)
    number = models.IntegerField(default=0,blank=False)
    payment = models.BooleanField(default=False,blank=False)
    type = models.CharField(max_length=255)
    paper_id=models.CharField(max_length=255,default='',blank=True)
    poster_id=models.CharField(max_length=255,default='',blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ConferenceUser.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()