from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'papers'
router = DefaultRouter()
router.register(r'', views.PaperViewset)

urlpatterns = [
    url('me', views.PaperList.as_view()),
    url('posters', views.PosterList.as_view()),
    path('', include(router.urls)),
]
