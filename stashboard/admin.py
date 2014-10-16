from django.contrib import admin

from .models import (
    Event,
    List,
    Service,
    Status,
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('service', 'start', 'status', 'message')
    list_filter = ('service', 'status')
    date_hierarchy = 'start'


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    list_filter = ('list',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'image', 'default')
