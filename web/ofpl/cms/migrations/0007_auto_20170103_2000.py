# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-04 02:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_hours'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Hours',
            new_name='HoursList',
        ),
    ]
