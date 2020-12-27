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
        if (data.current_stream == data.link):
            payload = {'Stream': data.current_stream, 'Title': data.title, 'Type': "Link",'Seek':data.seek}
        elif (data.current_stream == data.live_server1 or data.current_stream == data.live_server2):
            payload = {'Stream': data.current_stream, 'Title': data.title, 'Type': "Live",'Seek':data.seek}
        elif data.current_stream == "https://statconferencecusat.co.in/media/isbis.mp4":
            payload = {'Stream': "https://statconferencecusat.co.in/media/isbis.mp4", 'Title': "Break", 'Type': "Link" , 'Seek':data.seek}
        elif data.current_stream == Stream.objects.get(track=1).live_server1:
            payload = {'Stream': Stream.objects.get(track=1).live_server1, 'Title': data.title, 'Type': "Live", 'Seek':data.seek}
        elif data.current_stream == Stream.objects.get(track=1).live_server2:
            payload = {'Stream': Stream.objects.get(track=1).live_server2, 'Title': data.title, 'Type': "Live", 'Seek':data.seek}
        else:
            payload = {'Stream':'','Title':'','Type':'Poster'}
        return Response(payload)

    @action(detail=True, methods=['post'])
    def set_stream(self, request, pk=None):
        track = request.data['track']
        stream_model = Stream.objects.get(track=track)
        if 'title' in request.data:
            title = request.data['title']
            stream_model.title = title
            stream_model.save()
        seek = request.data['seek']
        if 'type' in request.data:
            type = request.data['type']
            if type == "live":
                live_server = int(request.data['server'])
                stream_model.seek = int(seek)
                if live_server == 1:
                    stream_model.current_stream = stream_model.live_server1
                    stream_model.save()
                elif live_server == 2:
                    stream_model.current_stream = stream_model.live_server2
                    stream_model.save()
                elif live_server == 3:
                    Stream.objects.update(current_stream=Stream.objects.get(track=1).live_server1)
                elif live_server == 4:
                    Stream.objects.update(current_stream=Stream.objects.get(track=1).live_server2)
                return Response(status.HTTP_200_OK)
            elif type == "link":
                stream_model.link = request.data['link']
                stream_model.seek = int(seek)
                stream_model.current_stream = request.data['link']
                stream_model.save()
                return Response(status.HTTP_200_OK)
            elif type == "break":
                stream_model.current_stream = "https://statconferencecusat.co.in/media/isbis.mp4"
                stream_model.save()
                return Response(status.HTTP_200_OK)
            return Response(status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status.HTTP_200_OK)
