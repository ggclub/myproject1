# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_auto_20150805_0832'),
    ]

    operations = [
        migrations.CreateModel(
            name='CirculatingPump2Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('CPID', models.SmallIntegerField(default=2, choices=[(1, b'1'), (2, b'2')])),
                ('opMode', models.CharField(default=b'AT', max_length=2, choices=[(b'MN', b'\xec\x88\x98\xeb\x8f\x99'), (b'AT', b'\xec\x9e\x90\xeb\x8f\x99')])),
                ('switch', models.CharField(default=b'OFF', max_length=3, choices=[(b'ON', b'On'), (b'OFF', b'Off')])),
                ('Hz', models.SmallIntegerField(default=0)),
                ('flux', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.RenameModel(
            old_name='CirculatingPumpLogger',
            new_name='CirculatingPump1Logger',
        ),
    ]
