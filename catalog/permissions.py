from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = "Недостатньо прав. Ця дія доступна лише адміністраторам."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        profile = getattr(request.user, "profile", None)
        return profile is not None and profile.role == "admin"