from rest_framework import permissions

from django.conf import settings
from django.contrib.sites.models import Site
from .models import Paper


class IsViewer(permissions.BasePermission):
    message = 'Not viewer'

    def has_permission(self, request, view):
        return request.user.role == 'viewer'


class IsReviewer(permissions.BasePermission):
    message = 'You do not have Reviewer privilege.'

    def has_permission(self, request, view):
        return request.user.role == 'reviewer'


class IsOrgnaiser(permissions.BasePermission):
    message = 'You do not have Organiser privilege.'

    def has_permission(self, request, view):
        return request.user.role == 'organiser'
