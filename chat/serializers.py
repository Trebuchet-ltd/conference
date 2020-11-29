from rest_framework import serializers
from .models import *


class InChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class OutChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['timestamp','user_name','message']
