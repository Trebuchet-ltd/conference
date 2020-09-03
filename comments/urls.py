from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'comments'
router = DefaultRouter()
router.register(r'', views.CommentViewset)

urlpatterns = [
    path('', include(router.urls)),
]
