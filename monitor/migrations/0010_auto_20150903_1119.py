# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0009_auto_20150902_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarmlogger',
            name='classification',
            field=models.CharField(default=b'TP', max_length=4, choices=[(b'TP', b'\xec\x98\xa8\xeb\x8f\x84 \xec\x95\x88\xec\xa0\x84\xeb\xb2\x94\xec\x9c\x84 \xec\x9d\xb4\xed\x83\x88'), (b'FX', b'\xec\x9c\xa0\xeb\x9f\x89 \xec\x95\x88\xec\xa0\x84\xeb\xb2\x94\xec\x9c\x84 \xec\x9d\xb4\xed\x83\x88'), (b'WL', b'\xec\x88\x98\xec\x9c\x84 \xeb\xb6\x80\xec\xa1\xb1'), (b'PO', b'\xec\xa0\x84\xeb\xa0\xa5 \xec\x95\x88\xec\xa0\x84\xeb\xb2\x94\xec\x9c\x84 \xec\xb4\x88\xea\xb3\xbc'), (b'COMM', b'\xed\x86\xb5\xec\x8b\xa0 \xec\x97\x90\xeb\x9f\xac')]),
        ),
        migrations.AlterField(
            model_name='alarmlogger',
            name='state',
            field=models.CharField(default=b'NA', max_length=2, choices=[(b'HT', b'\xea\xb3\xa0\xec\x98\xa8'), (b'LT', b'\xec\xa0\x80\xec\x98\xa8'), (b'HF', b'\xec\x9c\xa0\xeb\x9f\x89 \xea\xb3\xbc\xeb\x8b\xa4'), (b'LF', b'\xec\x9c\xa0\xeb\x9f\x89 \xeb\xb6\x80\xec\xa1\xb1'), (b'LL', b'\xec\x88\x98\xec\x9c\x84 \xeb\xb6\x80\xec\xa1\xb1'), (b'HP', b'\xea\xb3\xbc\xec\xa0\x84\xeb\xa0\xa5'), (b'CE', b'\xed\x86\xb5\xec\x8b\xa0 \xec\x97\x90\xeb\x9f\xac')]),
        ),
    ]