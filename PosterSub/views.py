from django.shortcuts import render, redirect
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *


class PosterViewset(viewsets.ModelViewSet):
    queryset = Poster.objects.all()
    serializer_class = PosterSerializer

    def perform_create(self, serializer):
        serializer.save()
