# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidature',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('speech', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'candidature',
                'verbose_name_plural': 'candidatures',
            },
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('description', models.TextField()),
                ('end_date', models.DateTimeField()),
                ('is_published', models.BooleanField(default=False)),
                ('slug', models.SlugField()),
                ('start_date', models.DateTimeField()),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'election',
                'verbose_name_plural': 'elections',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='VacantPosition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('elected_number', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name': 'vacant position',
                'verbose_name_plural': 'vacant positions',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('candidature', models.ForeignKey(to='elections.Candidature', related_name='votes')),
            ],
            options={
                'verbose_name': 'vote',
                'verbose_name_plural': 'votes',
            },
        ),
    ]
