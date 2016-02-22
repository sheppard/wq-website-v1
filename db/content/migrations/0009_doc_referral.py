# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_auto_20160129_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='referral',
            field=models.BooleanField(default=False),
        ),
    ]
