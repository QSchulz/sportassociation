# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('communication', '0002_article_author'),
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CancelledSession',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('cancellation_date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True)),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'cancelled session',
                'verbose_name_plural': 'cancelled sessions',
                'ordering': ['cancellation_date'],
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('description', models.TextField()),
                ('name', models.CharField(max_length=50)),
                ('opponent', models.CharField(max_length=30, blank=True)),
                ('result', models.CharField(max_length=50, blank=True)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.Location', related_name='matches', blank=True)),
                ('report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='communication.Article', related_name='matches', blank=True)),
            ],
            options={
                'verbose_name': 'match',
                'verbose_name_plural': 'matches',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('date', models.DateField(default=None, null=True, blank=True)),
                ('end_time', models.TimeField()),
                ('start_time', models.TimeField()),
                ('weekday', models.PositiveSmallIntegerField(choices=[(1, 'dimanche'), (2, 'lundi'), (3, 'mardi'), (4, 'mercredi'), (5, 'jeudi'), (6, 'vendredi'), (7, 'samedi')], null=True, blank=True)),
                ('location', models.ForeignKey(null=True, to='management.Location', related_name='sessions', on_delete=django.db.models.deletion.SET_NULL)),
                ('manager', models.ForeignKey(null=True, to='users.CustomUser', related_name='managed_sessions', on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'session',
                'verbose_name_plural': 'sessions',
                'ordering': ['weekday'],
            },
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('is_open', models.BooleanField(default=True)),
                ('mailing_list', models.EmailField(max_length=254, blank=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('competitors', models.ManyToManyField(to='users.CustomUser', related_name='competition_sports', blank=True)),
                ('managers', models.ManyToManyField(to='users.CustomUser', related_name='managed_sports')),
                ('participants', models.ManyToManyField(to='users.CustomUser', related_name='subscribed_sports', blank=True)),
            ],
            options={
                'verbose_name': 'sport',
                'verbose_name_plural': 'sports',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='session',
            name='sport',
            field=models.ForeignKey(to='sports.Sport', related_name='sessions'),
        ),
        migrations.AddField(
            model_name='match',
            name='sport',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sports.Sport', related_name='matches', blank=True),
        ),
        migrations.AddField(
            model_name='cancelledsession',
            name='cancelled_session',
            field=models.ForeignKey(to='sports.Session', related_name='cancelled_sessions'),
        ),
    ]
