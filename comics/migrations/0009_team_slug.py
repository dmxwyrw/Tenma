# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-11-14 19:23
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.text import slugify

SLUG_LENGTH = 200


def add_slug_data(apps, schema_editor):
    Team = apps.get_model('comics', 'Team')
    query = Team.objects.all()
    for team in query:
        new_slug = slugify(team.name)
        team.slug = new_slug
        team.save()


def remove_slug_data(apps, schema_editor):
    Team = apps.get_model('comics', 'Team')
    Team.objects.update(slug='')


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0008_creator_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
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
            model_name='team',
            name='slug',
            field=models.SlugField(
                max_length=SLUG_LENGTH),
        ),
    ]