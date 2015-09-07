# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_alarmlogger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarmlogger',
            name='state',
            field=models.CharField(default=b'NA', max_length=2, choices=[(b'HT', b'\xea\xb3\xa0\xec\x98\xa8'), (b'LT', b'\xec\xa0\x80\xec\x98\xa8'), (b'HF', b'\xec\x9c\xa0\xeb\x9f\x89 \xea\xb3\xbc\xeb\x8b\xa4'), (b'LF', b'\xec\x9c\xa0\xeb\x9f\x89 \xeb\xb6\x80\xec\xa1\xb1'), (b'LL', b'\xec\x88\x98\xec\x9c\x84 \xeb\xb6\x80\xec\xa1\xb1'), (b'HP', b'\xea\xb3\xbc\xec\xa0\x84\xeb\xa0\xa5'), (b'NA', b'\xed\x95\xb4\xeb\x8b\xb9 \xec\x97\x86\xec\x9d\x8c')]),
        ),
    ]
