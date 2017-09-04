# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercicio',
            name='inativo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='grupo',
            name='inativo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lista',
            name='inativo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lista',
            name='submeter',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='lista',
            name='ver',
            field=models.BooleanField(default=True),
        ),
    ]
