# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stashboard', '0003_auto_20141016_0546'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InternalEvent',
        ),
    ]
