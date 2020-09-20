from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ParseError
from .models import *
from .serializers import *
from .permissions import *
from profile.models import *
from django.utils.timezone import now

ACCEPTED_ABSTRACT_FILE_TYPES = ['application/pdf']


class PaperViewset(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

    # permission_classes = [
    #     permissions.IsAuthenticated & (CreateAndIsViewer | NotCreateAndIsOrgnaiser | RetrieveAndIsAuthor)]
    # TODO: Unfuck security.

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_update(self, serializer):
        if 'abstract' in serializer.validated_data:
            if serializer.validated_data['abstract'].content_type not in ACCEPTED_ABSTRACT_FILE_TYPES:
                print(serializer.validated_data['abstract'].content_type)
                raise serializers.ValidationError(
                    'Filetype not supported. Supported types are: ' + str(ACCEPTED_ABSTRACT_FILE_TYPES))
        if 'file' in serializer.validated_data:
            if serializer.validated_data['file'].content_type not in ACCEPTED_ABSTRACT_FILE_TYPES:
                print(serializer.validated_data['file'].content_type)
                raise serializers.ValidationError(
                    'Filetype not supported. Supported types are: ' + str(ACCEPTED_ABSTRACT_FILE_TYPES))
        serializer.save()

    def perform_create(self, serializer):
        print(serializer.validated_data)
        if 'abstract' in serializer.validated_data:
            if serializer.validated_data['abstract'].content_type not in ACCEPTED_ABSTRACT_FILE_TYPES:
                print(serializer.validated_data['abstract'].content_type)
                raise serializers.ValidationError(
                    'Filetype not supported. Supported types are: ' + str(ACCEPTED_ABSTRACT_FILE_TYPES))
        if 'file' in serializer.validated_data:
            if serializer.validated_data['file'].content_type not in ACCEPTED_ABSTRACT_FILE_TYPES:
                print(serializer.validated_data['file'].content_type)
                raise serializers.ValidationError(
                    'Filetype not supported. Supported types are: ' + str(ACCEPTED_ABSTRACT_FILE_TYPES))
        serializer.save()
        if serializer.validated_data['is_poster']:
            serializer.save(author_poster=self.request.user, submission_time=now(), status='submitted')
        else:
            serializer.save(author=self.request.user, submission_time=now(), status='submitted')

    def get_serializer_class(self):
        print(self.request.user.role)
        if self.request.user.role == 'organiser':
            return OrganiserPaperSerializer
        elif self.request.user.role == 'reviewer':
            return ReviewerPaperSerializer
        elif self.action == 'update':
            return FileUploadPaperSerializer
        return PaperSerializer


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
        print(request.data['reviewer'])
        paper.reviewer = User.objects.get(pk=request.data['reviewer'])
        paper.status = 'reviewing'
        paper.save()
        serializer = PaperSerializer(paper)
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
        if status not in ['approved', 'rejected', 'corrections', 'upload paper']:
            raise ParseError(f'Cannot set status to {status}')
        paper.status = status
        paper.save()
        serializer = PaperSerializer(paper)
        return Response(serializer.data)
    except Paper.DoesNotExist as e:
        print(e)
        print('Paper id', request.data['paper'])
        return Response("Paper with this id does not exist.")
