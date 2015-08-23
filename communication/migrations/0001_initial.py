# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('content', models.TextField()),
                ('cover', sorl.thumbnail.fields.ImageField(upload_to='public/covers/articles/', null=True, blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('is_frontpage', models.BooleanField(db_index=True, default=False)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('publication_date', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('slug', models.SlugField()),
                ('summary', models.CharField(null=True, max_length=180, blank=True)),
                ('title', models.CharField(db_index=True, max_length=50)),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
                'ordering': ['-publication_date'],
            },
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('is_important', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(db_index=True, default=False)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('title', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'verbose_name': 'information',
                'verbose_name_plural': 'informations',
                'ordering': ['start_date', '-end_date'],
            },
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('content', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('index', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'paragraph',
                'verbose_name_plural': 'paragraphs',
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='Weekmail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('conclusion', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('introduction', models.TextField()),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('sent_date', models.DateTimeField(db_index=True, blank=True, null=True, default=None)),
                ('subject', models.CharField(db_index=True, max_length=80)),
            ],
            options={
                'verbose_name': 'weekmail',
                'verbose_name_plural': 'weekmails',
                'ordering': ['-sent_date'],
            },
        ),
        migrations.AddField(
            model_name='paragraph',
            name='weekmail',
            field=models.ForeignKey(to='communication.Weekmail', related_name='paragraphs'),
        ),
    ]
