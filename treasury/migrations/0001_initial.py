# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashRegister',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'cash register',
                'verbose_name_plural': 'cash registers',
                'ordering': ['creation_date'],
            },
        ),
        migrations.CreateModel(
            name='FinancialOperation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('amount', models.DecimalField(max_digits=8, decimal_places=2)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('processed_date', models.DateField(null=True, blank=True)),
                ('unregistered_user', models.CharField(max_length=50, blank=True)),
                ('registered_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.CustomUser', related_name='financial_operations', blank=True)),
                ('related_activity', models.ForeignKey(null=True, to='activities.Activity', related_name='financial_operations', blank=True)),
            ],
            options={
                'verbose_name': 'financial operation',
                'verbose_name_plural': 'financial operations',
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='TreasuryOperation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('amount', models.DecimalField(max_digits=8, decimal_places=2)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('cash_register', models.ForeignKey(to='treasury.CashRegister', related_name='treasury_operations')),
            ],
            options={
                'verbose_name': 'treasury operation',
                'verbose_name_plural': 'treasury operations',
                'ordering': ['-creation_date'],
            },
        ),
    ]
