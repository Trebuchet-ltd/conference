from rest_framework import serializers
from .models import *
from profile.models import User


class SmallUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'payment_status', 'nationality', 'designation', 'affiliation',
                  'highest_degree', 'subject', 'specialization']


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class BaseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    participants = BaseParticipantSerializer(many=True)
    organiser = SmallUserSerializer()

    class Meta:
        model = Session
        fields = '__all__'
        extra_kwargs = {
            'status': {'read_only': True},
        }


class SmallSessionSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)
    organiser = serializers.StringRelatedField()

    class Meta:
        model = Session
        fields = ["organiser", "title", "desc", "status", "participants"]
        extra_kwargs = {
            'status': {'read_only': True},
        }


class ParticipantSerializer(serializers.ModelSerializer):
    session = serializers.StringRelatedField()

    class Meta:
        model = Participant
        fields = '__all__'
