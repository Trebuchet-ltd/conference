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

from talks.models import Participant , Session


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
        data = request.data
        subject = data['subject']
        content = data['content']
        mail_addresses = []
        content_data=[]
        if data['recipient']=='all':
            mail_addresses = User.objects.all().values_list('email',flat=True)
            names = list(User.objects.all().values_list('first_name',flat=True))
            print(names)
            content_data = [names]
        elif data['recipient']=='paper_all':
            mail_set = Paper.objects.all().values_list('author',flat=True)
            names = []
            paper = []
            for i in mail_set:
                x=User.objects.get(id=i).email
                mail_addresses.append(x)
                names.append(User.objects.get(id=i).first_name)
                paper.append(Paper.objects.get(author_id=i).title)
            content_data = [names,paper]
        elif data['recipient']=='paper_acc':
            mail_set = Paper.objects.filter(status='accepted').values_list('author',flat=True)
            names = []
            paper = []
            for i in mail_set:
                x=User.objects.get(id=i).email
                mail_addresses.append(x)
                names.append(User.objects.get(id=i).first_name)
                paper.append(Paper.objects.get(author_id=i).title)
            content_data = [names,paper]
        elif data['recipient']=='session_all':
            mail_set = Session.objects.all().values_list('organiser',flat=True)
            names = []
            for i in mail_set:
                x=User.objects.get(id=i).email
                mail_addresses.append(x)
                names.append(User.objects.get(id=i).first_name)
            for j in Participant.objects.all().values_list('email',flat=True):
                mail_addresses.append(j)
            for j in Participant.objects.all().values_list('speaker_name', flat=True):
                names.append(j)
            content_data = [names]
        elif data['recipient']=='session_org':
            mail_set = Session.objects.all().values_list('organiser',flat=True)
            names = []
            for i in mail_set:
                x=User.objects.get(id=i).email
                mail_addresses.append(x)
                names.append(User.objects.get(id=i).first_name)
            session_set = list(Session.objects.all().values_list('title',flat=True))
            content_data = [names,session_set]

        elif data['recipient']=='session_part':
            names = Participant.objects.all().values_list('speaker_name',flat=True)
            for j in Participant.objects.all().values_list('email',flat=True):
                mail_addresses.append(j)

            session_set = Participant.objects.all().values_list('session',flat=True)
            session = []
            for i in session_set:
                x=Session.objects.get(id=i).title
                session.append(x)
            title = Participant.objects.all().values_list('title',flat=True)
            content_data = [names,session,title]
        elif data['recipient']=='session_part_notacc':
            names = Participant.objects.filter(status='invited').values_list('speaker_name',flat=True)
            for j in Participant.objects.filter(status='invited').values_list('email',flat=True):
                mail_addresses.append(j)

            session_set = Participant.objects.filter(status='invited').values_list('session',flat=True)
            session = []
            for i in session_set:
                x=Session.objects.get(id=i).title
                session.append(x)
            title = list(Participant.objects.filter(status='invited').values_list('title',flat=True))
            content_data = [names,session,title]
        mail_addresses=list(set(mail_addresses))
        print(mail_addresses)

        og_content = content
        if mail_addresses!=[]:
            for i in range(len(mail_addresses)):
                if data['recipient']=='all':
                    content = og_content.replace('{name}',content_data[0][i])
                elif data['recipient']=='paper_all':
                    content = og_content.replace('{name}',content_data[0][i])
                    content = content.replace('{paper}',content_data[1][i])
                elif data['recipient']=='paper_acc':
                    content = og_content.replace('{name}',content_data[0][i])
                    content = content.replace('{paper}',content_data[1][i])
                elif data['recipient']=='session_all':
                    content = og_content.replace('{name}',content_data[0][i])
                elif data['recipient'] == 'session_org':
                    content = og_content.replace('{name}', content_data[0][i])
                    content = content.replace('{session}', content_data[1][i])
                elif data['recipient'] == 'session_part':
                    content = og_content.replace('{name}', content_data[0][i])
                    content = content.replace('{session}', content_data[1][i])
                    content = content.replace('{participant_presentation}' , content_data[2][i])
                elif data['recipient'] == 'session_part_notacc':
                    content = og_content.replace('{name}', content_data[0][i])
                    content = content.replace('{session}', content_data[1][i])
                    content = content.replace('{participant_presentation}', content_data[2][i])
                send_async_mail(subject,content,mail_addresses[i])
                print(content)
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)