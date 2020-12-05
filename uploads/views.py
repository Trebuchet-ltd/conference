from chunked_upload.constants import http_status
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from chunked_upload.exceptions import ChunkedUploadError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView

from profile.models import User
from papers.models import Paper
from .models import FileChunkedUpload
from talks.models import Participant


class FileChunkedUploadView(ChunkedUploadView):
    model = FileChunkedUpload
    field_name = 'the_file'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view.cls = cls
        view.initkwargs = initkwargs
        return csrf_exempt(view)

    def check_permissions(self, request):
        try:
            auth = TokenAuthentication().authenticate(request)
            if auth is None:
                raise AuthenticationFailed
        except AuthenticationFailed as e:
            raise ChunkedUploadError(
                status=http_status.HTTP_403_FORBIDDEN,
                detail='Authentication credentials were not provided'
            )


class FileChunkedUploadCompleteView(ChunkedUploadCompleteView):
    model = FileChunkedUpload

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view.cls = cls
        view.initkwargs = initkwargs
        return csrf_exempt(view)

    def check_permissions(self, request):
        try:
            TokenAuthentication().authenticate(request)
        except AuthenticationFailed as e:
            raise ChunkedUploadError(
                status=http_status.HTTP_403_FORBIDDEN,
                detail='Authentication credentials were not provided'
            )

    def on_completion(self, uploaded_file, request):
        auth = TokenAuthentication()
        user, token = auth.authenticate(request)
        print('User:', user, user.id)

        req_type = request.POST['type']

        if req_type == 'session':
            participant = Participant.objects.get(speaker=user)
            participant.recording = uploaded_file
            participant.save()
        elif req_type == 'paper':
            paper = Paper.objects.get(author=user)
            paper.recording = uploaded_file
            paper.save()
        elif req_type == 'poster':
            paper = Paper.objects.get(author_poster=user)
            paper.recording = uploaded_file
            paper.save()

    def get_response_data(self, chunked_upload, request):
        return {'message': ("You successfully uploaded '%s' (%s bytes)!" %
                            (chunked_upload.filename, chunked_upload.offset))}


class ChunkedUploadDemo(TemplateView):
    template_name = 'chunk_uploader.html'
