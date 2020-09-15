from rest_framework import serializers
from .models import *


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

    class Meta:
        model = Session
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    session = serializers.StringRelatedField()

    class Meta:
        model = Participant
        fields = '__all__'
