from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'sessions'
router = DefaultRouter()
router.register(r'', views.SessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
