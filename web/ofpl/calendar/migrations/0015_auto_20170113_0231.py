# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-13 08:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar', '0014_occurrence_all_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='end time'),
        ),
    ]
