# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_markdowntype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='markdowntype',
            old_name='branch',
            new_name='db_branch',
        ),
    ]
