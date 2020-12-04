from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from papers.permissions import *
from profile.models import User
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework import serializers
from rest_framework import permissions
from rest_framework.exceptions import ParseError, PermissionDenied
from papers.utils import send_async_mail
from papers.views import MAIL_FOOTER
from django.views.generic.base import TemplateView
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django.views.decorators.csrf import csrf_exempt
from .models import MyChunkedUpload
from django.utils.decorators import method_decorator
import os
import string
import random
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

ACCEPTED_ABSTRACT_FILE_TYPES = ['application/pdf']


def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# TODO: Security.
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    permission_classes = [IsAuthenticated]


class SessionList(ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SmallSessionSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'status']

    def get_serializer_class(self):
        if self.action == 'list':
            return ParticipantSerializer
        return BaseParticipantSerializer

    def perform_update(self, serializer):
        if 'abstract' in serializer.validated_data:
            if serializer.validated_data['abstract'].content_type not in ACCEPTED_ABSTRACT_FILE_TYPES:
                print(serializer.validated_data['abstract'].content_type)
                raise serializers.ValidationError(
                    'Filetype not supported. Supported types are: ' + str(ACCEPTED_ABSTRACT_FILE_TYPES))
        serializer.save()

    def perform_create(self, serializer):
        print('Hello')
        print(serializer.validated_data)
        name = ''
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
            print(user)
            name = user.first_name
        except User.DoesNotExist as e:
            print('The user is not register with the website.')
        session = serializer.validated_data['session']
        send_async_mail(
            f'Session Invitation',
            f'Dear Sir/Ma\'am, \n\n{session.organiser} has invited you to be speaker of the session, "{session.title}".'
            f' Kindly click the link below to confirm and register your participation in this session.'
            f'https://statconferencecusat.co.in/profile{MAIL_FOOTER}',
            [serializer.validated_data['email']]
        )
        serializer.save()


@api_view(['POST'])
def accept_invitation(request, participant_id):
    """
    View for a user to accept a session invite.
    """
    print(request.user, participant_id)
    try:
        participant = Participant.objects.get(pk=participant_id)
        print(request.user.email, participant.email)
        if request.user.email != participant.email:
            print('User not invited.')
            return HttpResponse("failure")
        status = request.data["status"]
        state = 'accepted'
        if str(status) == '1':
            participant.speaker = request.user
            participant.status = 'accepted'
        else:
            participant.status = 'declined'
            state = 'declined'
            participant.email = None
        participant.save()
        serializer = ParticipantSerializer(participant)
        send_async_mail(
            f'Session invitation {state}',
            f'Dear Sir/Ma\'am,\n\n{participant.speaker_name} has {state} the invitation to your session, '
            f'"{participant.session.title}".{MAIL_FOOTER}',
            [participant.session.organiser.email]
        )
        return Response(serializer.data)
    except Participant.DoesNotExist as e:
        print('The participant id is invalid.')
        return Response("Participant Id invalid")


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_session(request):
    """
    Single function to create session and participants together.
    """
    """
    {
        "title": "Sessions name",
        "description": "balch blach",
        "participants": [
            {
                "title": "JP",
                "email": "jp@mail.com"
            },
            {
                "title": "JJ",
                "email": "jjj@pmail.com"
            }
        ]
        }
    """
    session = Session(title=request.data['title'], desc=request.data['description'], organiser=request.user)
    session.save()
    participant_emails = []
    for participant_data in request.data['participants']:
        try:
            participant = Participant(
                title=participant_data['title'],
                affiliation=participant_data['affiliation'],
                email=participant_data['email'],
                speaker_name=participant_data['speaker'],
                status='invited',
                session=session
            )
            participant.save()
            participant_emails.append(participant_data['email'])
        except IntegrityError:
            print('same email')

    send_async_mail(
        f'Session Invitation',
        f'Dear Sir/Ma\'am, \n\n{session.organiser} has invited you to be a speaker in the session, “{session.title}". '
        f'Kindly visit https://statconferencecusat.co.in/profile to register and confirm your participation in this '
        f'session by clicking on the accept tab.\n\nThank you for your submission. Please visit '
        f'https://statconferencecusat.co.in for  further updates.{MAIL_FOOTER}',
        participant_emails
    )

    send_async_mail(
        f'Session created successfully!',
        f'Dear Sir/Ma\'am, \n\nYour session, "{session.title}" has been created successfully.\n'
        f'\nThank you for your submission. Please visit https://statconferencecusat.co.in for  further updates.'
        f'{MAIL_FOOTER}',
        [request.user.email]
    )

    serializer = SessionSerializer(session)
    print(serializer.data)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, IsOrgnaiser))
def change_session_status(request):
    if 'session' not in request.data or 'status' not in request.data:
        raise ParseError('Fields missing. "session" and "status" required.')
    try:
        session = Session.objects.get(pk=request.data['session'])
        session.status = request.data['status']
        session.save()
        serializer = SessionSerializer(session)
        sub = 'Session accepted'
        content = f'Your session, "{session.title}" has been accepted.\n\nInvites have been sent to all the ' \
                  f'participants. Kindly prompt them to register and accept the invitation.\n\nThank you for your ' \
                  f'submission. Please visit https://statconferencecusat.co.in for  further updates. '
        if request.data['status'] == 'rejected':
            sub = 'Session proposal rejected'
            content = f'We are sorry to inform you that your session, "{session.title}" has not been accepted to the ' \
                      f'conference. '
        content = 'Dear Sir/Ma\'am,\n\n' + content + MAIL_FOOTER
        participants = [p.email for p in session.participants.all()]
        participants.append(session.organiser.email)
        print(participants)
        send_async_mail(sub, content, participants)
        return Response(serializer.data)
    except Session.DoesNotExist as e:
        print(e)
        print('The Session with this id does not exist.', request.data['Session'])
        return Response("The Session with this id does not exist.")


class MyChunkedUploadView(ChunkedUploadView):
    model = MyChunkedUpload
    field_name = 'the_file'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        print('CSRF_Exempted.')
        return super(MyChunkedUploadView, self).dispatch(request, *args, **kwargs)

    def check_permissions(self, request):
        chunk = request.FILES.get(self.field_name)
        print(chunk)
        print(self.field_name)
        print('FILES:', request.FILES)
        print('POST:', request.POST)
        # Allow non authenticated users to make uploads
        pass


class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):
    model = MyChunkedUpload

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view.cls = cls
        view.initkwargs = initkwargs

        # Note: session based authentication is explicitly CSRF validated,
        # all other authentication is CSRF exempt.
        return csrf_exempt(view)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        print('CSRF_Exempted.')
        return super(MyChunkedUploadCompleteView, self).dispatch(request, *args, **kwargs)

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        print('Headers', request.headers)
        auth = TokenAuthentication()
        user, token = auth.authenticate(request)
        print('User:', user, user.id)
        user = User.objects.get(pk=user.id)
        user.recording = uploaded_file
        user.save()
        pass

    def get_response_data(self, chunked_upload, request):
        return {'message': ("You successfully uploaded '%s' (%s bytes)!" %
                            (chunked_upload.filename, chunked_upload.offset))}
