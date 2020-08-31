from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *


class PaperViewset(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
