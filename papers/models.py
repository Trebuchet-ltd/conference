from django.db import models
from users.models import User


# TODO: Make status an enum.
# TODO: Add Approved_Paper field.

def media_location(instance, filename):
    if instance.is_poster:
        return f'media/posters/{filename}'
    return f'media/papers/{filename}'


class Paper(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=255, default='pending')
    keyword = models.CharField(max_length=255)
    file = models.FileField(upload_to=media_location, null=True)
    is_poster = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_papers', null=True)
    approved_paper = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paper', null=True)
    approved_poster = models.OneToOneField(User, on_delete=models.CASCADE, related_name='poster', null=True)

    def __str__(self):
        return self.title
