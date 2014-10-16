# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stashboard', '0002_auto_20141016_0540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='id',
        ),
        migrations.RemoveField(
            model_name='status',
            name='id',
        ),
        migrations.AlterField(
            model_name='service',
            name='slug',
            field=models.SlugField(max_length=255, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='slug',
            field=models.SlugField(max_length=255, serialize=False, primary_key=True),
        ),
    ]
