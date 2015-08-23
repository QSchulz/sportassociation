# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('treasury', '0001_initial'),
        ('activities', '0001_initial'),
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='cash_register',
            field=models.ForeignKey(null=True, to='treasury.CashRegister', related_name='bought_items', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='participant',
            name='item',
            field=models.ForeignKey(to='activities.Item', related_name='participants'),
        ),
        migrations.AddField(
            model_name='participant',
            name='registered_user',
            field=models.ForeignKey(null=True, to='users.CustomUser', related_name='participations', blank=True),
        ),
        migrations.AddField(
            model_name='parameter',
            name='activity',
            field=models.ForeignKey(null=True, to='activities.Activity', related_name='parameters', blank=True),
        ),
        migrations.AddField(
            model_name='parameter',
            name='parent_parameter',
            field=models.ForeignKey(null=True, to='activities.Parameter', related_name='associated_parameters', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='parameter',
            field=models.ForeignKey(to='activities.Parameter', related_name='items'),
        ),
        migrations.AddField(
            model_name='activity',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.Location', related_name='activities', blank=True),
        ),
    ]
