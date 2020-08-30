from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from PosterSub import views

app_name = 'poster'
router = DefaultRouter()
router.register(r'', views.PosterViewset)

urlpatterns = [
    path('', include(router.urls)),
]
