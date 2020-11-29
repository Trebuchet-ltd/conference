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
    path('', include(router.urls)),
    path('chunked_upload_complete/', views.MyChunkedUploadCompleteView.as_view(), name='api_chunked_upload_complete'),
    path('chunked_upload/', views.MyChunkedUploadView.as_view(), name='api_chunked_upload'),
]
