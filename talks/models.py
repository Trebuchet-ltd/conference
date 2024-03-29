from django.db import models
from profile.models import User

INVITE_STATES = [
    ('invited', 'invited'),
    ('accepted', 'accepted'),
    ('declined', 'declined'),
]

TRACKS = [
    (0, 'Track 0'),
    (1, 'Track 1'),
    (2, 'Track 2'),
    (3, 'Track 3'),
]

SESSION_STATUS = [
    ('submitted', 'submitted'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected'),
]


class Session(models.Model):
    organiser = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='session_organising')
    title = models.CharField(max_length=256)
    desc = models.CharField(max_length=4096, null=True, blank=True, default='')
    status = models.CharField(max_length=10, choices=SESSION_STATUS, default='submitted')
    track = models.IntegerField(choices=TRACKS, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0, blank=True)
    chair = models.CharField(max_length=255,null=True,blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.title} - ({self.organiser})'


def video_location(instance, filename):
    return f'static/media/sessions/{filename}'


class Participant(models.Model):
    title = models.CharField(max_length=255, null=True)
    speaker_name = models.CharField(max_length=255, null=True, blank=True)
    speaker = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True,
                                   related_name='session_participating', blank=True)
    affiliation = models.CharField(max_length=255, null=True)
    paper_id = models.CharField(max_length=255, null=True, blank=True)
    # abstract = ContentTypeRestrictedFileField(upload_to='static/media/sessions/',
    #                                           content_types=['application/pdf', ],
    #                                           max_upload_size=5242880, null=True)
    abstract = models.FileField(upload_to='static/media/sessions/', null=True, blank=True)

    email = models.EmailField(unique=True, null=True)
    session = models.ForeignKey(to=Session, on_delete=models.CASCADE, related_name='participants', null=True)
    status = models.CharField(choices=INVITE_STATES, default='invited', max_length=20)
    recording = models.FileField(upload_to=video_location, null=True, blank=True)
    duration = models.IntegerField(default=0, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f'{str(self.speaker_name).title()}, {self.affiliation}'


class Program(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    name = models.CharField(max_length=255)
    track = models.IntegerField(choices=TRACKS, default=1)
