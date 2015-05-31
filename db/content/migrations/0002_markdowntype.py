# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarkdownType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]
