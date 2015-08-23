# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
        ('treasury', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='cash_register',
            field=models.ForeignKey(null=True, to='treasury.CashRegister', related_name='memberships', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='membership',
            name='member',
            field=models.ForeignKey(to='users.CustomUser', related_name='membership_history'),
        ),
        migrations.AddField(
            model_name='membership',
            name='membership_type',
            field=models.ForeignKey(null=True, to='management.MembershipType', related_name='memberships', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='lending',
            name='borrower',
            field=models.ForeignKey(to='users.CustomUser', related_name='lendings'),
        ),
        migrations.AddField(
            model_name='lending',
            name='equipment',
            field=models.ForeignKey(to='management.Equipment', related_name='lendings'),
        ),
        migrations.AddField(
            model_name='adminimage',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='adminfile',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
    ]
