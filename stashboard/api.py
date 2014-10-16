from rest_framework import permissions, routers, viewsets

from .models import Event, List, Service, Status
from .serializers import (
    ServiceSerializer,
    ServiceListSerializer,
    EventSerializer,
    StatusSerializer,
)


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows services to be viewed or edited.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly,)


class ServiceListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows service lists to be viewed or edited.
    """
    queryset = List.objects.all()
    serializer_class = ServiceListSerializer
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly,)


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly,)


class StatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows statuses to be viewed or edited.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly,)


router = routers.DefaultRouter()

router.register('services', ServiceViewSet)
router.register('events', EventViewSet)
router.register('service-lists', ServiceListViewSet)
router.register('statuses', StatusViewSet)
