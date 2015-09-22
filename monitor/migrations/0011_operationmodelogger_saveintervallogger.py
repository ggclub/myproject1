# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0010_auto_20150903_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationModeLogger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('operationMode', models.CharField(default=b'AT', max_length=2, choices=[(b'MN', b'\xec\x88\x98\xeb\x8f\x99'), (b'AT', b'\xec\x9e\x90\xeb\x8f\x99')])),
                ('temperatureMode', models.CharField(default=b'AT', max_length=2, choices=[(b'CL', b'\xeb\x83\x89\xeb\xb0\xa9'), (b'HT', b'\xeb\x82\x9c\xeb\xb0\xa9')])),
            ],
        ),
        migrations.CreateModel(
            name='SaveIntervalLogger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('interval', models.SmallIntegerField(default=10)),
            ],
        ),
    ]
