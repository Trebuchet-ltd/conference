from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('',views.PaymentViewSet.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)