from django.db import models
from profile.models import User

REVIEW_STAGES = [
    ('submitted', 'submitted'),
    ('reviewing', 'reviewing'),
    ('assigned', 'assigned'),
    ('reviewed', 'reviewed'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected'),
    ('corrections', 'corrections'),
    ('upload paper', 'upload paper'),
]

TRACKS = [
    (1, 1),
    (2, 2),
    (3, 3)
]


def media_location(instance, filename):
    if instance.is_poster:
        return f'static/media/posters/{filename}'
    return f'static/media/papers/{filename}'


def video_location(instance, filename):
    return f'static/media/paper_recordings/{filename}'


class Paper(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    status = models.CharField(choices=REVIEW_STAGES, max_length=12, default='submitted')
    keyword = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to=media_location, null=True, blank=True)
    abstract = models.FileField(upload_to='static/media/abstracts/', null=True, blank=True)
    is_poster = models.BooleanField(default=False)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='papers', null=True, blank=True)
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paper', null=True, blank=True)
    author_poster = models.OneToOneField(User, on_delete=models.CASCADE, related_name='poster', null=True, blank=True)
    submission_time = models.DateTimeField(auto_now=True)
    display = models.BooleanField(default=True)
    recording = models.FileField(upload_to=video_location, null=True, blank=True)
    track = models.IntegerField(choices=TRACKS, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
