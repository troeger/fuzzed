# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FuzzEd', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='client_id',
            field=models.BigIntegerField(default=-2147483647),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nodegroup',
            name='client_id',
            field=models.BigIntegerField(default=-2147483647),
            preserve_default=True,
        ),
    ]
