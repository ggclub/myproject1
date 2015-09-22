# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0011_operationmodelogger_saveintervallogger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationmodelogger',
            name='temperatureMode',
            field=models.CharField(default=b'CL', max_length=2, choices=[(b'CL', b'\xeb\x83\x89\xeb\xb0\xa9'), (b'HT', b'\xeb\x82\x9c\xeb\xb0\xa9')]),
        ),
    ]
