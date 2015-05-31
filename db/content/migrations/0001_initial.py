# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import wq.db.contrib.files.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.CharField(serialize=False, max_length=20, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('is_jsdoc', models.BooleanField(default=False)),
                ('interactive', models.BooleanField(default=False)),
                ('incomplete', models.BooleanField(default=False)),
                ('image', models.TextField(null=True, max_length=255, blank=True)),
                ('chapter', models.ForeignKey(null=True, to='content.Chapter')),
            ],
            options={
                'ordering': ['chapter__order', '_order'],
            },
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('markdown', models.TextField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('home_url', models.CharField(null=True, max_length=255, blank=True)),
                ('repo_url', models.CharField(null=True, max_length=255, blank=True)),
                ('app_url', models.CharField(null=True, max_length=255, blank=True)),
                ('icon', models.ImageField(null=True, upload_to='icons', blank=True)),
                ('public', models.BooleanField()),
                ('developer', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('markdown', models.TextField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('submodule', models.BooleanField(default=False)),
                ('latest_version', models.CharField(null=True, max_length=8, blank=True)),
                ('version_date', models.DateField(null=True, blank=True)),
                ('showcase', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('short_title', models.CharField(max_length=40)),
                ('full_title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('abstract', models.TextField()),
                ('authors', models.CharField(max_length=255)),
                ('conference', models.CharField(max_length=255)),
                ('conference_url', models.URLField(null=True)),
                ('date', models.DateField(null=True)),
                ('conference_longname', models.CharField(max_length=255)),
                ('publisher', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='ScreenShot',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(null=True, max_length=255, blank=True)),
                ('file', wq.db.contrib.files.models.FileField(height_field='height', upload_to='.', width_field='width')),
                ('size', models.IntegerField(null=True, blank=True)),
                ('width', models.IntegerField(null=True, blank=True)),
                ('height', models.IntegerField(null=True, blank=True)),
                ('example', models.ForeignKey(to='content.Example')),
                ('type', models.ForeignKey(null=True, blank=True, to='files.FileType')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='PDF',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('files.file',),
        ),
        migrations.AlterOrderWithRespectTo(
            name='doc',
            order_with_respect_to='chapter',
        ),
    ]
