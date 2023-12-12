from rest_framework import permissions


def isAdminUser(request):
    return request.user and request.user.groups.filter(name="admin").exists()


def isReadRequest(request):
    return request.method in permissions.SAFE_METHODS


class MoviePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return isReadRequest(request) or isAdminUser(request)
