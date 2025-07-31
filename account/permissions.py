from rest_framework.permissions import BasePermission



class Fulluser_authentication(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated



class Fulluser_isadmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated.is_admin

