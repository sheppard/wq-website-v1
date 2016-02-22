# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0010_projects'),
    ]

    operations = [
        migrations.AddField(
            model_name='markdowntype',
            name='current',
            field=models.BooleanField(default=False),
        ),
    ]
