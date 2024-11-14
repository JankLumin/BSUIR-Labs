from rest_framework import permissions


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == "employee"

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            "admin",
            "superadmin",
        ]

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role in [
            "admin",
            "superadmin",
        ]


class IsSuperAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "superadmin"

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == "superadmin"
