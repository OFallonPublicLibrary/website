# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 07:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.contrib.wagtailroutablepage.models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('calendar', '0006_event_page_skin'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarGridPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.wagtailcore.fields.RichTextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='event',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='occurrences', to='calendar.Event', verbose_name='event'),
        ),
    ]