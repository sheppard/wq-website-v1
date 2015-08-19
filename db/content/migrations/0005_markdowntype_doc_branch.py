# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_auto_20150531_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='markdowntype',
            name='doc_branch',
            field=models.CharField(default='master', max_length=50),
            preserve_default=False,
        ),
    ]
