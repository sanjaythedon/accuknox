from rest_framework.permissions import BasePermission


class IsLoggedIn(BasePermission):
    def has_permission(self, request, view):
        if request.session.get('token'):
            return True
        return False