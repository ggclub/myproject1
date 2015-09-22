# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0015_coefficientofperformancelogger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coefficientofperformancelogger',
            name='COP',
            field=models.FloatField(),
        ),
    ]
