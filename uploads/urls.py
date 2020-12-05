from django.urls import path

from .views import *
app_name = 'uploads'

urlpatterns = [
    path('complete/', FileChunkedUploadCompleteView.as_view(), name='api_chunked_upload_complete'),
    path('chunks/', FileChunkedUploadView.as_view(), name='api_chunked_upload'),
    path('demo/', ChunkedUploadDemo.as_view(), name='chunked_upload_test'),
]
