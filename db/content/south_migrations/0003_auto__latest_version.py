# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Page.latest_version'
        db.add_column(u'content_page', 'latest_version',
                      self.gf('django.db.models.fields.CharField')(max_length=8, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Page.latest_version'
        db.delete_column(u'content_page', 'latest_version')


    models = {
        u'content.page': {
            'Meta': {'object_name': 'Page'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_version': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'markdown': ('django.db.models.fields.TextField', [], {}),
            'submodule': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'content.paper': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Paper'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'conference': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'conference_longname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'conference_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'full_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'identify.authority': {
            'Meta': {'object_name': 'Authority', 'db_table': "'wq_identifiertype'"},
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'identify.identifier': {
            'Meta': {'object_name': 'Identifier', 'db_table': "'wq_identifier'"},
            'authority': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['identify.Authority']", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'relate.relationship': {
            'Meta': {'object_name': 'Relationship', 'db_table': "'wq_relationship'"},
            'computed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'from_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['contenttypes.ContentType']"}),
            'from_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['contenttypes.ContentType']"}),
            'to_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['relate.RelationshipType']"})
        },
        u'relate.relationshiptype': {
            'Meta': {'object_name': 'RelationshipType', 'db_table': "'wq_relationshiptype'"},
            'computed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'from_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inverse_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'to_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['contenttypes.ContentType']"})
        }
    }

    complete_apps = ['content']