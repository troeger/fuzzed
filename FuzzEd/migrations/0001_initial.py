# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Graph'
        db.create_table('FuzzEd_graph', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='graphs', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('FuzzEd', ['Graph'])

        # Adding model 'Node'
        db.create_table('FuzzEd_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client_id', self.gf('django.db.models.fields.BigIntegerField')(default=-9223372036854775807)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nodes', to=orm['FuzzEd.Graph'])),
            ('x', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('FuzzEd', ['Node'])

        # Adding model 'Edge'
        db.create_table('FuzzEd_edge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='edges', to=orm['FuzzEd.Graph'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='outgoing', to=orm['FuzzEd.Node'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='incoming', to=orm['FuzzEd.Node'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('FuzzEd', ['Edge'])

        # Adding model 'Property'
        db.create_table('FuzzEd_property', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')()),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='properties', to=orm['FuzzEd.Node'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('FuzzEd', ['Property'])

        # Adding model 'AddEdge'
        db.create_table('FuzzEd_addedge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Edge'])),
        ))
        db.send_create_signal('FuzzEd', ['AddEdge'])

        # Adding model 'AddGraph'
        db.create_table('FuzzEd_addgraph', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Graph'])),
        ))
        db.send_create_signal('FuzzEd', ['AddGraph'])

        # Adding model 'AddNode'
        db.create_table('FuzzEd_addnode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Node'])),
        ))
        db.send_create_signal('FuzzEd', ['AddNode'])

        # Adding model 'ChangeNode'
        db.create_table('FuzzEd_changenode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Node'])),
        ))
        db.send_create_signal('FuzzEd', ['ChangeNode'])

        # Adding model 'PropertyChange'
        db.create_table('FuzzEd_propertychange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('command', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changes', to=orm['FuzzEd.ChangeNode'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('old_value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('new_value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('FuzzEd', ['PropertyChange'])

        # Adding model 'DeleteEdge'
        db.create_table('FuzzEd_deleteedge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Edge'])),
        ))
        db.send_create_signal('FuzzEd', ['DeleteEdge'])

        # Adding model 'DeleteGraph'
        db.create_table('FuzzEd_deletegraph', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Graph'])),
        ))
        db.send_create_signal('FuzzEd', ['DeleteGraph'])

        # Adding model 'DeleteNode'
        db.create_table('FuzzEd_deletenode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Node'])),
        ))
        db.send_create_signal('FuzzEd', ['DeleteNode'])

        # Adding model 'RenameGraph'
        db.create_table('FuzzEd_renamegraph', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Graph'])),
            ('old_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('new_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('FuzzEd', ['RenameGraph'])

        # Adding model 'UserProfile'
        db.create_table('FuzzEd_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('newsletter', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('FuzzEd', ['UserProfile'])


    def backwards(self, orm):
        # Deleting model 'Graph'
        db.delete_table('FuzzEd_graph')

        # Deleting model 'Node'
        db.delete_table('FuzzEd_node')

        # Deleting model 'Edge'
        db.delete_table('FuzzEd_edge')

        # Deleting model 'Property'
        db.delete_table('FuzzEd_property')

        # Deleting model 'AddEdge'
        db.delete_table('FuzzEd_addedge')

        # Deleting model 'AddGraph'
        db.delete_table('FuzzEd_addgraph')

        # Deleting model 'AddNode'
        db.delete_table('FuzzEd_addnode')

        # Deleting model 'ChangeNode'
        db.delete_table('FuzzEd_changenode')

        # Deleting model 'PropertyChange'
        db.delete_table('FuzzEd_propertychange')

        # Deleting model 'DeleteEdge'
        db.delete_table('FuzzEd_deleteedge')

        # Deleting model 'DeleteGraph'
        db.delete_table('FuzzEd_deletegraph')

        # Deleting model 'DeleteNode'
        db.delete_table('FuzzEd_deletenode')

        # Deleting model 'RenameGraph'
        db.delete_table('FuzzEd_renamegraph')

        # Deleting model 'UserProfile'
        db.delete_table('FuzzEd_userprofile')


    models = {
        'FuzzEd.addedge': {
            'Meta': {'object_name': 'AddEdge'},
            'edge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Edge']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.addgraph': {
            'Meta': {'object_name': 'AddGraph'},
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Graph']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.addnode': {
            'Meta': {'object_name': 'AddNode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Node']"}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.changenode': {
            'Meta': {'object_name': 'ChangeNode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Node']"}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.deleteedge': {
            'Meta': {'object_name': 'DeleteEdge'},
            'edge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Edge']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.deletegraph': {
            'Meta': {'object_name': 'DeleteGraph'},
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Graph']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.deletenode': {
            'Meta': {'object_name': 'DeleteNode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Node']"}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.edge': {
            'Meta': {'object_name': 'Edge'},
            'client_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'edges'", 'to': "orm['FuzzEd.Graph']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outgoing'", 'to': "orm['FuzzEd.Node']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'incoming'", 'to': "orm['FuzzEd.Node']"})
        },
        'FuzzEd.graph': {
            'Meta': {'object_name': 'Graph'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'graphs'", 'to': "orm['auth.User']"})
        },
        'FuzzEd.node': {
            'Meta': {'object_name': 'Node'},
            'client_id': ('django.db.models.fields.BigIntegerField', [], {'default': '-9223372036854775807'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': "orm['FuzzEd.Graph']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'FuzzEd.property': {
            'Meta': {'object_name': 'Property'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'properties'", 'to': "orm['FuzzEd.Node']"}),
            'value': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {})
        },
        'FuzzEd.propertychange': {
            'Meta': {'object_name': 'PropertyChange'},
            'command': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changes'", 'to': "orm['FuzzEd.ChangeNode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'new_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'old_value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'FuzzEd.renamegraph': {
            'Meta': {'object_name': 'RenameGraph'},
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Graph']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'new_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'old_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
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
        }
    }

    complete_apps = ['FuzzEd']