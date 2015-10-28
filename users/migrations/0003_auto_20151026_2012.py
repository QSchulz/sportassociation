# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_diffusion_authorisation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'utilisateur', 'verbose_name_plural': 'utilisateurs', 'ordering': ['id']},
        ),
    ]
