# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-18 20:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendar', '0016_eventstreampage'),
    ]

    operations = [
        migrations.RenameField('Event', 'event_type', 'type')
    ]
