from rest_framework import permissions


def isAdminUser(request):
    return request.user and request.user.groups.filter(name="admin").exists()


def isReadRequest(request):
    return request.method in permissions.SAFE_METHODS


class MoviePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return isReadRequest(request) or isAdminUser(request)


class LikePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user and request.user == obj.user_id
