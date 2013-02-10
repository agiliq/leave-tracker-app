# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Leave'
        db.create_table('leave_tracker_leave', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type_of_leave', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('number_fo_days', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
        ))
        db.send_create_signal('leave_tracker', ['Leave'])

        # Adding model 'UserProfile'
        db.create_table('leave_tracker_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('leaves_taken', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=10)),
            ('total_leaves', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=10)),
        ))
        db.send_create_signal('leave_tracker', ['UserProfile'])

        # Adding model 'LeaveApplication'
        db.create_table('leave_tracker_leaveapplication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('usr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leave_tracker.UserProfile'])),
            ('leave', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leave_tracker.Leave'])),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('subject', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('leave_tracker', ['LeaveApplication'])


    def backwards(self, orm):
        # Deleting model 'Leave'
        db.delete_table('leave_tracker_leave')

        # Deleting model 'UserProfile'
        db.delete_table('leave_tracker_userprofile')

        # Deleting model 'LeaveApplication'
        db.delete_table('leave_tracker_leaveapplication')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'leave_tracker.leave': {
            'Meta': {'object_name': 'Leave'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_fo_days': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'type_of_leave': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'leave_tracker.leaveapplication': {
            'Meta': {'object_name': 'LeaveApplication'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['leave_tracker.Leave']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.TextField', [], {}),
            'usr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['leave_tracker.UserProfile']"})
        },
        'leave_tracker.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leaves_taken': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'total_leaves': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['leave_tracker']