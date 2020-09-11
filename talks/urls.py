from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'talks'
router = DefaultRouter()
router.register(r'sessions', views.SessionViewSet)
router.register(r'participants', views.ParticipantViewSet)

urlpatterns = [
    path('accept/<int:participant_id>', views.accept_invitation, name='accept'),
    path('create', views.create_session, name='create'),
    path('', include(router.urls)),
]
