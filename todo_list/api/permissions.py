from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Permission for admin.'''
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)


class IsAuthorOrReadOnly(permissions.BasePermission):
    '''Permission for author.'''
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
