from django.urls import path, include
from .views import LoginView, ClientsViewSet, ContractsViewSet, EventsViewSet, ClientContractsViewSet, \
    ClientEventsViewSet, ContractEventViewSet
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter

router = DefaultRouter()

router.register('client', ClientsViewSet)
router.register('contract', ContractsViewSet)
router.register('event', EventsViewSet)

client_contracts_router = NestedSimpleRouter(router, 'client', 'client')
client_contracts_router.register('contracts', ClientContractsViewSet, basename='contract')

client_event_router = NestedSimpleRouter(router, 'client', 'client')
client_event_router.register('events', ClientEventsViewSet, basename='event')

contract_event_router = NestedSimpleRouter(router, 'contract', 'contract')
contract_event_router.register('event', ContractEventViewSet, basename='event')

urlpatterns = [path('login/', LoginView.as_view()),
               path('', include(router.urls)),
               path('', include(client_contracts_router.urls)),
               path('', include(client_event_router.urls)),
               path('', include(contract_event_router.urls))
]
