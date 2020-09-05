from rest_framework import serializers
from .models import *


class PaperSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Paper
        fields = ['id', 'title', 'description', 'status', 'comments', 'keyword', 'file', 'is_poster', 'author',
                  'approved_paper',
                  'approved_poster']

        extra_kwargs = {
            'author': {'read_only': True}
        }
