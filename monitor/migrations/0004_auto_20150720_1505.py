# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20150720_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temphein1logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphein2logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='tempheout1logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='tempheout2logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphpin1logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphpin2logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphpin3logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphpin4logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphpin5logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphpin6logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphpout1logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphpout2logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphpout3logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphpout4logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphpout5logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='temphpout6logger',
            name='dateTime',
            field=models.DateTimeField(),
        ),
    ]
