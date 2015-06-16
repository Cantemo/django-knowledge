# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=50, null=True, verbose_name='nickname', blank=True)),
                ('suffix', models.CharField(max_length=50, null=True, verbose_name='suffix', blank=True)),
                ('title', models.CharField(max_length=200, verbose_name='title', blank=True)),
                ('about', models.TextField(null=True, verbose_name='about', blank=True)),
                ('avatar', models.ImageField(default=b'uploads/avatars-author/default.jpg', upload_to=b'uploads/avatars-author/')),
            ],
            options={
                'ordering': ('nickname',),
                'verbose_name': 'Author',
                'verbose_name_plural': 'Author',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('lastchanged', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('nickname', models.CharField(max_length=50, null=True, verbose_name='nickname', blank=True)),
                ('about', ckeditor.fields.RichTextField(null=True, verbose_name='about', blank=True)),
                ('web_site', models.URLField(verbose_name='URL')),
                ('location', models.CharField(max_length=255)),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('is_deleted', models.BooleanField(default=False)),
                ('avatar', models.ImageField(default=b'uploads/avatars/default.jpg', upload_to=b'uploads/avatars/')),
                ('external_id', models.ForeignKey(related_name='user_company', default=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('lastchanged', models.DateTimeField(auto_now=True)),
                ('alert', models.BooleanField(default=False, help_text='Check this if you want to be alerted when a new response is added.', verbose_name='Alert')),
                ('name', models.CharField(help_text='Enter your first and last name.', max_length=64, null=True, verbose_name='Name', blank=True)),
                ('email', models.EmailField(help_text='Enter a valid email address.', max_length=254, null=True, verbose_name='Email', blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('body', ckeditor.fields.RichTextField(null=True, verbose_name='Body', blank=True)),
                ('comment', ckeditor.fields.RichTextField(null=True, verbose_name='Comment', blank=True)),
                ('status', models.CharField(default=b'review', max_length=32, verbose_name='Status', db_index=True, choices=[(b'public', 'Public'), (b'draft', 'Draft'), (b'review', 'Review'), (b'rejected', 'Rejected')])),
                ('locked', models.BooleanField(default=False)),
                ('recommended', models.BooleanField(default=False)),
                ('hits', models.PositiveIntegerField(default=0)),
                ('categories', models.ManyToManyField(to='knowledge.Category', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-added'],
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('lastchanged', models.DateTimeField(auto_now=True)),
                ('alert', models.BooleanField(default=False, help_text='Check this if you want to be alerted when a new response is added.', verbose_name='Alert')),
                ('name', models.CharField(help_text='Enter your first and last name.', max_length=64, null=True, verbose_name='Name', blank=True)),
                ('email', models.EmailField(help_text='Enter a valid email address.', max_length=254, null=True, verbose_name='Email', blank=True)),
                ('body', ckeditor.fields.RichTextField(help_text='Please enter your response.', null=True, verbose_name='Response', blank=True)),
                ('status', models.CharField(default=b'inherit', max_length=32, verbose_name='Status', db_index=True, choices=[(b'public', 'Public'), (b'draft', 'Draft'), (b'review', 'Review'), (b'rejected', 'Rejected'), (b'inherit', 'Inherit')])),
                ('accepted', models.BooleanField(default=False)),
                ('question', models.ForeignKey(related_name='responses', to='knowledge.Question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['added'],
                'verbose_name': 'Response',
                'verbose_name_plural': 'Responses',
            },
        ),
        migrations.AddField(
            model_name='author',
            name='company',
            field=models.ForeignKey(to='knowledge.Company', null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.OneToOneField(related_name='user_author', to=settings.AUTH_USER_MODEL),
        ),
    ]
