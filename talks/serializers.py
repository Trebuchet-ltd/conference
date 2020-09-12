from rest_framework import serializers
from .models import *


class BaseSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    session = BaseSessionSerializer()

    class Meta:
        model = Participant
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Session
        fields = '__all__'
