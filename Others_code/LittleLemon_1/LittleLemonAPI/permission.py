from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

class IsManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        is_manager = user.groups.filter(name__iexact = 'manager').exists()
        if user.is_authenticated and is_manager:
            return True
        else:
            return False
class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        is_crew = user.groups.filter(name__iexact = 'delivery crew').exists()
        if user.is_authenticated and is_crew:
            return True
        else:
            return False