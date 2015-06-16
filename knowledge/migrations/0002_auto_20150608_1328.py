# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ('user',), 'verbose_name': 'Author', 'verbose_name_plural': 'Author'},
        ),
        migrations.RemoveField(
            model_name='author',
            name='nickname',
        ),
        migrations.RemoveField(
            model_name='author',
            name='suffix',
        ),
        migrations.AlterField(
            model_name='question',
            name='comment',
            field=models.CharField(max_length=455, null=True, verbose_name='Comment', blank=True),
        ),
    ]
