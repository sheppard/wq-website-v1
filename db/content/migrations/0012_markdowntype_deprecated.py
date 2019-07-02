# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0011_markdowntype_current'),
    ]

    operations = [
        migrations.AddField(
            model_name='markdowntype',
            name='deprecated',
            field=models.BooleanField(default=False),
        ),
    ]
