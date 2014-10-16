from .models import Event, List, Service, Status

from rest_framework import serializers


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    events = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='event-detail')

    class Meta:
        model = Service
        fields = ('name', 'description', 'list', 'events', 'url')


class ServiceListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'description', 'url', 'services')


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'name', 'description', 'image', 'default', 'url')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    timestamp = serializers.DateTimeField(source='start', read_only=True)

    class Meta:
        model = Event
        fields = ('service', 'status', 'message', 'timestamp',
                  'informational', 'url')
