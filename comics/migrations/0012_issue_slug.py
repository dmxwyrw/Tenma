# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-11-14 20:20
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.text import slugify

SLUG_LENGTH = 200


def add_slug_data(apps, schema_editor):
    Issue = apps.get_model('comics', 'Issue')
    query = Issue.objects.all()
    for issue in query:
        if issue.date is not None:
            slugy = issue.series.name + ' ' + \
                issue.number + ' ' + str(issue.date.year)
        else:
            slugy = issue.series + ' ' + issue.number

        new_slug = slugify(slugy)
        issue.slug = new_slug
        issue.save()


def remove_slug_data(apps, schema_editor):
    Issue = apps.get_model('comics', 'Issue')
    Issue.objects.update(slug='')


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0011_storyarc_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
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
            model_name='issue',
            name='slug',
            field=models.SlugField(
                max_length=SLUG_LENGTH),
        ),
    ]
