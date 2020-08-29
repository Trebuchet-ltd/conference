from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class ConferenceUser(models.Model):
    class Meta:
        db_table = 'users'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    number = models.IntegerField(default=0, blank=False)
    payment = models.BooleanField(default=False, blank=False)
    type = models.CharField(max_length=255)
    paper = models.CharField(max_length=255, default='', blank=True)
    poster = models.CharField(max_length=255, default='', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(self, instance, created, **kwargs):
        if created:
            ConferenceUser.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(self, instance, **kwargs):
        instance.profile.save()
