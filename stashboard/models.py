# Copyright (c) 2010 Twilio Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from datetime import timedelta
from datetime import date

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

from uuidfield import UUIDField


class List(models.Model):
    """A list to group service

    Properties:
    name        -- string: The name of this list
    description -- string: The description of the list
    slug        -- string: URL friendly version of the name
    """
    slug = models.SlugField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    __unicode__ = lambda self: self.name


class Service(models.Model):
    """A service to track

    Properties:
    name        -- string: The name of this service
    description -- string: The function of the service
    slug        -- stirng: URL friendly version of the name
    """
    slug = models.SlugField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    list = models.ForeignKey(List, related_name='services')

    __unicode__ = lambda self: self.name

    class Meta:
        ordering = ('name',)

    def history(self, days, default, start=None):
        """ Return the past n days of activity AFTER the start date.

        Arguments:
        days    -- The number of days of activity to calculate
        default -- The status to use as the base status

        Keyword Arguments
        start   -- The day to look before (defaults to today)

        This funciton is currently only used on the front page
        """
        start = start or date.today()
        ago = start - timedelta(days=days)

        events = self.events.filter(start__gte=ago, start__lt=start)

        stats = {}

        for i in range(days):
            start = start - timedelta(days=1)
            stats[start.day] = {
                "image": default.image,
                "name": default.name,
                "day": start,
                "information": False,
            }

        for event in events:
            if event.status.slug != default.slug:
                stats[event.start.day]["image"] = "icons/fugue/information.png"
                stats[event.start.day]["information"] = True
                stats[event.start.day]["name"] = "information"

        history = stats.values()
        history.sort()
        history.reverse()

        return history


class Status(models.Model):
    """A possible system status

    Properties:
    name        -- string: The friendly name of this status
    slug        -- stirng: The identifier for the status
    description -- string: The state this status represents
    image       -- string: Image in /images/status
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, primary_key=True)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    default = models.BooleanField(default=False)

    __unicode__ = lambda self: self.name

    class Meta:
        verbose_name_plural = u'Statuses'


class Event(models.Model):

    uuid = UUIDField(auto=True, primary_key=True)
    start = models.DateTimeField(auto_now_add=True)

    service = models.ForeignKey(Service, related_name="events")
    status = models.ForeignKey(Status, related_name='statuses')
    message = models.TextField()
    informational = models.BooleanField(default=False)

    class Meta:
        ordering = ('-start',)
