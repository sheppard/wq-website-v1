# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_auto_20160129_1028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='link',
            options={'ordering': ('type_id',)},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('type_id',)},
        ),
        migrations.AlterModelOptions(
            name='tagtype',
            options={'ordering': ('pk',)},
        ),
        migrations.RemoveField(
            model_name='example',
            name='app_url',
        ),
        migrations.RemoveField(
            model_name='example',
            name='home_url',
        ),
        migrations.RemoveField(
            model_name='example',
            name='repo_url',
        ),
    ]
