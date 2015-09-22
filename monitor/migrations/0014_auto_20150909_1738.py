# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0013_auto_20150909_1737'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temperaturemodelogger',
            old_name='temperatureMode',
            new_name='tempMode',
        ),
    ]
