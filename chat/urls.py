from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'chat'
router = DefaultRouter()
router.register(r'', views.ChatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
