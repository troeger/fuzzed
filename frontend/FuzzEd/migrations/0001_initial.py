# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'FuzzEd_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='own_projects', to=orm['auth.User'])),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('FuzzEd', ['Project'])

        # Adding M2M table for field users on 'Project'
        m2m_table_name = db.shorten_name(u'FuzzEd_project_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['FuzzEd.project'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'user_id'])

        # Adding model 'Graph'
        db.create_table(u'FuzzEd_graph', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='graphs', to=orm['auth.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='graphs', to=orm['FuzzEd.Project'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('read_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('FuzzEd', ['Graph'])

        # Adding model 'Sharing'
        db.create_table(u'FuzzEd_sharing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sharings', to=orm['FuzzEd.Graph'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sharings', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='sharings', null=True, to=orm['FuzzEd.Project'])),
        ))
        db.send_create_signal('FuzzEd', ['Sharing'])

        # Adding model 'Node'
        db.create_table(u'FuzzEd_node', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client_id', self.gf('django.db.models.fields.BigIntegerField')(default=-2147483647)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nodes', to=orm['FuzzEd.Graph'])),
            ('x', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('FuzzEd', ['Node'])

        # Adding model 'Edge'
        db.create_table(u'FuzzEd_edge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='edges', to=orm['FuzzEd.Graph'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='outgoing', to=orm['FuzzEd.Node'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='incoming', to=orm['FuzzEd.Node'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('FuzzEd', ['Edge'])

        # Adding model 'Configuration'
        db.create_table(u'FuzzEd_configuration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='configurations', to=orm['FuzzEd.Graph'])),
            ('costs', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('FuzzEd', ['Configuration'])

        # Adding model 'NodeConfiguration'
        db.create_table(u'FuzzEd_nodeconfiguration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['FuzzEd.Node'])),
            ('setting', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')()),
            ('configuration', self.gf('django.db.models.fields.related.ForeignKey')(related_name='node_configurations', to=orm['FuzzEd.Configuration'])),
        ))
        db.send_create_signal('FuzzEd', ['NodeConfiguration'])

        # Adding model 'Result'
        db.create_table(u'FuzzEd_result', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='results', to=orm['FuzzEd.Graph'])),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(related_name='results', to=orm['FuzzEd.Job'])),
            ('configuration', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='results', null=True, to=orm['FuzzEd.Configuration'])),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('minimum', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('maximum', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('peak', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('reliability', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('mttf', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('timestamp', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('rounds', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('failures', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('binary_value', self.gf('django.db.models.fields.BinaryField')(null=True)),
            ('points', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')(null=True, blank=True)),
            ('issues', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')(null=True, blank=True)),
        ))
        db.send_create_signal('FuzzEd', ['Result'])

        # Adding model 'Job'
        db.create_table(u'FuzzEd_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jobs', null=True, to=orm['FuzzEd.Graph'])),
            ('graph_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('secret', self.gf('django.db.models.fields.CharField')(default='a9c093f8-7edc-4cc7-afe5-1c34b2c1ae16', max_length=64)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('exit_code', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('FuzzEd', ['Job'])

        # Adding model 'NodeGroup'
        db.create_table(u'FuzzEd_nodegroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client_id', self.gf('django.db.models.fields.BigIntegerField')(default=-2147483647)),
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

        # Adding model 'Property'
        db.create_table(u'FuzzEd_property', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')()),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='properties', null=True, blank=True, to=orm['FuzzEd.Node'])),
            ('edge', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='properties', null=True, blank=True, to=orm['FuzzEd.Edge'])),
            ('node_group', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='properties', null=True, blank=True, to=orm['FuzzEd.NodeGroup'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('FuzzEd', ['Property'])

        # Adding model 'AddProject'
        db.create_table(u'FuzzEd_addproject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Project'])),
        ))
        db.send_create_signal('FuzzEd', ['AddProject'])

        # Adding model 'AddEdge'
        db.create_table(u'FuzzEd_addedge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Edge'])),
        ))
        db.send_create_signal('FuzzEd', ['AddEdge'])

        # Adding model 'AddGraph'
        db.create_table(u'FuzzEd_addgraph', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Graph'])),
        ))
        db.send_create_signal('FuzzEd', ['AddGraph'])

        # Adding model 'AddNode'
        db.create_table(u'FuzzEd_addnode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Node'])),
        ))
        db.send_create_signal('FuzzEd', ['AddNode'])

        # Adding model 'ChangeNode'
        db.create_table(u'FuzzEd_changenode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Node'])),
        ))
        db.send_create_signal('FuzzEd', ['ChangeNode'])

        # Adding model 'ChangeEdge'
        db.create_table(u'FuzzEd_changeedge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Edge'])),
        ))
        db.send_create_signal('FuzzEd', ['ChangeEdge'])

        # Adding model 'PropertyChange'
        db.create_table(u'FuzzEd_propertychange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('command', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changes', to=orm['FuzzEd.ChangeNode'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('old_value', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')()),
            ('new_value', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal('FuzzEd', ['PropertyChange'])

        # Adding model 'EdgePropertyChange'
        db.create_table(u'FuzzEd_edgepropertychange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('command', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changes', to=orm['FuzzEd.ChangeEdge'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('old_value', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')()),
            ('new_value', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal('FuzzEd', ['EdgePropertyChange'])

        # Adding model 'DeleteEdge'
        db.create_table(u'FuzzEd_deleteedge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Edge'])),
        ))
        db.send_create_signal('FuzzEd', ['DeleteEdge'])

        # Adding model 'DeleteGraph'
        db.create_table(u'FuzzEd_deletegraph', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Graph'])),
        ))
        db.send_create_signal('FuzzEd', ['DeleteGraph'])

        # Adding model 'DeleteProject'
        db.create_table(u'FuzzEd_deleteproject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Project'])),
        ))
        db.send_create_signal('FuzzEd', ['DeleteProject'])

        # Adding model 'DeleteNode'
        db.create_table(u'FuzzEd_deletenode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Node'])),
        ))
        db.send_create_signal('FuzzEd', ['DeleteNode'])

        # Adding model 'RenameGraph'
        db.create_table(u'FuzzEd_renamegraph', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('undoable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['FuzzEd.Graph'])),
            ('old_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('new_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('FuzzEd', ['RenameGraph'])

        # Adding model 'UserProfile'
        db.create_table(u'FuzzEd_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('newsletter', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('FuzzEd', ['UserProfile'])

        # Adding model 'Notification'
        db.create_table(u'FuzzEd_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('FuzzEd', ['Notification'])

        # Adding M2M table for field users on 'Notification'
        m2m_table_name = db.shorten_name(u'FuzzEd_notification_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notification', models.ForeignKey(orm['FuzzEd.notification'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['notification_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table(u'FuzzEd_project')

        # Removing M2M table for field users on 'Project'
        db.delete_table(db.shorten_name(u'FuzzEd_project_users'))

        # Deleting model 'Graph'
        db.delete_table(u'FuzzEd_graph')

        # Deleting model 'Sharing'
        db.delete_table(u'FuzzEd_sharing')

        # Deleting model 'Node'
        db.delete_table(u'FuzzEd_node')

        # Deleting model 'Edge'
        db.delete_table(u'FuzzEd_edge')

        # Deleting model 'Configuration'
        db.delete_table(u'FuzzEd_configuration')

        # Deleting model 'NodeConfiguration'
        db.delete_table(u'FuzzEd_nodeconfiguration')

        # Deleting model 'Result'
        db.delete_table(u'FuzzEd_result')

        # Deleting model 'Job'
        db.delete_table(u'FuzzEd_job')

        # Deleting model 'NodeGroup'
        db.delete_table(u'FuzzEd_nodegroup')

        # Removing M2M table for field nodes on 'NodeGroup'
        db.delete_table(db.shorten_name(u'FuzzEd_nodegroup_nodes'))

        # Deleting model 'Property'
        db.delete_table(u'FuzzEd_property')

        # Deleting model 'AddProject'
        db.delete_table(u'FuzzEd_addproject')

        # Deleting model 'AddEdge'
        db.delete_table(u'FuzzEd_addedge')

        # Deleting model 'AddGraph'
        db.delete_table(u'FuzzEd_addgraph')

        # Deleting model 'AddNode'
        db.delete_table(u'FuzzEd_addnode')

        # Deleting model 'ChangeNode'
        db.delete_table(u'FuzzEd_changenode')

        # Deleting model 'ChangeEdge'
        db.delete_table(u'FuzzEd_changeedge')

        # Deleting model 'PropertyChange'
        db.delete_table(u'FuzzEd_propertychange')

        # Deleting model 'EdgePropertyChange'
        db.delete_table(u'FuzzEd_edgepropertychange')

        # Deleting model 'DeleteEdge'
        db.delete_table(u'FuzzEd_deleteedge')

        # Deleting model 'DeleteGraph'
        db.delete_table(u'FuzzEd_deletegraph')

        # Deleting model 'DeleteProject'
        db.delete_table(u'FuzzEd_deleteproject')

        # Deleting model 'DeleteNode'
        db.delete_table(u'FuzzEd_deletenode')

        # Deleting model 'RenameGraph'
        db.delete_table(u'FuzzEd_renamegraph')

        # Deleting model 'UserProfile'
        db.delete_table(u'FuzzEd_userprofile')

        # Deleting model 'Notification'
        db.delete_table(u'FuzzEd_notification')

        # Removing M2M table for field users on 'Notification'
        db.delete_table(db.shorten_name(u'FuzzEd_notification_users'))


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
        'FuzzEd.configuration': {
            'Meta': {'object_name': 'Configuration'},
            'costs': ('django.db.models.fields.IntegerField', [], {}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'configurations'", 'to': "orm['FuzzEd.Graph']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'secret': ('django.db.models.fields.CharField', [], {'default': "'0e102679-c01a-4fe3-a00c-0130e18b1768'", 'max_length': '64'})
        },
        'FuzzEd.node': {
            'Meta': {'object_name': 'Node'},
            'client_id': ('django.db.models.fields.BigIntegerField', [], {'default': '-2147483647'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': "orm['FuzzEd.Graph']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'FuzzEd.nodeconfiguration': {
            'Meta': {'object_name': 'NodeConfiguration'},
            'configuration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'node_configurations'", 'to': "orm['FuzzEd.Configuration']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['FuzzEd.Node']"}),
            'setting': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {})
        },
        'FuzzEd.nodegroup': {
            'Meta': {'object_name': 'NodeGroup'},
            'client_id': ('django.db.models.fields.BigIntegerField', [], {'default': '-2147483647'}),
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
        'FuzzEd.result': {
            'Meta': {'object_name': 'Result'},
            'binary_value': ('django.db.models.fields.BinaryField', [], {'null': 'True'}),
            'configuration': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'results'", 'null': 'True', 'to': "orm['FuzzEd.Configuration']"}),
            'failures': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['FuzzEd.Graph']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issues': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['FuzzEd.Job']"}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'maximum': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'minimum': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'mttf': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'peak': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'points': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'reliability': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rounds': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'FuzzEd.sharing': {
            'Meta': {'object_name': 'Sharing'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sharings'", 'to': "orm['FuzzEd.Graph']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'sharings'", 'null': 'True', 'to': "orm['FuzzEd.Project']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sharings'", 'to': u"orm['auth.User']"})
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