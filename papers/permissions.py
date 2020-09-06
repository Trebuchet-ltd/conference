from rest_framework import permissions

from django.conf import settings
from django.contrib.sites.models import Site
from .models import Paper


class IsAuthor(permissions.BasePermission):
    """
    Object-level permission to only allow authors of a paper to edit it.
    """
    message = 'You must be the author of this paper/poster.'

    def has_object_permission(self, request, view, obj):
        current_user_id = request.user.id
        return obj.author.id == current_user_id


class IsViewer(permissions.BasePermission):
    message = 'Not viewer'

    def has_permission(self, request, view):
        return request.user.role == 'viewer'


class IsReviewer(permissions.BasePermission):
    message = 'Not reviewer'

    def has_permission(self, request, view):
        return request.user.role == 'reviewer'


class IsOrgnaiser(permissions.BasePermission):
    message = 'Not Organiser'

    def has_permission(self, request, view):
        return request.user.role == 'organiser'


class NotCreateAndIsOrgnaiser(IsOrgnaiser):
    message = "!NotCreateAndIsOrgnaiser"

    def has_permission(self, request, view):
        return (view.action in ['update', 'partial_update', 'destroy', 'list', 'retrieve']
                and super(NotCreateAndIsOrgnaiser, self).has_permission(request, view))


class CreateAndIsViewer(IsViewer):
    message = "!CreateAndIsAuthenticated"

    def has_permission(self, request, view):
        print('Permissions', request.user.role, request.user.id, view.action)
        return (view.action in ['create']
                and super(CreateAndIsViewer, self).has_permission(request, view))


class RetrieveAndIsAuthor(permissions.BasePermission):
    message = "!RetrieveAndIsAuthor"

    def has_permission(self, request, view):
        is_author = False
        if view.action in ['retrieve', 'destroy', 'update']:
            try:
                is_author = Paper.objects.get(pk=view.kwargs['pk']).author.id == request.user.id
            except AttributeError:
                is_author = False
            except Paper.DoesNotExist:
                is_author = True
        return is_author
