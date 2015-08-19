# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_markdowntype_doc_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='indent',
            field=models.BooleanField(default=False),
        ),
    ]
