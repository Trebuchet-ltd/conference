from rest_framework import serializers
from .models import *


class PaperSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Paper
        fields = '__all__'
