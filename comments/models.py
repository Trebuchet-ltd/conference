from django.db import models
from papers.models import Paper
from users.models import User



class Comment(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='comments')
    message = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.message} - {str(self.author)}'
