from rest_framework import serializers
from .models import Client, Contract, Event


class ClientSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Client
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'date_created',
                  'date_updated', 'sales_contact')
        extra_kwargs = {'sales_contact': {'read_only': True}, 'date_created': {'read_only': True},
                        'date_updated': {'read_only': True}}


class ContractSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Contract
        fields = ('id', 'sales_contact', 'client', 'date_created', 'date_updated', 'status', 'amount', 'payment_due')
        extra_kwargs = {'sales_contact': {'read_only': True}, 'date_created': {'read_only': True},
                        'date_updated': {'read_only': True}}


class EventSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Event
        fields = ('id', 'client', 'date_created', 'date_updated', 'support_contact', 'event_status', 'attendees',
                  'event_date', 'notes')
        extra_kwargs = {'date_created': {'read_only': True}, 'date_updated': {'read_only': True}}
