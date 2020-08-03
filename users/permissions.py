from rest_framework import permissions


class IsSelf(permissions.IsAdminUser):
    def has_object_permission(self, request, view, user):
        return bool(self.has_permission(request, view) or user == request.user)
