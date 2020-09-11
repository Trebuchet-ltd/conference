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


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']

    def perform_create(self, serializer):
        print(serializer.validated_data)
        # if 'speaker' not in serializer.validated_data:
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


def accept_invitation(request, participant_id):
    print(request.user, participant_id)
    try:
        participant = Participant.objects.get(pk=participant_id)
        print(request.user.email, participant.email)
        if request.user.email != participant.email:
            # TODO: Handle PermissionDeniedError
            print('User not invited.')

    except Participant.DoesNotExist as e:
        print('The participant id is invalid.')
        # TODO: Handle InvalidLinkError
    return HttpResponse(str(request.user) + ' ' + str(participant_id))
