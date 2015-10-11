# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0018_auto_20151010_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='AB110Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
                ('level', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='AB120Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='AB130Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='AB210Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
                ('level', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='AB220Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='AB230Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='IB110Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
                ('level', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='IB130Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='IB150Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='IB170Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='IJ110Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
                ('level', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='IJ130Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='IJ150Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SB110Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
                ('level', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SB115Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SB120Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SB125Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SB210Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
                ('level', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SB215Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SB220Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SB225Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateTime', models.DateTimeField()),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='twab1logger',
            name='level',
        ),
        migrations.RemoveField(
            model_name='twab2logger',
            name='level',
        ),
        migrations.RemoveField(
            model_name='twib1logger',
            name='level',
        ),
        migrations.RemoveField(
            model_name='twij1logger',
            name='level',
        ),
        migrations.RemoveField(
            model_name='twsb1logger',
            name='level',
        ),
        migrations.RemoveField(
            model_name='twsb2logger',
            name='level',
        ),
        migrations.AlterField(
            model_name='twab1logger',
            name='temp10',
            field=models.ForeignKey(default=None, blank=True, to='monitor.AB110Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twab1logger',
            name='temp20',
            field=models.ForeignKey(default=None, blank=True, to='monitor.AB120Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twab1logger',
            name='temp30',
            field=models.ForeignKey(default=None, blank=True, to='monitor.AB130Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twab2logger',
            name='temp10',
            field=models.ForeignKey(default=None, blank=True, to='monitor.AB210Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twab2logger',
            name='temp20',
            field=models.ForeignKey(default=None, blank=True, to='monitor.AB220Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twab2logger',
            name='temp30',
            field=models.ForeignKey(default=None, blank=True, to='monitor.AB230Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twib1logger',
            name='temp10',
            field=models.ForeignKey(default=None, blank=True, to='monitor.IB110Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twib1logger',
            name='temp30',
            field=models.ForeignKey(default=None, blank=True, to='monitor.IB130Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twib1logger',
            name='temp50',
            field=models.ForeignKey(default=None, blank=True, to='monitor.IB150Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twib1logger',
            name='temp70',
            field=models.ForeignKey(default=None, blank=True, to='monitor.IB170Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twij1logger',
            name='temp10',
            field=models.ForeignKey(default=None, blank=True, to='monitor.IJ110Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twij1logger',
            name='temp30',
            field=models.ForeignKey(default=None, blank=True, to='monitor.IJ130Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twij1logger',
            name='temp50',
            field=models.ForeignKey(default=None, blank=True, to='monitor.IJ150Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twsb1logger',
            name='temp10',
            field=models.ForeignKey(default=None, blank=True, to='monitor.SB110Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twsb1logger',
            name='temp15',
            field=models.ForeignKey(default=None, blank=True, to='monitor.SB115Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twsb1logger',
            name='temp20',
            field=models.ForeignKey(default=None, blank=True, to='monitor.SB120Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twsb1logger',
            name='temp25',
            field=models.ForeignKey(default=None, blank=True, to='monitor.SB125Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twsb2logger',
            name='temp10',
            field=models.ForeignKey(default=None, blank=True, to='monitor.SB210Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twsb2logger',
            name='temp15',
            field=models.ForeignKey(default=None, blank=True, to='monitor.SB215Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twsb2logger',
            name='temp20',
            field=models.ForeignKey(default=None, blank=True, to='monitor.SB220Logger', null=True),
        ),
        migrations.AlterField(
            model_name='twsb2logger',
            name='temp25',
            field=models.ForeignKey(default=None, blank=True, to='monitor.SB225Logger', null=True),
        ),
    ]
