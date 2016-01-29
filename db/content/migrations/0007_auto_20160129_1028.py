# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_doc_indent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('url', models.URLField()),
                ('example', models.ForeignKey(to='content.Example')),
            ],
        ),
        migrations.CreateModel(
            name='LinkType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='icons')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TagType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='type',
            field=models.ForeignKey(to='content.TagType'),
        ),
        migrations.AddField(
            model_name='link',
            name='type',
            field=models.ForeignKey(to='content.LinkType'),
        ),
        migrations.AddField(
            model_name='example',
            name='tags',
            field=models.ManyToManyField(to='content.Tag'),
        ),
    ]
