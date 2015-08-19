# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20150531_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='markdowntype',
            name='app_branch',
            field=models.CharField(max_length=50, default='0.0'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='markdowntype',
            name='io_branch',
            field=models.CharField(max_length=50, default='0.0'),
            preserve_default=False,
        ),
    ]
