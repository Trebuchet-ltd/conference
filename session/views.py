from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from.serializers import *
from .permissions import *
# Create your views here.
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    # permission_classes = [permissions.IsAuthenticated]


