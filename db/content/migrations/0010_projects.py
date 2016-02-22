# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def update_contenttype(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    ctype = ContentType.objects.get(model='example')
    ctype.model = 'project'
    ctype.save()



class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_doc_referral'),
    ]

    operations = [
        migrations.RenameModel('Example', 'Project'),
        migrations.RenameField(
            model_name='link',
            old_name='example',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='screenshot',
            old_name='example',
            new_name='project',
        ),
        migrations.RunPython(update_contenttype),
    ]
