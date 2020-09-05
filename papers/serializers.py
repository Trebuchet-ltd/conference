from rest_framework import serializers
from .models import *


class PaperSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Paper
        fields = ['id', 'title', 'description', 'status', 'comments', 'keyword', 'file', 'is_poster', 'author']

        extra_kwargs = {
            'author': {'read_only': True}
        }


class OrganiserPaperSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Paper
        fields = ['id', 'title', 'description', 'status', 'comments', 'keyword', 'file', 'is_poster', 'author',
                  'reviewer']

        extra_kwargs = {
            'author': {'read_only': True},
            'title': {'read_only': True},
            'description': {'read_only': True},
            'comments': {'read_only': True},
            'keyword': {'read_only': True},
            'file': {'read_only': True},
            'is_poster': {'read_only': True},
        }


class ReviewerPaperSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Paper
        fields = ['id', 'title', 'description', 'status', 'comments', 'keyword', 'file', 'is_poster', 'author',
                  'reviewer']

        extra_kwargs = {
            'author': {'read_only': True},
            'title': {'read_only': True},
            'description': {'read_only': True},
            'comments': {'read_only': True},
            'keyword': {'read_only': True},
            'is_poster': {'read_only': True},
            'reviewer': {'read_only': True},
            'file': {'read_only': True},
        }


class FileUploadPaperSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Paper
        fields = ['id', 'title', 'description', 'status', 'comments', 'keyword', 'file', 'is_poster', 'author',
                  'reviewer']

        extra_kwargs = {
            'author': {'read_only': True},
            'title': {'read_only': True},
            'description': {'read_only': True},
            'comments': {'read_only': True},
            'keyword': {'read_only': True},
            'is_poster': {'read_only': True},
            'reviewer': {'read_only': True},
            'status': {'read_only': True},
        }
