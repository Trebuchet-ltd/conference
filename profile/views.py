from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .models import User
from papers.models import Paper
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from string import ascii_lowercase, ascii_uppercase, digits
import random
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from papers.permissions import IsOrgnaiser
from papers.utils import send_async_mail, send_bulk_async_mail

from talks.models import Participant, Session


@receiver(reset_password_token_created)
def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
    """
       Handles password reset tokens
       When a token is created, an e-mail needs to be sent to the user
    """

    base_url = 'https://statconferencecusat.co.in/reset/'
    link = base_url + reset_password_token.key
    user_email = reset_password_token.user.email
    user_name = reset_password_token.user.first_name
    # send an e-mail to the user
    print('Sending password reset mail to', user_email)
    send_mail(
        f'[ISBIS 2020] Password Reset',
        f'Hey {user_name}! \nClick the link below to reset your password. \n{link} ',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )


@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view()
def complete_view(request):
    return HttpResponse("Email account is activated")


class AnonPlenaryList(ListAPIView):
    queryset = User.objects.all().filter(is_plenary=True)
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get"]


class ReviewerList(ListAPIView):
    queryset = User.objects.filter(role='reviewer')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOrgnaiser]


class UserList(ListAPIView):
    queryset = User.objects.exclude(role='reviewer').exclude(role='organiser')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOrgnaiser]


class SendMail(APIView):
    def post(self, request, format=None):
        data = request.data
        subject = data['subject']
        content = data['content']
        mail_addresses = []
        content_data = []
        lst=[]
        if data['recipient'] == 'all':
            users = User.objects.all()
            for i in users:
                _name = f"{i.first_name} {i.last_name}"
                _content = content.replace('{name}', _name)
                lst.append([subject, _content, [i.email]])
            send_bulk_async_mail(lst)


        elif data['recipient'] == 'paper_all' or data['recipient'] == 'paper_acc':
            users = User.objects.all().filter(paper__isnull=False)
            if data['recipient'] == 'paper_acc':
                users = users.filter(paper__status='accepted')
            for i in users:
                _name = f"{i.first_name} {i.last_name}"
                _content = content.replace('{name}', _name)
                _content = _content.replace('{paper}', i.paper.title)
                lst.append([subject, _content, [i.email]])
            send_bulk_async_mail(lst)

        elif data['recipient'] == 'session_all':
            users = User.objects.all().filter(session_organising__isnull=False) | \
                    User.objects.all().filter(session_participating__isnull=False)
            for i in users:
                _name = f"{i.first_name} {i.last_name}"
                _content = content.replace('{name}', _name)
                lst.append([subject, _content, [i.email]])
            send_bulk_async_mail(lst)

        elif data['recipient'] == 'session_org':
            users = User.objects.all().filter(session_organising__isnull=False)
            for i in users:
                _name = f"{i.first_name} {i.last_name}"
                _content = content.replace('{name}', _name)
                _content = _content.replace('{session}', i.session_organising.title)
                lst.append([subject, _content, [i.email]])
            send_bulk_async_mail(lst)

        elif data['recipient'] == 'session_part':
            users = User.objects.all().filter(session_participating__isnull=False)
            for i in users:
                _name = f"{i.first_name} {i.last_name}"
                _content = content.replace('{name}', _name)
                _content = _content.replace('{session}', i.session_participating.session.title)
                _content = _content.replace('{participant_presentation}', i.session_participating.title)
                lst.append([subject, _content, [i.email]])
            send_bulk_async_mail(lst)

        elif data['recipient'] == 'session_part_notacc':
            participants = Participant.objects.filter(status='invited')
            for i in participants:
                _content = content.replace('{name}', i.speaker_name)
                _content = _content.replace('{session}', i.session.title)
                _content = _content.replace('{participant_presentation}', i.title)
                lst.append([subject, _content, [i.email]])
            send_bulk_async_mail(lst)

        elif data['recipient'] == 'plenary':
            users = User.objects.all().filter(is_plenary=True)
            for i in users:
                _name = f"{i.first_name} {i.last_name}"
                _content = content.replace('{name}', _name)
                lst.append([subject, _content, [i.email]])
            send_bulk_async_mail(lst)

        return Response(status.HTTP_200_OK)
