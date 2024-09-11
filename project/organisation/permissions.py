from rest_framework.permissions import BasePermission

class IsHR(BasePermission):
    """
    Custom permission to only allow users with the role `ORG_HR` to perform certain tasks.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the `ORG_HR` role
        if request.user and request.user.is_authenticated:
            return request.user.role == 'ORG_HR'
        return False