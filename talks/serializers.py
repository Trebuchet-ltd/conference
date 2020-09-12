from rest_framework import serializers
from .models import *


class ParticipantSerializer(serializers.ModelSerializer):
    session = serializers.StringRelatedField()

    class Meta:
        model = Participant
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Session
        fields = '__all__'
