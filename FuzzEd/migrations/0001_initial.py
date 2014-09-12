# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import FuzzEd.models.job
from django.conf import settings
import FuzzEd.lib.jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddEdge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('undoable', models.BooleanField(default=False)),
                ('insert_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AddGraph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('undoable', models.BooleanField(default=False)),
                ('insert_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AddNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('undoable', models.BooleanField(default=False)),
                ('insert_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AddProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('undoable', models.BooleanField(default=False)),
                ('insert_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChangeEdge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('undoable', models.BooleanField(default=False)),
                ('insert_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChangeNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('undoable', models.BooleanField(default=False)),
                ('insert_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('costs', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeleteEdge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('undoable', models.BooleanField(default=False)),
                ('insert_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeleteGraph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('undoable', models.BooleanField(default=False)),
                ('insert_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeleteNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('undoable', models.BooleanField(default=False)),
                ('insert_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeleteProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('undoable', models.BooleanField(default=False)),
                ('insert_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.BigIntegerField()),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EdgePropertyChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255)),
                ('old_value', FuzzEd.lib.jsonfield.fields.JSONField()),
                ('new_value', FuzzEd.lib.jsonfield.fields.JSONField()),
                ('command', models.ForeignKey(related_name=b'changes', to='FuzzEd.ChangeEdge')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=127, choices=[('dfd', 'Data Flow Diagram'), ('faulttree', 'Fault Tree'), ('fuzztree', 'Fuzz Tree'), ('rbd', 'Reliability Block Diagram')])),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('read_only', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(related_name=b'graphs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('graph_modified', models.DateTimeField()),
                ('secret', models.CharField(default=FuzzEd.models.job.gen_uuid, max_length=64)),
                ('kind', models.CharField(max_length=127, choices=[(b'mincut', b'Cutset computation'), (b'topevent', b'Top event calculation (analytical)'), (b'simulation', b'Top event calculation (simulation)'), (b'eps', b'EPS rendering job'), (b'pdf', b'PDF rendering job')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('exit_code', models.IntegerField(null=True)),
                ('graph', models.ForeignKey(related_name=b'jobs', to='FuzzEd.Graph', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.BigIntegerField(default=-9223372036854775807)),
                ('kind', models.CharField(max_length=127, choices=[('Data Flow Diagram', (('node', 'Node'), ('process', 'Process'), ('stickyNote', 'Sticky Note'), ('storage', 'Storage'), ('external', 'External Entity'))), ('Fault Tree', (('dynamicGate', 'Dynamic Gate'), ('intermediateEventSet', 'Intermediate Event Set'), ('xorGate', 'XOR Gate'), ('undevelopedEvent', 'Undeveloped Event'), ('event', 'Event'), ('houseEvent', 'House Event'), ('eventSet', 'Event Set'), ('stickyNote', 'Sticky Note'), ('spareGate', 'Spare Gate'), ('intermediateEvent', 'Intermediate Event'), ('fdepGate', 'FDEP Gate'), ('staticGate', 'Static Gate'), ('gate', 'Gate'), ('seqGate', 'Sequential Gate'), ('node', 'Node'), ('transferIn', 'Transfer In'), ('basicEvent', 'Basic Event'), ('andGate', 'AND Gate'), ('basicEventSet', 'Basic Event Set'), ('votingOrGate', 'Voting OR Gate'), ('orGate', 'OR Gate'), ('topEvent', 'Top Event'), ('priorityAndGate', 'Priority AND Gate'))), ('Fuzz Tree', (('dynamicGate', 'Dynamic Gate'), ('intermediateEventSet', 'Intermediate Event Set'), ('xorGate', 'XOR Gate'), ('undevelopedEvent', 'Undeveloped Event'), ('event', 'Event'), ('houseEvent', 'House Event'), ('eventSet', 'eventSet'), ('stickyNote', 'Sticky Note'), ('intermediateEvent', 'Intermediate Event'), ('staticGate', 'Static Gate'), ('gate', 'Gate'), ('node', 'Node'), ('featureVariation', 'Feature Variation'), ('redundancyVariation', 'Redundancy Variation'), ('transferIn', 'Transfer In'), ('basicEvent', 'Basic Event'), ('andGate', 'AND Gate'), ('basicEventSet', 'Basic Event Set'), ('variationPoint', 'Variation Point'), ('votingOrGate', 'Voting OR Gate'), ('orGate', 'OR Gate'), ('topEvent', 'Top Event'))), ('Reliability Block Diagram', (('node', 'Node'), ('stickyNote', 'Sticky Note'), ('end', 'End'), ('out_of', 'Out of'), ('start', 'Start'), ('block', 'Block')))])),
                ('x', models.IntegerField(default=0)),
                ('y', models.IntegerField(default=0)),
                ('deleted', models.BooleanField(default=False)),
                ('graph', models.ForeignKey(related_name=b'nodes', to='FuzzEd.Graph')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NodeConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('setting', FuzzEd.lib.jsonfield.fields.JSONField()),
                ('configuration', models.ForeignKey(related_name=b'node_configurations', to='FuzzEd.Configuration')),
                ('node', models.ForeignKey(to='FuzzEd.Node')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NodeGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.BigIntegerField(default=-9223372036854775807)),
                ('deleted', models.BooleanField(default=False)),
                ('graph', models.ForeignKey(related_name=b'groups', to='FuzzEd.Graph')),
                ('nodes', models.ManyToManyField(to='FuzzEd.Node')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=255)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(related_name=b'own_projects', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name=b'projects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255)),
                ('value', FuzzEd.lib.jsonfield.fields.JSONField()),
                ('deleted', models.BooleanField(default=False)),
                ('edge', models.ForeignKey(related_name=b'properties', default=None, blank=True, to='FuzzEd.Edge', null=True)),
                ('node', models.ForeignKey(related_name=b'properties', default=None, blank=True, to='FuzzEd.Node', null=True)),
                ('node_group', models.ForeignKey(related_name=b'properties', default=None, blank=True, to='FuzzEd.NodeGroup', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PropertyChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255)),
                ('old_value', FuzzEd.lib.jsonfield.fields.JSONField()),
                ('new_value', FuzzEd.lib.jsonfield.fields.JSONField()),
                ('command', models.ForeignKey(related_name=b'changes', to='FuzzEd.ChangeNode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RenameGraph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('undoable', models.BooleanField(default=False)),
                ('insert_date', models.DateTimeField(auto_now_add=True)),
                ('old_name', models.CharField(max_length=255)),
                ('new_name', models.CharField(max_length=255)),
                ('graph', models.ForeignKey(related_name=b'+', to='FuzzEd.Graph')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=1, choices=[(b'G', b'graphissues'), (b'S', b'simulation'), (b'M', b'mincut'), (b'T', b'topevent'), (b'P', b'pdf'), (b'E', b'eps')])),
                ('minimum', models.FloatField(null=True)),
                ('maximum', models.FloatField(null=True)),
                ('peak', models.FloatField(null=True)),
                ('reliability', models.FloatField(null=True)),
                ('mttf', models.FloatField(null=True)),
                ('timestamp', models.IntegerField(null=True)),
                ('rounds', models.IntegerField(null=True)),
                ('failures', models.IntegerField(null=True)),
                ('binary_value', models.BinaryField(null=True)),
                ('points', FuzzEd.lib.jsonfield.fields.JSONField(null=True, blank=True)),
                ('issues', FuzzEd.lib.jsonfield.fields.JSONField(null=True, blank=True)),
                ('configuration', models.ForeignKey(related_name=b'results', blank=True, to='FuzzEd.Configuration', null=True)),
                ('graph', models.ForeignKey(related_name=b'results', to='FuzzEd.Graph')),
                ('job', models.ForeignKey(related_name=b'results', to='FuzzEd.Job')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sharing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('graph', models.ForeignKey(related_name=b'sharings', to='FuzzEd.Graph')),
                ('project', models.ForeignKey(related_name=b'sharings', default=None, to='FuzzEd.Project', null=True)),
                ('user', models.ForeignKey(related_name=b'sharings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('newsletter', models.BooleanField(default=False)),
                ('user', models.OneToOneField(related_name=b'profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='graph',
            name='project',
            field=models.ForeignKey(related_name=b'graphs', to='FuzzEd.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='edge',
            name='graph',
            field=models.ForeignKey(related_name=b'edges', to='FuzzEd.Graph'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='edge',
            name='source',
            field=models.ForeignKey(related_name=b'outgoing', to='FuzzEd.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='edge',
            name='target',
            field=models.ForeignKey(related_name=b'incoming', to='FuzzEd.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deleteproject',
            name='project',
            field=models.ForeignKey(related_name=b'+', to='FuzzEd.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deletenode',
            name='node',
            field=models.ForeignKey(related_name=b'+', to='FuzzEd.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deletegraph',
            name='graph',
            field=models.ForeignKey(related_name=b'+', to='FuzzEd.Graph'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deleteedge',
            name='edge',
            field=models.ForeignKey(related_name=b'+', to='FuzzEd.Edge'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='configuration',
            name='graph',
            field=models.ForeignKey(related_name=b'configurations', to='FuzzEd.Graph'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='changenode',
            name='node',
            field=models.ForeignKey(related_name=b'+', to='FuzzEd.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='changeedge',
            name='edge',
            field=models.ForeignKey(related_name=b'+', to='FuzzEd.Edge'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='addproject',
            name='project',
            field=models.ForeignKey(related_name=b'+', to='FuzzEd.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='addnode',
            name='node',
            field=models.ForeignKey(related_name=b'+', to='FuzzEd.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='addgraph',
            name='graph',
            field=models.ForeignKey(related_name=b'+', to='FuzzEd.Graph'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='addedge',
            name='edge',
            field=models.ForeignKey(related_name=b'+', to='FuzzEd.Edge'),
            preserve_default=True,
        ),
    ]
