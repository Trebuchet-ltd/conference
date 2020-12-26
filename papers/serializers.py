from rest_framework import serializers
from .models import *
from profile.models import User
from comments.models import Comment


class SmallUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'payment_status', 'nationality', 'designation', 'affiliation',
                  'highest_degree', 'subject', 'specialization','is_plenary']


class SmallCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        exclude = ['paper', 'id']


class SmallPaperSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    author_poster = serializers.StringRelatedField()

    class Meta:
        model = Paper
        # fields = '__all__'
        fields = ['id', 'title', 'description', 'author_poster', 'status', 'comments', 'keyword', 'file', 'is_poster',
                  'author', 'abstract', 'recording', 'display_front','chair']

        extra_kwargs = {
            'author': {'read_only': True},
            'author_poster': {'read_only': True},
            'comments': {'read_only': True, 'required': False},

        }


class PaperSerializer(serializers.ModelSerializer):
    comments = SmallCommentSerializer(many=True, required=False)
    author_name = SmallUserSerializer(source='author', required=False)
    author_poster_name = SmallUserSerializer(source='author_poster', required=False)

    class Meta:
        model = Paper
        # fields = '__all__'
        fields = ['id', 'title', 'description', 'author_poster', 'status', 'comments', 'keyword', 'file', 'is_poster',
                  'author', 'abstract', 'author_name', 'author_poster_name', 'recording', 'track', 'time', 'duration',
                  'display_front','chair']

        extra_kwargs = {
            'author': {'read_only': True},
            'author_poster': {'read_only': True},
            'comments': {'read_only': True, 'required': False},

        }


class OrganiserPaperSerializer(serializers.ModelSerializer):
    comments = SmallCommentSerializer(many=True, required=False)

    author_name = SmallUserSerializer(source='author', required=False)
    author_poster_name = SmallUserSerializer(source='author_poster', required=False)

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
            'is_poster': {'read_only': True},
            'reviewer': {'read_only': True},
            'file': {'read_only': True},
            'abstract': {'read_only': True},
        }


class FileUploadPaperSerializer(serializers.ModelSerializer):
    comments = SmallCommentSerializer(many=True, required=False, read_only=True)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Paper
        # # fields = '__all__'
        # exclude = ['comments']
        fields = ['id', 'title', 'description', 'comments', 'status', 'keyword', 'file', 'is_poster', 'author',
                  'abstract', 'author_poster','display_front','chair']

        extra_kwargs = {
            'author': {'read_only': True},
            'author_poster': {'read_only': True},
            'comments': {'read_only': True},
            'keyword': {'read_only': True},
            'is_poster': {'read_only': True},
            'reviewer': {'read_only': True},
            'status': {'read_only': True},
        }

    def get_validation_exclusions(self):
        exclusions = super(FileUploadPaperSerializer, self).get_validation_exclusions()
        return exclusions + ['comments']
