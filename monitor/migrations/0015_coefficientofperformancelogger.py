# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0014_auto_20150909_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoefficientOfPerformanceLogger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('COP', models.SmallIntegerField()),
            ],
        ),
    ]
