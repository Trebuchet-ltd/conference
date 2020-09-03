from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save()
