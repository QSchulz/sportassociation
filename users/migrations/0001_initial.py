# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import sorl.thumbnail.fields
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('birthdate', models.DateField(null=True, blank=True)),
                ('competition_license', models.CharField(max_length=15, blank=True)),
                ('competition_expiration', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, blank=True)),
                ('global_scope', models.PositiveSmallIntegerField(choices=[(1, 'Registered users'), (2, 'Members'), (3, 'Managers'), (4, 'Staff')], default=1, validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(1)])),
                ('id_photo', sorl.thumbnail.fields.ImageField(upload_to='protected/users/')),
                ('mail_scope', models.PositiveSmallIntegerField(choices=[(1, 'Registered users'), (2, 'Members'), (3, 'Managers'), (4, 'Staff')], default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('nickname', models.CharField(max_length=20, blank=True)),
                ('phone', models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format:                     '+999999999'. Up to 15 digits allowed.")])),
                ('phone_scope', models.PositiveSmallIntegerField(choices=[(1, 'Registered users'), (2, 'Members'), (3, 'Managers'), (4, 'Staff')], default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], max_length=2, blank=True)),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.Position', related_name='users', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'utilisateur',
                'verbose_name_plural': 'utilisateurs',
            },
        ),
    ]
