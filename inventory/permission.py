from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS):
            return True
        return bool(request.user and request.user.is_staff)


# ! this is the right way to
# ! inherit just the GET perms map rather than rewriting the entire thing


# class FullDjangoPerm(permissions.DjangoModelPermissions):
#     def __init__(self) -> None:
#         self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class CanCrudObject(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.method == 'POST' and view.request.data:
            user = request.user
            return str(user.id) == str(request.data['user'])
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm(view.get_permission_type(), obj)
