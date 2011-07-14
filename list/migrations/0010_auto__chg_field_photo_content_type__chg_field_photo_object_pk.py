# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Photo.content_type'
        db.alter_column('list_photo', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['contenttypes.ContentType']))

        # Changing field 'Photo.object_pk'
        db.alter_column('list_photo', 'object_pk', self.gf('django.db.models.fields.TextField')(null=True, blank=True))


    def backwards(self, orm):
        
        # Changing field 'Photo.content_type'
        db.alter_column('list_photo', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))

        # Changing field 'Photo.object_pk'
        db.alter_column('list_photo', 'object_pk', self.gf('django.db.models.fields.TextField')())


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cities.city': {
            'Meta': {'object_name': 'City'},
            'centre_of_town': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'chinese_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'list.commoninfo': {
            'Meta': {'object_name': 'CommonInfo'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cities.City']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['list.Laowai']", 'null': 'True'})
        },
        'list.info': {
            'Meta': {'object_name': 'Info'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['list.Laowai']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cities.City']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'list.laowai': {
            'Meta': {'object_name': 'Laowai'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'watched_cities'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cities.City']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cities.City']", 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'profile_views': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'rank_points': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'subscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'list.likes': {
            'Meta': {'object_name': 'Likes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'liked': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['list.Info']"}),
            'liker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['list.Laowai']"})
        },
        'list.newinfo': {
            'Meta': {'object_name': 'NewInfo', '_ormbases': ['list.CommonInfo']},
            'commoninfo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['list.CommonInfo']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'list.photo': {
            'Meta': {'object_name': 'Photo', '_ormbases': ['list.CommonInfo']},
            'commoninfo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['list.CommonInfo']", 'unique': 'True', 'primary_key': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'content_type_set_for_photo'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'object_pk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'list.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'list.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submitted_by': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'votes': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['list']
