# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20161221_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='page_skin',
            field=models.CharField(choices=[(' ', 'Default'), ('kids', 'Kids'), ('teens', 'Teens')], max_length=255),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='page_skin',
            field=models.CharField(choices=[(' ', 'Default'), ('kids', 'Kids'), ('teens', 'Teens')], max_length=255),
        ),
    ]