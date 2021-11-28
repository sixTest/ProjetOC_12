from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from .models import Client, Contract, Event, User
from .permissions import ClientsPermissions, ContractsPermissions, EventsPermissions
from rest_framework import status
from .exceptions import PermissionOnClientError, UserGroupError, PermissionOnContractError, PermissionModificationError


class LoginView(APIView):

    def post(self, request, format=None):

        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class ClientsViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, ClientsPermissions]
    queryset = Client.objects.all()

    def perform_create(self, serializer):
        serializer.save(sales_contact=self.request.user)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class ContractsViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ContractsPermissions]
    queryset = Contract.objects.all()

    def perform_create(self, serializer):
        if not Client.objects.filter(id=self.request.data['client']).first().sales_contact.id == self.request.user.id:
            raise PermissionOnClientError()
        serializer.save(sales_contact=self.request.user)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class EventsViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, EventsPermissions]
    queryset = Event.objects.all()

    def perform_create(self, serializer):
        if not Client.objects.filter(id=self.request.data['client']).first().sales_contact.id == self.request.user.id:
            raise PermissionOnClientError()
        if not User.objects.filter(groups__name='support_group').filter(id=self.request.data['support_contact']).exists():
            raise UserGroupError()
        if not Contract.objects.filter(id=self.request.data['event_status']).first().sales_contact.id == self.request.user.id:
            raise PermissionOnContractError()
        serializer.save()

    def perform_update(self, serializer):
        if User.objects.filter(groups__name='support_group').filter(id=self.request.user.id).exists():
            obj = self.get_object()
            if obj.client.id != self.request.data['client'] or obj.event_status.id != self.request.data['event_status']:
                raise PermissionModificationError()
            if not User.objects.filter(groups__name='support_group').filter(id=self.request.data['support_contact']).exists():
                raise UserGroupError()
            serializer.save()
        else:
            self.perform_create(serializer)


class ClientContractsViewSet(ListModelMixin, GenericViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contract.objects.filter(client=int(self.kwargs['nested_1_pk']))


class ClientEventsViewSet(ListModelMixin, GenericViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(client=int(self.kwargs['nested_1_pk']))


class ContractEventViewSet(ListModelMixin, GenericViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(event_status=int(self.kwargs['nested_1_pk']))
