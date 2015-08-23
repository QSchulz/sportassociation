# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import management.models
import sorl.thumbnail.fields
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=management.models.AdminFile.custom_path)),
                ('object_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AdminImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('file', sorl.thumbnail.fields.ImageField(upload_to=management.models.AdminImage.custom_path)),
                ('object_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30)),
                ('description', models.TextField(blank=True)),
                ('quantity', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name': 'equipment',
                'verbose_name_plural': 'equipments',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Lending',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField()),
                ('returned', models.BooleanField(default=False)),
                ('deposit', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name': 'lending',
                'verbose_name_plural': 'lendings',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100, blank=True)),
                ('city', models.CharField(max_length=30, blank=True)),
                ('latitude', models.FloatField(default=None, blank=True, null=True, validators=[django.core.validators.MaxValueValidator(90), django.core.validators.MinValueValidator(0)])),
                ('longitude', models.FloatField(default=None, blank=True, null=True, validators=[django.core.validators.MaxValueValidator(180), django.core.validators.MinValueValidator(-180)])),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('expiration_date', models.DateField()),
                ('certificate_date', models.DateField()),
                ('payment_mean', models.CharField(choices=[('cash', 'Cash'), ('cheque', 'Cheque')], max_length=6)),
                ('cheque_bank', models.CharField(max_length=30, blank=True)),
                ('certificate', sorl.thumbnail.fields.ImageField(upload_to='admin/certificates', null=True, blank=True)),
                ('membership_copy', sorl.thumbnail.fields.ImageField(upload_to='admin/memberships')),
            ],
            options={
                'verbose_name': 'membership',
                'verbose_name_plural': 'memberships',
                'ordering': ['-expiration_date'],
            },
        ),
        migrations.CreateModel(
            name='MembershipType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('semester_fee', models.DecimalField(max_digits=6, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('year_fee', models.DecimalField(max_digits=6, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'membership type',
                'verbose_name_plural': 'membership types',
                'ordering': ['semester_fee'],
            },
        ),
        migrations.CreateModel(
            name='Permanence',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('weekday', models.PositiveSmallIntegerField(choices=[(1, 'dimanche'), (2, 'lundi'), (3, 'mardi'), (4, 'mercredi'), (5, 'jeudi'), (6, 'vendredi'), (7, 'samedi')], null=True, blank=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('related_activities', models.ManyToManyField(to='activities.Activity', related_name='permanences', blank=True)),
            ],
            options={
                'verbose_name': 'permanence',
                'verbose_name_plural': 'permanences',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'position',
                'verbose_name_plural': 'positions',
            },
        ),
        migrations.CreateModel(
            name='ProtectedFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=management.models.ProtectedFile.custom_path)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='ProtectedImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('file', sorl.thumbnail.fields.ImageField(upload_to=management.models.ProtectedImage.custom_path)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='PublicFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=management.models.PublicFile.custom_path)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='PublicImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('file', sorl.thumbnail.fields.ImageField(upload_to=management.models.PublicImage.custom_path)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
    ]
