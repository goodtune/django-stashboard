from django.conf.urls import patterns, url

from .views import (
    RootHandler,
    ServiceHandler,
)

urlpatterns = patterns(
    '',
    url(r'^$', RootHandler.as_view(), name='index'),
    url(r'^services/(?P<slug>.+)$', ServiceHandler.as_view(), name='service'),
)
