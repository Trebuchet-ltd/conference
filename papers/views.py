from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.exceptions import ParseError
from PyPDF2 import PdfFileReader, PdfFileWriter
from rest_framework.generics import ListAPIView
from django.shortcuts import render, redirect
from rest_framework.response import Response
from notification.models import Notification
from django.utils.timezone import now
from django.http import HttpResponse
from django.core.files import File
from .utils import send_async_mail
from profile.models import *
from .serializers import *
from .permissions import *
from pathlib import Path
from .models import *
import os

ACCEPTED_ABSTRACT_FILE_TYPES = ['application/pdf']

MAIL_FOOTER = f'\n\nFor any queries please contact isbis2020@gmail.com\n\nRegards,\nTeam ISBIS ' \
              f'2020\nstatconferencecusat.co.in '


class PaperViewset(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_poster', 'status']
    permission_classes = [permissions.IsAuthenticated]

    # permission_classes = [
    #     permissions.IsAuthenticated & (CreateAndIsViewer | NotCreateAndIsOrgnaiser | RetrieveAndIsAuthor)]
    # TODO: Unfuck security.

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_update(self, serializer):
        print(serializer.validated_data)
        if 'abstract' in serializer.validated_data:
            if serializer.validated_data['abstract'].content_type not in ACCEPTED_ABSTRACT_FILE_TYPES:
                print(serializer.validated_data['abstract'].content_type)
                send_async_mail(
                    f'Error in abstract submission.',
                    f'Dear Sir/Madam, \n\nYour submission was erroneous. The filetype is not supported. Supported '
                    f'filetype is pdf. Please try again with the appropriate '
                    f'filetype.\n\nKindly ignore this mail if you have already addressed this.{MAIL_FOOTER}',
                    [self.request.user.email]
                )
                raise serializers.ValidationError(
                    'Filetype not supported. Supported types are: ' + str(ACCEPTED_ABSTRACT_FILE_TYPES))
        if 'file' in serializer.validated_data:
            if serializer.validated_data['file'].content_type not in ACCEPTED_ABSTRACT_FILE_TYPES:
                print(serializer.validated_data['file'].content_type)
                send_async_mail(
                    f'Error in paper/poster submission.',
                    f'Dear Sir/Madam, \n\nYour submission was erroneous. The filetype is not supported. Supported '
                    f'filetype is pdf. Please try again with the appropriate '
                    f'filetype.\n\nKindly ignore this mail if you have already addressed this.{MAIL_FOOTER}',
                    [self.request.user.email]
                )
                raise serializers.ValidationError(
                    'Filetype not supported. Supported types are: ' + str(ACCEPTED_ABSTRACT_FILE_TYPES))
        paper = serializer.save()
        print(self.request.user.role, 'updating the paper', paper.title)
        if self.request.user.role != 'organiser':
            paper.status = 'submitted'
        paper.save()
        send_async_mail(
            f'Submission updated successfully!',
            f'Dear {self.request.user}, \n\nYour submission, "{paper.title}" has been updated '
            f'successfully.{MAIL_FOOTER}',
            [self.request.user.email]
        )
        return Response(serializer.data)

    def perform_create(self, serializer):
        print(serializer.validated_data)
        if 'abstract' in serializer.validated_data:
            if serializer.validated_data['abstract'].content_type not in ACCEPTED_ABSTRACT_FILE_TYPES:
                print(serializer.validated_data['abstract'].content_type)
                send_async_mail(
                    f'Error in abstract submission.',
                    f'Dear Sir/Madam, \n\nYour submission was erroneous. The filetype is not supported. Supported '
                    f'filetype is pdf. Please try again with the appropriate '
                    f'filetype.\n\nKindly ignore this mail if you have already addressed this.{MAIL_FOOTER}',
                    [self.request.user.email]
                )
                raise serializers.ValidationError(
                    'Filetype not supported. Supported types are: ' + str(ACCEPTED_ABSTRACT_FILE_TYPES))
        if 'file' in serializer.validated_data:
            if serializer.validated_data['file'].content_type not in ACCEPTED_ABSTRACT_FILE_TYPES:
                print(serializer.validated_data['file'].content_type)
                send_async_mail(
                    f'Error in paper/poster submission.',
                    f'Dear Sir/Madam, \n\nYour submission was erroneous. The filetype is not supported. Supported '
                    f'filetype is pdf. Please try again with the appropriate '
                    f'filetype.\n\nKindly ignore this mail if you have already addressed this.{MAIL_FOOTER}',
                    [self.request.user.email]
                )
                raise serializers.ValidationError(
                    'Filetype not supported. Supported types are: ' + str(ACCEPTED_ABSTRACT_FILE_TYPES))
        serializer.save()
        paper = 'paper'
        if serializer.validated_data['is_poster']:
            paper = 'poster'
            serializer.save(author_poster=self.request.user, submission_time=now(), status='submitted')
        else:
            serializer.save(author=self.request.user, submission_time=now(), status='submitted')

        send_async_mail(
            f'{paper.title()} submitted successfully!',
            f'Dear {self.request.user}, \n\nYour {paper}, "{serializer.validated_data["title"]}" has been submitted '
            f'successfully.{MAIL_FOOTER}',
            [self.request.user.email]
        )
        return Response(serializer.data)

    def get_serializer_class(self):
        print('Paper get_serializer_class:', self.request.user.role, self.action)
        if self.request.user.role == 'organiser':
            return OrganiserPaperSerializer
        elif self.request.user.role == 'reviewer':
            return ReviewerPaperSerializer
        elif self.action == 'update':
            print('File Upload')
            return FileUploadPaperSerializer
        return PaperSerializer


class PublicPlenarySpeakersList(ListAPIView):
    queryset = Paper.objects.filter(author__is_plenary__exact=True)
    serializer_class = SmallPaperSerializer


class AnonPaperList(ListAPIView):
    queryset = Paper.objects.all()
    serializer_class = SmallPaperSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get"]


class PaperList(ListAPIView):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(self.request.user, self.request.user.id)
        if self.request.user.role == 'reviewer':
            return Paper.objects.filter(reviewer=self.request.user.id)
        return Paper.objects.filter(author=self.request.user.id)

    def get_serializer_class(self):
        if self.request.user.role == 'reviewer':
            return ReviewerPaperSerializer
        return PaperSerializer


class PosterList(ListAPIView):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(self.request.user, self.request.user.id)
        if self.request.user.role == 'reviewer':
            return Paper.objects.filter(reviewer=self.request.user.id)
        return Paper.objects.filter(author_poster=self.request.user.id)

    def get_serializer_class(self):
        if self.request.user.role == 'reviewer':
            return ReviewerPaperSerializer
        return PaperSerializer


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, IsOrgnaiser))
def assign_paper(request):
    if 'paper' not in request.data or 'reviewer' not in request.data:
        raise ParseError('Fields missing. "paper" and "reviewer" required.')
    try:
        paper = Paper.objects.get(pk=request.data['paper'])
        reviewer = User.objects.get(pk=request.data['reviewer'])
        print(request.data['reviewer'])
        paper.reviewer = reviewer
        paper.status = 'reviewing'
        paper.save()
        serializer = PaperSerializer(paper)
        send_async_mail(
            f'Paper assigned for review.',
            f'Hello {reviewer}, \n\nThe paper, "{paper.title}" has been assigned to you for review.{MAIL_FOOTER}',
            [reviewer.email]
        )
        return Response(serializer.data)
    except Paper.DoesNotExist as e:
        print(e)
        print('The Paper with this id does not exist.', request.data['paper'])
        return Response("The Paper with this id does not exist.")


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, IsReviewer))
def review_paper(request):
    if 'paper' not in request.data:
        raise ParseError('Fields missing. "paper" required.')
    try:
        paper = Paper.objects.get(pk=request.data['paper'])
        paper.status = 'reviewed'
        paper.save()
        serializer = PaperSerializer(paper)
        return Response(serializer.data)
    except Paper.DoesNotExist as e:
        print(e)
        print('The Paper with this id does not exist.', request.data['paper'])
        return Response("The Paper with this id does not exist.")


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, IsOrgnaiser))
def change_paper_status(request):
    if 'paper' not in request.data or 'status' not in request.data:
        raise ParseError('Fields missing. "paper" and "status" required.')
    try:
        paper = Paper.objects.get(pk=request.data['paper'])
        status = request.data['status']
        if status not in ['accepted', 'rejected', 'corrections', 'upload paper']:
            raise ParseError(f'Cannot set status to {status}')
        if status == 'accepted':
            filename = str(paper.file)
            filename = filename.split('/')[-1].split('.')[0] + '_abstract.pdf'
            pdf = PdfFileReader(paper.file)
            first_page = pdf.getPage(0)
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(first_page)
            path = f'static/media/abstracts/{filename}'
            with Path(path).open(mode="wb") as output_file:
                pdf_writer.write(output_file)
            with Path(path).open(mode="rb") as input_file:
                paper.abstract.save(filename, input_file)
            os.remove(path)

        paper.status = status
        paper.save()
        serializer = PaperSerializer(paper)

        notif_content = {
            'accepted': f'Your submission, "{paper.title}" has been accepted for ISBIS 2020.',
            'rejected': f'Your submission, "{paper.title}", was not accepted to the conference ISBIS 2020.',
            'corrections': f'Your submission, "{paper.title}" has underwent review and the reviewers have asked for '
                           f'some corrections.',
            'upload paper': f'Your abstract for "{paper.title}" has been approved. Please submit the full document for '
                            f'the final approval. '
        }

        content = {
            'accepted': f'Your submission, "{paper.title}" has been accepted for presentation at the International '
                        f'Virtual Conference on Advanced Statistical Techniques in Business and Industry.\nPlease '
                        f'visit https://statconferencecusat.co.in for further updates.',
            'rejected': f'We regret to inform you that your submission, "{paper.title}", was not accepted for '
                        f'presentation at the International Virtual Conference on Advanced Statistical Techniques in '
                        f'Business and Industry.\nYou are welcome to participate in the conference.\nPlease visit '
                        f'https://statconferencecusat.co.in for further updates.\n\nThank you once again for your '
                        f'submission.',
            'corrections': f'Your submission, "{paper.title}" has undergone review and the reviewers have asked for '
                           f'some corrections. Please login to your account for the comments.posted in your '
                           f'dashboard.\nPlease visit https://statconferencecusat.co.in for  submission of revised '
                           f'paper and further updates.\n\nThank you for your submission.',
            'upload paper': f'Your abstract for "{paper.title}" has been approved. Please submit the full document for '
                            f'the final approval. '
        }
        recipient = paper.is_poster and paper.author_poster or paper.author
        body = f'Dear {recipient},\n\n' + content[status] + MAIL_FOOTER
        notification = Notification(user_id=recipient.id, text=notif_content[status])
        notification.save()
        send_async_mail(
            f'Updates on your submission to ISBIS 2020',
            body,
            [recipient.email]
        )
        return Response(serializer.data)
    except Paper.DoesNotExist as e:
        print(e)
        print('Paper id', request.data['paper'])
        return Response("Paper with this id does not exist.")
