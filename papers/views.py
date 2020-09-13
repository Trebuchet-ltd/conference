from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *
from .permissions import *
from django.utils.timezone import now


class PaperViewset(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    # permission_classes = [
    #     permissions.IsAuthenticated & (CreateAndIsViewer | NotCreateAndIsOrgnaiser | RetrieveAndIsAuthor)]
    # TODO: Unfuck security.

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        print(serializer.validated_data)
        if serializer.validated_data['is_poster']:
            serializer.save(author_poster=self.request.user, submission_time=now(), status='submitted')
        else:
            serializer.save(author=self.request.user, submission_time=now(), status='submitted')

    def get_serializer_class(self):
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
