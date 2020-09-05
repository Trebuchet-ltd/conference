from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['paper', 'message', 'author', 'time']
        extra_kwargs = {
            'author': {'read_only': True},
            'time': {'read_only': True},
        }
