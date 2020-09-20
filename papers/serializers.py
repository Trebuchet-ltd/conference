from rest_framework import serializers
from .models import *
from profile.models import User
from comments.models import Comment


class SmallUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'payment_status', 'nationality', 'designation', 'affiliation',
                  'highest_degree', 'subject', 'specialization']


class SmallCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        exclude = ['paper', 'id']


class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = '__all__'
        # fields = ['id', 'title', 'description', 'status', 'comments', 'keyword', 'file', 'is_poster', 'author',
        #           'abstract']

        extra_kwargs = {
            'author': {'read_only': True},
            'author_poster': {'read_only': True},
        }


class OrganiserPaperSerializer(serializers.ModelSerializer):
    comments = SmallCommentSerializer(many=True)

    author_name = SmallUserSerializer(source='author')
    author_poster_name = SmallUserSerializer(source='author_poster')

    class Meta:
        model = Paper
        fields = '__all__'
        # fields = ['id', 'title', 'description', 'status', 'comments', 'keyword', 'file', 'is_poster', 'author',
        #           'reviewer', 'abstract']

        extra_kwargs = {
            'author': {'read_only': True},
            'author_poster': {'read_only': True},
            'title': {'read_only': True},
            'description': {'read_only': True},
            'comments': {'read_only': True},
            'keyword': {'read_only': True},
            'file': {'read_only': True},
            'is_poster': {'read_only': True},
        }


class ReviewerPaperSerializer(serializers.ModelSerializer):
    comments = SmallCommentSerializer(many=True)

    class Meta:
        model = Paper
        fields = '__all__'
        # fields = ['id', 'title', 'description', 'status', 'comments', 'keyword', 'file', 'is_poster', 'author',
        #           'reviewer', 'abstract']

        extra_kwargs = {
            'author': {'read_only': True},
            'author_poster': {'read_only': True},
            'title': {'read_only': True},
            'description': {'read_only': True},
            'comments': {'read_only': True},
            'keyword': {'read_only': True},
            'is_poster': {'read_only': True},
            'reviewer': {'read_only': True},
            'file': {'read_only': True},
            'abstract': {'read_only': True},
        }


class FileUploadPaperSerializer(serializers.ModelSerializer):
    comments = SmallCommentSerializer(many=True)

    class Meta:
        model = Paper
        fields = '__all__'
        # fields = ['id', 'title', 'description', 'status', 'comments', 'keyword', 'file', 'is_poster', 'author',
        #           'abstract']

        extra_kwargs = {
            'author': {'read_only': True},
            'author_poster': {'read_only': True},
            'comments': {'read_only': True},
            'keyword': {'read_only': True},
            'is_poster': {'read_only': True},
            'reviewer': {'read_only': True},
            'status': {'read_only': True},
        }
