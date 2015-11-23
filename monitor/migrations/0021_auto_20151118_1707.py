# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0020_auto_20151011_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dwpflowmeterlogger',
            name='currentFlux',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='dwpflowmeterlogger',
            name='integralFlux',
            field=models.FloatField(),
        ),
    ]
