# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Configuration.id'
        db.delete_column(u'FuzzEd_configuration', u'id')

        # Adding field 'Configuration.result'
        db.add_column(u'FuzzEd_configuration', 'result',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, related_name='configuration', unique=True, primary_key=True, to=orm['FuzzEd.Result']),
                      keep_default=False)

        # Adding field 'Graph.graph_issues'
        db.add_column(u'FuzzEd_graph', 'graph_issues',
                      self.gf('FuzzEd.lib.jsonfield.fields.JSONField')(default=''),
                      keep_default=False)


        # Changing field 'NodeConfiguration.setting'
        db.alter_column(u'FuzzEd_nodeconfiguration', 'setting', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')())
        # Deleting field 'Result.prob_sortable'
        db.delete_column(u'FuzzEd_result', 'prob_sortable')

        # Deleting field 'Result.analysis_type'
        db.delete_column(u'FuzzEd_result', 'analysis_type')

        # Deleting field 'Result.configuration'
        db.delete_column(u'FuzzEd_result', 'configuration_id')

        # Deleting field 'Result.issues'
        db.delete_column(u'FuzzEd_result', 'issues')

        # Adding field 'Result.type'
        db.add_column(u'FuzzEd_result', 'type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1),
                      keep_default=False)

        # Adding field 'Result.prob_sort'
        db.add_column(u'FuzzEd_result', 'prob_sort',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Result.node_issues'
        db.add_column(u'FuzzEd_result', 'node_issues',
                      self.gf('FuzzEd.lib.jsonfield.fields.JSONField')(default=''),
                      keep_default=False)


        # Changing field 'Result.prob'
        db.alter_column(u'FuzzEd_result', 'prob', self.gf('FuzzEd.lib.jsonfield.fields.JSONField')())

        # Changing field 'Result.rounds'
        db.alter_column(u'FuzzEd_result', 'rounds', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Result.failures'
        db.alter_column(u'FuzzEd_result', 'failures', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):
        # Adding field 'Configuration.id'
        db.add_column(u'FuzzEd_configuration', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Deleting field 'Configuration.result'
        db.delete_column(u'FuzzEd_configuration', 'result_id')

        # Deleting field 'Graph.graph_issues'
        db.delete_column(u'FuzzEd_graph', 'graph_issues')


        # Changing field 'NodeConfiguration.setting'
        db.alter_column(u'FuzzEd_nodeconfiguration', 'setting', self.gf('django.db.models.fields.TextField')())
        # Adding field 'Result.prob_sortable'
        db.add_column(u'FuzzEd_result', 'prob_sortable',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Result.analysis_type'
        db.add_column(u'FuzzEd_result', 'analysis_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1),
                      keep_default=False)

        # Adding field 'Result.configuration'
        db.add_column(u'FuzzEd_result', 'configuration',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='result', to=orm['FuzzEd.Configuration']),
                      keep_default=False)

        # Adding field 'Result.issues'
        db.add_column(u'FuzzEd_result', 'issues',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'Result.type'
        db.delete_column(u'FuzzEd_result', 'type')

        # Deleting field 'Result.prob_sort'
        db.delete_column(u'FuzzEd_result', 'prob_sort')

        # Deleting field 'Result.node_issues'
        db.delete_column(u'FuzzEd_result', 'node_issues')


        # Changing field 'Result.prob'
        db.alter_column(u'FuzzEd_result', 'prob', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Result.rounds'
        db.alter_column(u'FuzzEd_result', 'rounds', self.gf('django.db.models.fields.IntegerField')(default=0))

        # Changing field 'Result.failures'
        db.alter_column(u'FuzzEd_result', 'failures', self.gf('django.db.models.fields.IntegerField')(default=0))

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
            'result': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'configuration'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['FuzzEd.Result']"})
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
        'FuzzEd.graph': {
            'Meta': {'object_name': 'Graph'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'graph_issues': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {}),
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
            'secret': ('django.db.models.fields.CharField', [], {'default': "'c66d9eb2-0eaf-46d7-a5f8-053cb5674521'", 'max_length': '64'})
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
        'FuzzEd.nodeconfiguration': {
            'Meta': {'object_name': 'NodeConfiguration'},
            'configuration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'node_configurations'", 'to': "orm['FuzzEd.Configuration']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['FuzzEd.Node']"}),
            'setting': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'properties'", 'to': "orm['FuzzEd.Node']"}),
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
            'decomposition': ('django.db.models.fields.IntegerField', [], {}),
            'failures': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['FuzzEd.Graph']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node_issues': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {}),
            'prob': ('FuzzEd.lib.jsonfield.fields.JSONField', [], {}),
            'prob_sort': ('django.db.models.fields.IntegerField', [], {}),
            'rounds': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
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