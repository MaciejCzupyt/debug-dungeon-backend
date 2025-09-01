from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only allow owners of an object to edit/delete it.
    Assumes the model instance has a 'user' attribute, which corresponds to the owner.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsSelfOrReadOnly(permissions.BasePermission):
    """
    Only allow users to edit themselves.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
