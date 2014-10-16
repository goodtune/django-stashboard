# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stashboard', '0004_delete_internalevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.AlterField(
            model_name='list',
            name='description',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
