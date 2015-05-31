# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Doc'
        db.create_table(u'content_doc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('markdown', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('chapter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Chapter'], null=True)),
            ('is_jsdoc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('interactive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'content', ['Doc'])

        # Adding model 'Chapter'
        db.create_table(u'content_chapter', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'content', ['Chapter'])


        # Changing field 'Example.updated'
        db.alter_column(u'content_example', 'updated', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Example.markdown'
        db.alter_column(u'content_example', 'markdown', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Example.description'
        db.alter_column(u'content_example', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Page.updated'
        db.alter_column(u'content_page', 'updated', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Page.markdown'
        db.alter_column(u'content_page', 'markdown', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Page.description'
        db.alter_column(u'content_page', 'description', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):
        # Deleting model 'Doc'
        db.delete_table(u'content_doc')

        # Deleting model 'Chapter'
        db.delete_table(u'content_chapter')


        # Changing field 'Example.updated'
        db.alter_column(u'content_example', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=None))

        # Changing field 'Example.markdown'
        db.alter_column(u'content_example', 'markdown', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Example.description'
        db.alter_column(u'content_example', 'description', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Page.updated'
        db.alter_column(u'content_page', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=None))

        # Changing field 'Page.markdown'
        db.alter_column(u'content_page', 'markdown', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Page.description'
        db.alter_column(u'content_page', 'description', self.gf('django.db.models.fields.TextField')(default=''))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'content.chapter': {
            'Meta': {'ordering': "['order']", 'object_name': 'Chapter'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'content.doc': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Doc'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Chapter']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interactive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_jsdoc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'markdown': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'content.example': {
            'Meta': {'object_name': 'Example'},
            'api_version': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'app_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'app_version': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'db_version': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'home_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'icon_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'io_version': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'markdown': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'repo_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'vera_version': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'})
        },
        u'content.page': {
            'Meta': {'object_name': 'Page'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_version': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'markdown': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'submodule': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
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