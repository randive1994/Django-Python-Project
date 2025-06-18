# permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class RoleBasedAccessPermission(BasePermission):
    """
    - GET (read): all authenticated users
    - POST (create): only admin
    - PUT/PATCH (update): admin and staff
    - DELETE: only admin
    """

    def has_permission(self, request, view):
        # Allow unauthenticated access for signup in UserViewSet
        if view.basename == 'user' and request.method == 'POST':
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        method = request.method
        role = getattr(request.user, 'role', None)

        # Read access: all authenticated users
        if method in SAFE_METHODS:
            return True

        # Create: only admin
        if method == 'POST':
            return role == 'admin'

        # Update: admin or staff
        if method in ['PUT', 'PATCH']:
            return role in ['admin', 'staff']

        # Delete: only admin
        if method == 'DELETE':
            return role == 'admin'

        return False
