from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from .seralizers import *
from rest_framework.decorators import action, api_view
from rest_framework import status

# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


    @action(detail=True,methods=['get'])
    def get_notification(self,request,pk=None):
        uid=request.query_params.get('uid')
        notification_pvt = Notification.objects.filter(user_id__in=[uid,0], read=False)
        s1 = NotificationSerializer(notification_pvt.all(),many=True)
        return Response(s1.data)

    @action(detail=True,methods=['get'])
    def mark_read(self,request,pk=None):
        not_id = request.query_params.get('nid')
        notification = Notification.objects.get(id=not_id)
        notification.read=True
        notification.save()
        return Response(status.HTTP_200_OK)