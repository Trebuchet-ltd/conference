from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
import requests
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import views
import json
from .models import *
from .serializers import *
from rest_framework import status
import datetime
import hmac
import hashlib
import codecs
from django.shortcuts import redirect
from rest_framework import permissions, viewsets
import json


# Create your views here.
class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer

    def perform_create(self, serializer):
        print('created')

    @action(detail=True, methods=['get'])
    def current_stream(self, request, pk=None):
        track = request.query_params.get('track')
        data = Stream.objects.get(track=track)
        payload = {'Stream': data.current_stream, 'Title': data.title}
        return Response(payload)

    @action(detail=True, methods=['post'])
    def set_stream(self, request, pk=None):
        print(request.data)
        print(request.POST)
        track = request.data['track']
        stream_model = Stream.objects.get(track=track)
        if 'title' in request.data:
            title = request.data['title']
            stream_model.title = title
        try:
            type = request.data['type']
            if type == "live":
                live_server = int(request.data['server'])
                if live_server == 1:
                    stream_model.current_stream = stream_model.live_server1
                    stream_model.save()
                elif live_server == 2:
                    stream_model.current_stream = stream_model.live_server2
                    stream_model.save()
                return Response(status.HTTP_200_OK)
            elif type == "link":
                stream_model.link = request.data['link']
                stream_model.current_stream = request.data['link']
                stream_model.save()
                return Response(status.HTTP_200_OK)
            return Response(status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            print("No data")
            return Response(status.HTTP_200_OK)
