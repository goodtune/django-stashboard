from .models import Event, List, Service, Status

from rest_framework import serializers


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SlugField(source='slug')

    class Meta:
        model = Status
        fields = ('id', 'name', 'description', 'image', 'default', 'url')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    timestamp = serializers.DateTimeField(source='start', read_only=True)
    service = serializers.SlugRelatedField(slug_field='slug')
    status = serializers.SlugRelatedField(slug_field='slug')

    class Meta:
        model = Event
        fields = ('service', 'status', 'message', 'timestamp',
                  'informational', 'url')


class NestedEventSerializer(EventSerializer):
    class Meta(EventSerializer.Meta):
        fields = ('status', 'message', 'timestamp', 'url')


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SlugField(source='slug')
    events = NestedEventSerializer(many=True, read_only=True)
    list = serializers.SlugRelatedField(slug_field='slug', required=True)

    class Meta:
        model = Service
        fields = ('id', 'name', 'description', 'list', 'events', 'url')


class NestedServiceSerializer(ServiceSerializer):
    class Meta(ServiceSerializer.Meta):
        fields = ('id', 'name', 'url')


class ServiceListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SlugField(source='slug')
    services = NestedServiceSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ('id', 'name', 'description', 'services', 'url')
