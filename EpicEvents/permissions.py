from rest_framework.permissions import BasePermission
from .models import User


class ClientsPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return False
        if view.action == 'create':
            return User.objects.filter(groups__name='sales_group').filter(id=request.user.id).exists()
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        return obj.sales_contact == request.user


class ContractsPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return False
        if view.action == 'create':
            return User.objects.filter(groups__name='sales_group').filter(id=request.user.id).exists()
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        return obj.sales_contact == request.user


class EventsPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return False
        if view.action == 'create':
            return User.objects.filter(groups__name='sales_group').filter(id=request.user.id).exists()
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        return obj.event_status.sales_contact == request.user or obj.support_contact == request.user
