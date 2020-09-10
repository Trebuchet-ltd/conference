from rest_framework import permissions

# class IsViewer(permissions.BasePermission):
#     message = 'Not viewer'
#
#     def has_permission(self, request, view):
#         return request.user.role == 'viewer'