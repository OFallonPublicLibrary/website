# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-04 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_alert'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='show',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
