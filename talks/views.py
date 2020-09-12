from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from profile.models import User
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']

    def get_serializer_class(self):
        if self.action == 'list':
            return ParticipantSerializer
        return BaseParticipantSerializer

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
        send_mail(
            f'Session Invitation',
            f'Hey {name}! \n {session.organiser} has invited you to be part of the session, "{session.title}". '
            f'Click the link below to confirm you participation in the session.',
            settings.EMAIL_HOST_USER,
            [serializer.validated_data['email']],
            fail_silently=False,
        )
        serializer.save()


@api_view(['GET'])
def accept_invitation(request, participant_id):
    """
    View for a user to accept a session invite.
    """
    print(request.user, participant_id)
    try:
        participant = Participant.objects.get(pk=participant_id)
        print(request.user.email, participant.email)
        if request.user.email != participant.email:
            # TODO: Handle PermissionDeniedError
            print('User not invited.')
        participant.status = 'accepted'
        participant.speaker = request.user
        participant.save()
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data)
    except Participant.DoesNotExist as e:
        print('The participant id is invalid.')
        # TODO: Handle InvalidLinkError
    return HttpResponse(str(request.user) + ' ' + str(participant_id))


@api_view(['POST'])
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
                # TODO: Add the required fields.
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

    # TODO: Send Invite Mail. Create Notification.
    send_mail(
        f'Session Invitation',
        f'Hello , \n {session.organiser} has invited you to be part of the session, "{session.title}". '
        f'Click the link below to confirm you participation in the session.'
        f'https://isbis.trebuchet.one/profile',
        settings.EMAIL_HOST_USER,
        participant_emails,
        fail_silently=False,
    )
    serializer = SessionSerializer(session)
    print(serializer.data)
    return Response(serializer.data)
