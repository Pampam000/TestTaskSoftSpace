from rest_framework import permissions as p


class NotAuthenticatedOrAdmin(p.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return not request.user.is_authenticated or request.user.is_staff


class IsOwnerAdminOrReadOnly(p.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in p.SAFE_METHODS:
            return True
        return obj == request.user or request.user.is_staff
