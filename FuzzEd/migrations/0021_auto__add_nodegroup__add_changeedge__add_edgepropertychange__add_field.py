# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NodeGroup'
        db.create_table(u'FuzzEd_nodegroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groups', to=orm['FuzzEd.Graph'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('FuzzEd', ['NodeGroup'])

        # Adding M2M table for field nodes on 'NodeGroup'
        m2m_table_name = db.shorten_name(u'FuzzEd_nodegroup_nodes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nodegroup', models.ForeignKey(orm['FuzzEd.nodegroup'], null=False)),
            ('node', models.ForeignKey(orm['FuzzEd.node'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nodegroup_id', 'node_id'])

        # Adding model 'ChangeEdge'
        db.create_table(u'FuzzEd_changeedge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Edge'])),
        ))
        db.send_create_signal('FuzzEd', ['ChangeEdge'])

        # Adding model 'EdgePropertyChange'
        db.create_table(u'FuzzEd_edgepropertychange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('command', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changes', to=orm['FuzzEd.ChangeEdge'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('old_value', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')()),
            ('new_value', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal('FuzzEd', ['EdgePropertyChange'])

        # Adding field 'Property.edge'
        db.add_column(u'FuzzEd_property', 'edge',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='properties', null=True, blank=True, to=orm['FuzzEd.Edge']),
                      keep_default=False)

        # Adding field 'Property.node_group'
        db.add_column(u'FuzzEd_property', 'node_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='properties', null=True, blank=True, to=orm['FuzzEd.NodeGroup']),
                      keep_default=False)


        # Changing field 'Property.node'
        db.alter_column(u'FuzzEd_property', 'node_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['FuzzEd.Node']))

    def backwards(self, orm):
        # Deleting model 'NodeGroup'
        db.delete_table(u'FuzzEd_nodegroup')

        # Removing M2M table for field nodes on 'NodeGroup'
        db.delete_table(db.shorten_name(u'FuzzEd_nodegroup_nodes'))

        # Deleting model 'ChangeEdge'
        db.delete_table(u'FuzzEd_changeedge')

        # Deleting model 'EdgePropertyChange'
        db.delete_table(u'FuzzEd_edgepropertychange')

        # Deleting field 'Property.edge'
        db.delete_column(u'FuzzEd_property', 'edge_id')

        # Deleting field 'Property.node_group'
        db.delete_column(u'FuzzEd_property', 'node_group_id')


        # User chose to not deal with backwards NULL issues for 'Property.node'
        raise RuntimeError("Cannot reverse this migration. 'Property.node' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Property.node'
        db.alter_column(u'FuzzEd_property', 'node_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['FuzzEd.Node']))

    models = {
        'FuzzEd.addedge': {
            'Meta': {'object_name': 'AddEdge'},
            'edge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Edge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.addgraph': {
            'Meta': {'object_name': 'AddGraph'},
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Graph']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.addnode': {
            'Meta': {'object_name': 'AddNode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Node']"}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.addproject': {
            'Meta': {'object_name': 'AddProject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Project']"}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.changeedge': {
            'Meta': {'object_name': 'ChangeEdge'},
            'edge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Edge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.changenode': {
            'Meta': {'object_name': 'ChangeNode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Node']"}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.deleteedge': {
            'Meta': {'object_name': 'DeleteEdge'},
            'edge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Edge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.deletegraph': {
            'Meta': {'object_name': 'DeleteGraph'},
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Graph']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.deletenode': {
            'Meta': {'object_name': 'DeleteNode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Node']"}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.deleteproject': {
            'Meta': {'object_name': 'DeleteProject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Project']"}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.edge': {
            'Meta': {'object_name': 'Edge'},
            'client_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'edges'", 'to': "orm['FuzzEd.Graph']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outgoing'", 'to': "orm['FuzzEd.Node']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'incoming'", 'to': "orm['FuzzEd.Node']"})
        },
        'FuzzEd.edgepropertychange': {
            'Meta': {'object_name': 'EdgePropertyChange'},
            'command': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changes'", 'to': "orm['FuzzEd.ChangeEdge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'new_value': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {}),
            'old_value': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {})
        },
        'FuzzEd.graph': {
            'Meta': {'object_name': 'Graph'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'graphs'", 'to': u"orm['auth.User']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'graphs'", 'to': "orm['FuzzEd.Project']"}),
            'read_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.job': {
            'Meta': {'object_name': 'Job'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exit_code': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs'", 'null': 'True', 'to': "orm['FuzzEd.Graph']"}),
            'graph_modified': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'result': ('django.db.models.fields.BinaryField', [], {'null': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'67ab569d-d1fa-4cf4-bbc3-a8615d838d7c'", 'max_length': '64'})
        },
        'FuzzEd.node': {
            'Meta': {'object_name': 'Node'},
            'client_id': ('django.db.models.fields.BigIntegerField', [], {'default': '-9223372036854775807'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': "orm['FuzzEd.Graph']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'FuzzEd.nodegroup': {
            'Meta': {'object_name': 'NodeGroup'},
            'client_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups'", 'to': "orm['FuzzEd.Graph']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nodes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['FuzzEd.Node']", 'symmetrical': 'False'})
        },
        'FuzzEd.notification': {
            'Meta': {'object_name': 'Notification'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        },
        'FuzzEd.project': {
            'Meta': {'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'own_projects'", 'to': u"orm['auth.User']"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        'FuzzEd.property': {
            'Meta': {'object_name': 'Property'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edge': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'properties'", 'null': 'True', 'blank': 'True', 'to': "orm['FuzzEd.Edge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'properties'", 'null': 'True', 'blank': 'True', 'to': "orm['FuzzEd.Node']"}),
            'node_group': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'properties'", 'null': 'True', 'blank': 'True', 'to': "orm['FuzzEd.NodeGroup']"}),
            'value': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {})
        },
        'FuzzEd.propertychange': {
            'Meta': {'object_name': 'PropertyChange'},
            'command': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changes'", 'to': "orm['FuzzEd.ChangeNode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'new_value': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {}),
            'old_value': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {})
        },
        'FuzzEd.renamegraph': {
            'Meta': {'object_name': 'RenameGraph'},
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['FuzzEd.Graph']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'new_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'old_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'undoable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'FuzzEd.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['FuzzEd']