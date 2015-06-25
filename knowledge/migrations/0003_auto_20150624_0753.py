# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0002_auto_20150608_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='knowledge.Question', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='external_id',
            field=models.ForeignKey(related_name='user_company', default=False, to=settings.AUTH_USER_MODEL, help_text='ID of the user that will own the company.'),
        ),
    ]
