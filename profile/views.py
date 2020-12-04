from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .models import User
from papers.models import Paper
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
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
from papers.utils import send_async_mail


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


class ReviewerList(ListAPIView):
    queryset = User.objects.filter(role='reviewer')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOrgnaiser]


class UserList(ListAPIView):
    queryset = User.objects.exclude(role='reviewer').exclude(role='organiser')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOrgnaiser]

class SendMail(APIView):
    def post(self,request,format=None):
        mail_addresses = Paper.objects.all().values_list('author', flat=True)
        print(mail_addresses)
        data = request.data
        mail_addresses = []
        if data['recipient']=='all':
            mail_addresses = User.objects.all().values_list('email',flat=True)
        elif data['recipient']=='paper_all':
            mail_addresses = Paper.objects.all().values_list('User.email',flat=True)
        print(mail_addresses)
        return Response(status.HTTP_200_OK)
