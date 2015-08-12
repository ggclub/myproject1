# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20150720_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temphein1logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 565000)),
        ),
        migrations.AlterField(
            model_name='temphein2logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 566000)),
        ),
        migrations.AlterField(
            model_name='tempheout1logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 565000)),
        ),
        migrations.AlterField(
            model_name='tempheout2logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 566000)),
        ),
        migrations.AlterField(
            model_name='temphpin1logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 566000)),
        ),
        migrations.AlterField(
            model_name='temphpin2logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 567000)),
        ),
        migrations.AlterField(
            model_name='temphpin3logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 568000)),
        ),
        migrations.AlterField(
            model_name='temphpin4logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 568000)),
        ),
        migrations.AlterField(
            model_name='temphpin5logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 569000)),
        ),
        migrations.AlterField(
            model_name='temphpin6logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 570000)),
        ),
        migrations.AlterField(
            model_name='temphpout1logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 567000)),
        ),
        migrations.AlterField(
            model_name='temphpout2logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 567000)),
        ),
        migrations.AlterField(
            model_name='temphpout3logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 568000)),
        ),
        migrations.AlterField(
            model_name='temphpout4logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 569000)),
        ),
        migrations.AlterField(
            model_name='temphpout5logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 569000)),
        ),
        migrations.AlterField(
            model_name='temphpout6logger',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 4, 36, 570000)),
        ),
    ]
