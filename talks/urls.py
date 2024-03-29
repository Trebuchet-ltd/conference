from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'talks'
router = DefaultRouter()
router.register(r'sessions', views.SessionViewSet)
router.register(r'participants', views.ParticipantViewSet)
router.register(r'programs', views.ProgramViewSet)

urlpatterns = [
    path('accept/<int:participant_id>', views.accept_invitation, name='accept'),
    path('create/', views.create_session, name='create'),
    path('status/', views.change_session_status, name='change_session_status'),
    path('session_anon/', views.SessionList.as_view(), name='session_anonymous'),
    path('', include(router.urls)),
]
