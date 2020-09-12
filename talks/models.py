from django.db import models
from profile.models import User

INVITE_STATES = [
    ('invited', 'invited'),
    ('accepted', 'accepted'),
    ('declined', 'declined'),
]


class Session(models.Model):
    organiser = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='session_organising')
    title = models.CharField(max_length=256)
    desc = models.CharField(max_length=4096)

    def __str__(self):
        return f'{self.title} - ({self.organiser})'


class Participant(models.Model):
    title = models.CharField(max_length=255, null=True)
    speaker_name = models.CharField(max_length=255, null=True)
    speaker = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True,
                                   related_name='session_participating')
    affiliation = models.CharField(max_length=255, null=True)
    paper_id = models.CharField(max_length=255, null=True)
    abstract = models.FileField(upload_to='static/media/sessions/', null=True)

    email = models.EmailField(unique=True,null=True)
    session = models.ForeignKey(to=Session, on_delete=models.CASCADE, related_name='participants',null=True)
    status = models.CharField(choices=INVITE_STATES, default='invited', max_length=20)

    def __str__(self):
        return f'{self.title} - [{str(self.speaker)}]'
