# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar', '0010_remove_calendargridpage_event_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrence',
            name='display_name_override',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]