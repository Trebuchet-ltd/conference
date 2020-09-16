from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'profile'

urlpatterns = [
    url('registration/complete', views.complete_view, name='account_confirm_complete'),
]
