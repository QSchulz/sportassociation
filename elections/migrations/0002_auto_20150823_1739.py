# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('elections', '0001_initial'),
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='voter',
            field=models.ForeignKey(to='users.CustomUser', related_name='votes'),
        ),
        migrations.AddField(
            model_name='vacantposition',
            name='election',
            field=models.ForeignKey(to='elections.Election', related_name='vacant_positions'),
        ),
        migrations.AddField(
            model_name='vacantposition',
            name='position',
            field=models.ForeignKey(to='management.Position', related_name='vacant_positions'),
        ),
        migrations.AddField(
            model_name='vacantposition',
            name='staying_staff',
            field=models.ManyToManyField(to='users.CustomUser', related_name='kept_positions'),
        ),
        migrations.AddField(
            model_name='candidature',
            name='candidate',
            field=models.ForeignKey(to='users.CustomUser', related_name='candidatures'),
        ),
        migrations.AddField(
            model_name='candidature',
            name='vacant_position',
            field=models.ForeignKey(to='elections.VacantPosition', related_name='candidatures'),
        ),
    ]
