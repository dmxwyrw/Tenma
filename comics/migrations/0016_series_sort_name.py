# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-11-23 18:16
from __future__ import unicode_literals

from django.db import migrations, models


def add_sort_name_data(apps, schema_editor):
    Series = apps.get_model('comics', 'Series')
    query = Series.objects.all()
    for series in query:
        sort_name = series.name
        title_begins = sort_name.startswith('The ')
        if title_begins:
            sort_name = sort_name.replace('The ', '')
            sort_name = sort_name + ", The"
        series.sort_title=sort_name
        series.save()


def remove_sort_name_data(apps, schema_editor):
    Series = apps.get_model('comics', 'Series')
    Series.objects.update(sort_title='')


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0015_settings_directory'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='sort_title',
            field=models.CharField(max_length=200,
                                   verbose_name='Sort Name',
                                   default=''),
        ),
        migrations.RunPython(
            add_sort_name_data,
            reverse_code=remove_sort_name_data
        ),
    ]
