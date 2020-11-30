from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
import requests
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import views
import json
from .models import Chat
from .serializers import *
from rest_framework import status
import datetime
import hmac
import hashlib
import codecs
from django.shortcuts import redirect

# Create your views here.
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    # serializer_class = InChatSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return OutChatSerializer
        if self.action == 'create':
            return InChatSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        serializer.save()
        return Response(status.HTTP_200_OK)

    def get_queryset(self):
        timestamp = self.request.query_params.get('timestamp')
        stream = self.request.query_params.get('stream')
        if timestamp!=None and stream!=None:
            queryset = Chat.objects.filter(timestamp__gte=timestamp,stream=stream).values('timestamp','user_name','message')
            return queryset
