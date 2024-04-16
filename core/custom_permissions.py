from rest_framework import permissions
from django.conf import settings


class SafeIPsPermission(permissions.BasePermission):
    """
    Global permission to allow access to a
    dictionary of safe IPs
    """

    def has_permission(self, request, view):
        ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if ip:
            ip = ip.split(",")[-1]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip in settings.SAFE_IPS
