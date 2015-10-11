# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0017_tubewelllogger_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='TWAB1Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('level', models.FloatField()),
                ('temp10', models.FloatField()),
                ('temp20', models.FloatField()),
                ('temp30', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TWAB2Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('level', models.FloatField()),
                ('temp10', models.FloatField()),
                ('temp20', models.FloatField()),
                ('temp30', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TWIB1Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('level', models.FloatField()),
                ('temp10', models.FloatField()),
                ('temp30', models.FloatField()),
                ('temp50', models.FloatField()),
                ('temp70', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TWIJ1Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('level', models.FloatField()),
                ('temp10', models.FloatField()),
                ('temp30', models.FloatField()),
                ('temp50', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TWSB1Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('level', models.FloatField()),
                ('temp10', models.FloatField()),
                ('temp15', models.FloatField()),
                ('temp20', models.FloatField()),
                ('temp25', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TWSB2Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('level', models.FloatField()),
                ('temp10', models.FloatField()),
                ('temp15', models.FloatField()),
                ('temp20', models.FloatField()),
                ('temp25', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='tubewelllogger',
            name='T1level',
        ),
        migrations.RemoveField(
            model_name='tubewelllogger',
            name='T1temp',
        ),
        migrations.RemoveField(
            model_name='tubewelllogger',
            name='T2level',
        ),
        migrations.RemoveField(
            model_name='tubewelllogger',
            name='T2temp',
        ),
        migrations.RemoveField(
            model_name='tubewelllogger',
            name='T3level',
        ),
        migrations.RemoveField(
            model_name='tubewelllogger',
            name='T3temp',
        ),
        migrations.RemoveField(
            model_name='tubewelllogger',
            name='T4level',
        ),
        migrations.RemoveField(
            model_name='tubewelllogger',
            name='T4temp',
        ),
        migrations.AddField(
            model_name='tubewelllogger',
            name='AB1',
            field=models.ForeignKey(default=None, blank=True, to='monitor.TWAB1Logger', null=True),
        ),
        migrations.AddField(
            model_name='tubewelllogger',
            name='AB2',
            field=models.ForeignKey(default=None, blank=True, to='monitor.TWAB2Logger', null=True),
        ),
        migrations.AddField(
            model_name='tubewelllogger',
            name='IB1',
            field=models.ForeignKey(default=None, blank=True, to='monitor.TWIB1Logger', null=True),
        ),
        migrations.AddField(
            model_name='tubewelllogger',
            name='IJ1',
            field=models.ForeignKey(default=None, blank=True, to='monitor.TWIJ1Logger', null=True),
        ),
        migrations.AddField(
            model_name='tubewelllogger',
            name='SB1',
            field=models.ForeignKey(default=None, blank=True, to='monitor.TWSB1Logger', null=True),
        ),
        migrations.AddField(
            model_name='tubewelllogger',
            name='SB2',
            field=models.ForeignKey(default=None, blank=True, to='monitor.TWSB2Logger', null=True),
        ),
    ]
