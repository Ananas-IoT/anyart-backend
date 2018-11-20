from rest_framework import permissions
from django.contrib.auth.models import User

from authorization.models import UserProfile


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = User.objects.filter(id=request.auth.user_id).get()
        return obj.owner == user


class IsTokenAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.auth is not None and request.auth.key is not None


class IsArtist(permissions.BasePermission):

    def has_permission(self, request, view):
        user_profile = UserProfile.objects.filter(owner_id=request.auth.user_id).get()
        if user_profile.rights == 'artist':
            return True
        else:
            return False


class IsGovernment(permissions.BasePermission):

    def has_permission(self, request, view):
        user_profile = UserProfile.objects.filter(owner_id=request.auth.user_id).get()
        if user_profile.rights == 'gov':
            return True
        else:
            return False


class IsBasicUser(permissions.BasePermission):

    def has_permission(self, request, view):
        user_profile = UserProfile.objects.filter(owner_id=request.auth.user_id).get()
        if user_profile.rights == 'basic':
            return True
        else:
            return False


class IsBasicUserOrArtist(permissions.BasePermission):

    def has_permission(self, request, view):
        user_profile = UserProfile.objects.filter(owner_id=request.auth.user_id).get()
        if user_profile.rights in ('basic', 'artist'):
            return True
        else:
            return False


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user_profile = UserProfile.objects.filter(owner_id=request.auth.user_id).get()
        if user_profile.rights == 'admin':
            return True
        else:
            return False
