# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Question'
        db.create_table('questions_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, db_index=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities.City'])),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['list.Laowai'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 7, 12, 19, 47, 35, 771147))),
            ('vote_count', self.gf('django.db.models.fields.IntegerField')(default='0')),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('questions', ['Question'])

        # Adding model 'Answer'
        db.create_table('questions_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Question'])),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['list.Laowai'])),
            ('answer', self.gf('django.db.models.fields.TextField')()),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 7, 12, 19, 47, 35, 771960))),
            ('vote_count', self.gf('django.db.models.fields.IntegerField')(default='0')),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('questions', ['Answer'])

        # Adding model 'Vote'
        db.create_table('questions_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Answer'])),
            ('laowai', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['list.Laowai'])),
        ))
        db.send_create_signal('questions', ['Vote'])


    def backwards(self, orm):
        
        # Deleting model 'Question'
        db.delete_table('questions_question')

        # Deleting model 'Answer'
        db.delete_table('questions_answer')

        # Deleting model 'Vote'
        db.delete_table('questions_vote')


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
        'questions.answer': {
            'Meta': {'object_name': 'Answer'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['list.Laowai']"}),
            'answer': ('django.db.models.fields.TextField', [], {}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 12, 19, 47, 35, 771960)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'default': "'0'"})
        },
        'questions.question': {
            'Meta': {'object_name': 'Question'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['list.Laowai']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cities.City']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 12, 19, 47, 35, 771147)'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'default': "'0'"})
        },
        'questions.vote': {
            'Meta': {'object_name': 'Vote'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Answer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laowai': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['list.Laowai']"})
        }
    }

    complete_apps = ['questions']
