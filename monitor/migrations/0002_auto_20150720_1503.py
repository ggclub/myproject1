# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='temphein1logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 125000)),
        ),
        migrations.AddField(
            model_name='temphein2logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 126000)),
        ),
        migrations.AddField(
            model_name='tempheout1logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 126000)),
        ),
        migrations.AddField(
            model_name='tempheout2logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 126000)),
        ),
        migrations.AddField(
            model_name='temphpin1logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 127000)),
        ),
        migrations.AddField(
            model_name='temphpin2logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 127000)),
        ),
        migrations.AddField(
            model_name='temphpin3logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 128000)),
        ),
        migrations.AddField(
            model_name='temphpin4logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 129000)),
        ),
        migrations.AddField(
            model_name='temphpin5logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 129000)),
        ),
        migrations.AddField(
            model_name='temphpin6logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 130000)),
        ),
        migrations.AddField(
            model_name='temphpout1logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 127000)),
        ),
        migrations.AddField(
            model_name='temphpout2logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 128000)),
        ),
        migrations.AddField(
            model_name='temphpout3logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 128000)),
        ),
        migrations.AddField(
            model_name='temphpout4logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 129000)),
        ),
        migrations.AddField(
            model_name='temphpout5logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 130000)),
        ),
        migrations.AddField(
            model_name='temphpout6logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 3, 7, 131000)),
        ),
    ]
