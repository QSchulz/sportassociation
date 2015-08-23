# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('content', models.TextField()),
                ('cover', sorl.thumbnail.fields.ImageField(upload_to='public/covers/activities/', null=True, blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('is_big_activity', models.BooleanField(default=False)),
                ('is_frontpage', models.BooleanField(db_index=True, default=False)),
                ('is_member_only', models.BooleanField(default=False)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('publication_date', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('slug', models.SlugField()),
                ('start_date', models.DateTimeField()),
                ('summary', models.CharField(max_length=180, blank=True)),
                ('title', models.CharField(db_index=True, max_length=50)),
                ('website', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': 'activity',
                'verbose_name_plural': 'activities',
                'ordering': ['-publication_date'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('default_price', models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.TextField(blank=True)),
                ('max_bought_items', models.PositiveSmallIntegerField(default=None, null=True, blank=True)),
                ('member_price', models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('default_price', models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.TextField(blank=True)),
                ('is_mandatory', models.BooleanField(default=False)),
                ('is_member_only', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
                ('max_bought_items', models.PositiveSmallIntegerField(default=None, null=True, blank=True)),
                ('member_price', models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'parameter',
                'verbose_name_plural': 'parameters',
                'ordering': ['creation_date'],
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('cheque_bank', models.CharField(max_length=30, blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('payment_mean', models.CharField(choices=[('cash', 'Cash'), ('cheque', 'Cheque')], max_length=6)),
                ('unregistered_user', models.CharField(null=True, max_length=30, blank=True)),
            ],
            options={
                'verbose_name': 'participant',
                'verbose_name_plural': 'participants',
                'ordering': ['registered_user', 'unregistered_user'],
            },
        ),
    ]
