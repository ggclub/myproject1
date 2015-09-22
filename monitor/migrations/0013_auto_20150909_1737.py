# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0012_auto_20150909_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemperatureModeLogger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temperatureMode', models.CharField(default=b'CL', max_length=2, choices=[(b'CL', b'\xeb\x83\x89\xeb\xb0\xa9'), (b'HT', b'\xeb\x82\x9c\xeb\xb0\xa9')])),
            ],
        ),
        migrations.RenameField(
            model_name='operationmodelogger',
            old_name='operationMode',
            new_name='opMode',
        ),
        migrations.RemoveField(
            model_name='operationmodelogger',
            name='temperatureMode',
        ),
    ]
