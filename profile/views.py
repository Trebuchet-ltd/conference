import json
import os
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
from .models import User, Feedback
from papers.models import Paper
from .serializers import UserSerializer, FeedbackSerializer
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
from scripts.create_certificate import create_page
from scripts.create_paper_certificate import create_page as create_paper
from scripts.create_session_certificate import create_page as create_session
from PyPDF2 import PdfFileWriter
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
        lst = []
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


@api_view()
@permission_classes([permissions.IsAuthenticated])
def get_participation_certificate(request):
    print(request.user.id)
    if not request.user.feedback_submitted:
        return Response(status=402)
    output = PdfFileWriter()

    feedback = Feedback.objects.get(user=request.user.id)
    page = create_page(feedback.name, feedback.affiliation)

    output.addPage(page)
    # output.write(response)
    outputStream = open(os.path.join(settings.BASE_DIR, 'static/media', str(request.user.id) + 'viewer.pdf'), "wb")
    output.write(outputStream)
    return HttpResponse(json.dumps({'link': 'media/' + str(request.user.id) + 'viewer.pdf'}),
                        content_type="application/json")


@api_view()
@permission_classes([permissions.IsAuthenticated])
def get_paper_certificate(request):
    if not request.user.feedback_submitted:
        return Response(status=402)

    output = PdfFileWriter()

    feedback = Feedback.objects.get(user=request.user.id)
    page = create_paper(feedback.name, feedback.affiliation, feedback.title)

    output.addPage(page)
    outputStream = open(os.path.join(settings.BASE_DIR, 'static/media', str(request.user.id) + 'paper.pdf'), "wb")
    output.write(outputStream)
    return HttpResponse(json.dumps({'link': 'media/' + str(request.user.id) + 'paper.pdf'}),
                        content_type="application/json")


@api_view()
@permission_classes([permissions.IsAuthenticated])
def get_session_certificate(request):
    if not request.user.feedback_submitted:
        return Response(status=402)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="certificate.pdf"'
    output = PdfFileWriter()

    feedback = Feedback.objects.get(user=request.user.id)
    page = create_session(feedback.name, feedback.affiliation, feedback.session)

    output.addPage(page)
    outputStream = open(os.path.join(settings.BASE_DIR, 'static/media', str(request.user.id) + 'paper.pdf'), "wb")
    output.write(outputStream)
    return HttpResponse(json.dumps({'link': 'media/' + str(request.user.id) + 'session.pdf'}),
                        content_type="application/json")


@api_view()
@permission_classes([permissions.IsAuthenticated])
def delete_feedback(request):
    print(request.user.id)
    print(request.user)
    feedback = Feedback.objects.get(user=request.user.id)
    feedback.delete()
    request.user.feedback_submitted = False
    request.user.save()
    return Response(200)


class FeedbackViewset(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = User.objects.get(pk=serializer.validated_data['user'].id)
        user.feedback_submitted = True
        user.save()
        serializer.save()
        return Response(serializer.data)
