# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20150823_1739'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adminfile',
            options={'ordering': ['-creation_date']},
        ),
        migrations.AlterModelOptions(
            name='adminimage',
            options={'ordering': ['-creation_date']},
        ),
        migrations.AlterModelOptions(
            name='protectedfile',
            options={'ordering': ['-creation_date']},
        ),
        migrations.AlterModelOptions(
            name='protectedimage',
            options={'ordering': ['-creation_date']},
        ),
        migrations.AlterModelOptions(
            name='publicfile',
            options={'ordering': ['-creation_date']},
        ),
        migrations.AlterModelOptions(
            name='publicimage',
            options={'ordering': ['-creation_date']},
        ),
        migrations.AddField(
            model_name='permanence',
            name='location',
            field=models.ForeignKey(default=1, to='management.Location', related_name='permanences'),
            preserve_default=False,
        ),
    ]
