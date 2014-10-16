# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stashboard', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('-start',)},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name_plural': 'Statuses'},
        ),
        migrations.RemoveField(
            model_name='list',
            name='id',
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.ForeignKey(related_name=b'statuses', to='stashboard.Status'),
        ),
        migrations.AlterField(
            model_name='list',
            name='slug',
            field=models.SlugField(max_length=255, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='list',
            field=models.ForeignKey(related_name=b'services', to='stashboard.List'),
        ),
    ]
