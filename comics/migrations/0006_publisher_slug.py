# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-11-14 12:22
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.text import slugify

SLUG_LENGTH = 200


def add_slug_data(apps, schema_editor):
    Publisher = apps.get_model(
        'comics', 'Publisher')
    query = Publisher.objects.all()
    for publisher in query:
        new_slug = slugify(publisher.name)
        publisher.slug = new_slug
        publisher.save()


def remove_slug_data(apps, schema_editor):
    Publisher = apps.get_model(
        'comics', 'Publisher')
    Publisher.objects.update(slug='')


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0005_issue_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='slug',
            field=models.SlugField(
                max_length=SLUG_LENGTH,
                default=''),
        ),
        migrations.RunPython(
            add_slug_data,
            reverse_code=remove_slug_data
        ),
        migrations.AlterField(
            model_name='publisher',
            name='slug',
            field=models.SlugField(
                max_length=SLUG_LENGTH,
                unique=True),
        ),
    ]
