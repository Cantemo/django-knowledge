# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('knowledge', '0002_auto_20150608_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='company',
            name='external_id',
            field=models.ForeignKey(related_name='user_company', default=False, to=settings.AUTH_USER_MODEL, help_text='ID of the user that will own the company.'),
        ),
    ]
