from django.conf.urls import include, patterns, url

from .views import (
    RootHandler,
    ServiceHandler,
    RSSHandler,
)

from .api import router

urlpatterns = patterns(
    '',
    (r'^', include('django.contrib.auth.urls')),

    url(r'^$',
        RootHandler.as_view(), name='index'),

    url(r'^services/(?P<slug>.+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$',
        ServiceHandler.as_view(), name='service-day'),
    url(r'^services/(?P<slug>.+)/(?P<year>\d+)/(?P<month>\d+)$',
        ServiceHandler.as_view(), name='service-month'),
    url(r'^services/(?P<slug>.+)/(?P<year>\d+)$',
        ServiceHandler.as_view(), name='service-year'),
    url(r'^services/(?P<slug>.+)$',
        ServiceHandler.as_view(), name='service'),

    url(r'^rss$', RSSHandler(), name='rss'),

    url(r'^api/v1/', include(router.urls)),
    url(r'^api/auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
)
