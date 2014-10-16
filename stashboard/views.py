# The MIT License
#
# Copyright (c) 2008 William T. Katz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

__author__ = 'Kyle Conroy'

import calendar
import datetime

from django.conf import settings
from models import Status, Service, Event
from django.views.generic import TemplateView, DetailView
from django.views.generic.dates import YearMixin, MonthMixin, DayMixin
from django.http import Http404
from django.contrib.syndication.views import Feed, add_domain
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from .forms import RSSQueryForm

RSS_NUM_EVENTS_TO_FETCH = getattr(settings, 'RSS_NUM_EVENTS_TO_FETCH', 10)
INDEX_NUM_DAYS = getattr(settings, 'INDEX_NUM_DAYS', 6)


def get_past_days(num):
    date = datetime.date.today()
    dates = []
    for i in range(1, num + 1):
        dates.append(date - datetime.timedelta(days=i))
    return dates


class RootHandler(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        services = []
        default_status = Status.objects.get(default=True)

        for service in Service.objects.all():
            try:
                event = service.events.latest('start')
            except Event.DoesNotExist:
                status = default_status
            else:
                status = event.status

            today = datetime.date.today() + datetime.timedelta(days=1)
            current, = service.history(1, default_status, start=today)
            has_issues = (current["information"] and
                          status == default_status)

            service_dict = {
                "slug": service.slug,
                "name": service.name,
                "status": status,
                "has_issues": has_issues,
                "history": service.history(INDEX_NUM_DAYS, default_status),
            }
            services.append(service_dict)

        return {
            "days": get_past_days(INDEX_NUM_DAYS),
            "statuses": Status.objects.all(),
            "services": services,
        }


class ServiceHandler(YearMixin, MonthMixin, DayMixin, DetailView):

    model = Service
    template_name = 'service.html'

    def events(self):
        try:
            year = self.get_year()
        except Http404:
            year = None

        try:
            month = self.get_month()
        except Http404:
            month = None

        try:
            day = self.get_day()
        except Http404:
            day = None

        try:
            if day:
                start_date = datetime.date(int(year), int(month), int(day))
                end_date = start_date + datetime.timedelta(days=1)
            elif month:
                start_date = datetime.date(int(year), int(month), 1)
                days = calendar.monthrange(start_date.year,
                                           start_date.month)[1]
                end_date = start_date + datetime.timedelta(days=days)
            elif year:
                start_date = datetime.date(int(year), 1, 1)
                end_date = start_date + datetime.timedelta(days=365)
            else:
                start_date = None
                end_date = None
        except ValueError, x:
            raise Http404(x)

        if start_date and end_date:
            return self.object.events.filter(start__gte=start_date,
                                             start__lt=end_date)

        return self.object.events.all()

    def get_context_data(self, **kwargs):
        context = super(ServiceHandler, self).get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["events"] = self.events()
        return context


class RSSHandler(Feed):
    """ Feed of the last settings.RSS_NUM_EVENTS_TO_FETCH events """

    def get_object(self, request, *args, **kwargs):
        return request

    def title(self, obj=None):
        current_site = Site.objects.get_current()

        data = {} if obj is None else obj.GET
        form = RSSQueryForm(data=data)
        if not form.is_valid():
            raise Http404('Form has errors.')

        services = form.cleaned_data['services']
        if services.count() == 1:
            return u'%s - %s' % (current_site.name, services[0].name)

        return current_site.name

    def description(self, obj):
        form = RSSQueryForm(data=obj.GET)
        if not form.is_valid():
            raise Http404('Form has errors.')

        service_list = list(form.cleaned_data['services'])
        service_string = 'all services'
        if len(service_list) > 0:
            if len(service_list) == 1:
                service_string = 'the %s service' % service_list[0].name
            elif len(service_list) == 2:
                service_string = 'the %s and %s services' % (
                    service_list[0].name, service_list[1].name)
            else:
                service_string = 'the %s, and %s services' % (', '.join(
                    [service.name for service in service_list[:-1]]),
                    service_list[-1].name)

        return 'This feed shows the last %d events on %s on %s.' % (
            RSS_NUM_EVENTS_TO_FETCH, service_string, self.title())

    def items(self, obj):
        form = RSSQueryForm(data=obj.GET)
        if not form.is_valid():
            raise Http404('Form has errors.')

        services = form.cleaned_data['services']
        if services:
            queryset = Event.objects.filter(
                service__in=services.values_list('pk', flat=True))
        queryset = Event.objects.all()

        return queryset[:RSS_NUM_EVENTS_TO_FETCH]

    def link(self, obj):
        form = RSSQueryForm(data=obj.GET)
        if not form.is_valid():
            raise Http404('Form has errors.')

        services = form.cleaned_data['services']
        if services.count() == 1:
            return reverse('service', kwargs={'slug': services[0].slug})

        return reverse('index')

    def item_pubdate(self, item):
        return item.start

    def item_title(self, item):
        return '%s - %s' % (item.service.name, item.status.name)

    def item_link(self, item):
        return reverse('service', kwargs={'slug': item.service.slug})

    def item_categories(self, item):
        return [item.service.slug, item.service.list.slug]

    def item_description(self, item):
        return unicode(item.message)

    def item_guid(self, item):
        current_site = Site.objects.get_current()
        link = reverse('event-detail', kwargs={'pk': item.pk})
        return add_domain(current_site.domain, link)
