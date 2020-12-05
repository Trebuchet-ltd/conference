from django.db import models
from profile.models import User
from chunked_upload.models import ChunkedUpload

INVITE_STATES = [
    ('invited', 'invited'),
    ('accepted', 'accepted'),
    ('declined', 'declined'),
]

TRACKS = [
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

    def __str__(self):
        return f'{self.title} - ({self.organiser})'


class Participant(models.Model):
    title = models.CharField(max_length=255, null=True)
    speaker_name = models.CharField(max_length=255, null=True)
    speaker = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True,
                                   related_name='session_participating')
    affiliation = models.CharField(max_length=255, null=True)
    paper_id = models.CharField(max_length=255, null=True)
    # abstract = ContentTypeRestrictedFileField(upload_to='static/media/sessions/',
    #                                           content_types=['application/pdf', ],
    #                                           max_upload_size=5242880, null=True)
    abstract = models.FileField(upload_to='static/media/sessions/', null=True)

    email = models.EmailField(unique=True, null=True)
    session = models.ForeignKey(to=Session, on_delete=models.CASCADE, related_name='participants', null=True)
    status = models.CharField(choices=INVITE_STATES, default='invited', max_length=20)

    def __str__(self):
        return f'{self.title.capitalize()} by {str(self.speaker_name).capitalize()}, {self.affiliation.capitalize()}'


class Program(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    name = models.CharField(max_length=255)
    track = models.IntegerField(choices=TRACKS, default=1)


MyChunkedUpload = ChunkedUpload
