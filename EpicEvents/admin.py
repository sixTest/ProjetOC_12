from django.contrib import admin
from .models import Client, Contract, Event, User


class ClientAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if request.user.is_superuser or \
                User.objects.filter(groups__name='support_group').filter(id=request.user.id).exists():
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return obj.sales_contact == request.user
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        if obj:
            return obj.sales_contact == request.user
        return True

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name']
        return ['sales_contact']

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ClientAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if kwargs['request'].user.is_superuser and db_field.name == 'sales_contact':
            field.queryset = User.objects.filter(groups__name='sales_group')
        return field

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            for contract in Contract.objects.filter(client=obj.id):
                contract.sales_contact = User.objects.filter(id=form.data['sales_contact']).first()
                contract.save()
        else:
            obj.sales_contact = request.user
        obj.save()


class ContractAdmin(admin.ModelAdmin):

    readonly_fields = ['sales_contact']

    def has_add_permission(self, request):
        if request.user.is_superuser or \
                User.objects.filter(groups__name='support_group').filter(id=request.user.id).exists():
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        if obj:
            return obj.sales_contact == request.user
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        if obj:
            return obj.sales_contact == request.user
        return True

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ContractAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'client':
            field.queryset = field.queryset.filter(sales_contact__id=kwargs['request'].user.id)
        return field

    def save_model(self, request, obj, form, change):
        obj.sales_contact = request.user
        obj.save()


class EventAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if request.user.is_superuser or \
                User.objects.filter(groups__name='support_group').filter(id=request.user.id).exists():
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        if obj:
            return obj.support_contact == request.user or obj.client.sales_contact == request.user
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        if obj:
            return obj.support_contact == request.user or obj.client.sales_contact == request.user
        return True

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(EventAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if User.objects.filter(groups__name='support_group').filter(id=kwargs['request'].user.id).exists():
            if db_field.name == 'client':
                field.queryset = Client.objects.filter(id=self.get_queryset(kwargs['request']).first().client.id)
            if db_field.name == 'event_status':
                field.queryset = Contract.objects.filter(id=self.get_queryset(kwargs['request']).first().event_status.id)
        else:
            if db_field.name == 'client':
                field.queryset = Client.objects.filter(sales_contact__id=kwargs['request'].user.id)
            if db_field.name == 'event_status':
                field.queryset = Contract.objects.filter(sales_contact__id=kwargs['request'].user.id)
        if db_field.name == 'support_contact':
            field.queryset = User.objects.filter(groups__name='support_group')
        return field


admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)

