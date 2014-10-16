# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('uuid', uuidfield.fields.UUIDField(primary_key=True, serialize=False, editable=False, max_length=32, blank=True, unique=True)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('informational', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-start',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('slug', models.SlugField(max_length=255, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('slug', models.SlugField(max_length=255, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, blank=True)),
                ('list', models.ForeignKey(related_name=b'services', to='stashboard.List')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=255)),
                ('default', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Statuses',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='service',
            field=models.ForeignKey(related_name=b'events', to='stashboard.Service'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.ForeignKey(related_name=b'statuses', to='stashboard.Status'),
            preserve_default=True,
        ),
    ]
