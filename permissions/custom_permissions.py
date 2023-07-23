from rest_framework import permissions
from rest_framework.request import settings

class IsAdminOrReadOnly(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class CreateForMyAccount(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and request.data and view.basename == 'cart':
            return str(request.data['user']) == str(request.user.id)

        if request.method == 'POST' and request.data and view.basename == 'user-shipping-address':
            return str(request.data['user']) == str(request.user.id)

        # ? True here to allow crud http method
        return bool(request.user and request.user.is_authenticated)


class IsAuthenticatedAndIsObjectOwner(permissions.DjangoObjectPermissions):

    # ? general permission
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    # ? individual object permission level so for retrieve, put, patch, delete on a detail item
    def has_object_permission(self, request, view, obj):

        return request.user.has_perm(view.get_permission_type(), obj)


class AdminCreatePerm(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
