from django.db import models
from users.models import User

REVIEW_STAGES = [
    ('submitted', 'submitted'),
    ('reviewing', 'reviewing'),
    ('assigned', 'assigned'),
    ('reviewed', 'reviewed'),
    ('approved', 'approved'),
    ('rejected', 'rejected'),
    ('corrections', 'corrections'),
]


def media_location(instance, filename):
    if instance.is_poster:
        return f'static/media/posters/{filename}'
    return f'static/media/papers/{filename}'


class Paper(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    status = models.CharField(choices=REVIEW_STAGES, max_length=12, default='submitted')
    keyword = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to=media_location, null=True)
    is_poster = models.BooleanField(default=False)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='papers', null=True)
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paper', null=True)
    submission_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
