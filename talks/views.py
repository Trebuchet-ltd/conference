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
from rest_framework import serializers
from rest_framework import permissions
from rest_framework.exceptions import ParseError, PermissionDenied
from papers.utils import send_async_mail

ACCEPTED_ABSTRACT_FILE_TYPES = ['application/pdf']

MAIL_FOOTER = f'\n\nFor ant technical queries mail to : sahilathrij@gmail.com\nAnd for any queries on conference ' \
              f'organisation : asha@cusat.ac.in\n\nRegards,\nTeam ISBIS 2020\nstatconferencecusat.co.in '


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']

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
            f'Dear Sir/Ma\'am, \n {session.organiser} has invited you to be part of the session, "{session.title}". '
            f'Click the link below to confirm you participation in the session.{MAIL_FOOTER}',
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
        if str(status) == '1':
            participant.speaker = request.user
            participant.status = 'accepted'
        else:
            participant.status = 'declined'
            participant.email = None
        participant.save()
        serializer = ParticipantSerializer(participant)
        send_async_mail(
            'Session invitation accepted',
            f'Dear Sir/Ma\'am,\n\n{participant} has accepted the invitation to your session.{MAIL_FOOTER}',
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
        f'Dear Sir/Ma\'am, \n\n{session.organiser} has invited you to be speaker of the session, "{session.title}". '
        f'Kindly click the link below to confirm and register your participation in this session.'
        f'https://statconferencecusat.co.in/profile{MAIL_FOOTER}',
        participant_emails
    )

    send_async_mail(
        f'Session created successfully!',
        f'Dear Sir/Ma\'am, \n\nYour session, "{session.title}" has been created successfully.\n'
        f'Invites have been sent to the participants as per your application.{MAIL_FOOTER}',
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
        content = f'Your session, "{session.title}" has been accepted.'
        if request.data['status'] == 'rejected':
            sub = 'Session proposal rejected'
            content = f'We are sorry to inform you that your session, "{session.title}" has not been accepted to the ' \
                      f'conference. '
        content = 'Dear Sir/Ma\'am,\n\n' + content + MAIL_FOOTER
        participants = [p.email for p in session.participants.all()]
        send_async_mail(sub, content, participants)
        return Response(serializer.data)
    except Session.DoesNotExist as e:
        print(e)
        print('The Session with this id does not exist.', request.data['Session'])
        return Response("The Session with this id does not exist.")

