# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0016_auto_20150920_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='tubewelllogger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 20, 15, 33, 19, 654000)),
            preserve_default=False,
        ),
    ]
