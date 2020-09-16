from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from .seralizers import *

# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    def perform_create(self, serializer):
        print("Not set up yet")
