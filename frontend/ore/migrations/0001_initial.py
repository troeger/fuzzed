# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import ore.models.job


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('costs', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.BigIntegerField()),
                ('deleted', models.BooleanField(default=False)),
            ],
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
                ('owner', models.ForeignKey(related_name='graphs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('graph_modified', models.DateTimeField()),
                ('secret', models.CharField(default=ore.models.job.gen_uuid, max_length=64)),
                ('kind', models.CharField(max_length=127, choices=[(b'mincut', b'Cutset computation'), (b'topevent', b'Top event calculation (analytical)'), (b'simulation', b'Top event calculation (simulation)'), (b'eps', b'EPS rendering job'), (b'pdf', b'PDF rendering job')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('exit_code', models.IntegerField(null=True)),
                ('graph', models.ForeignKey(related_name='jobs', to='ore.Graph', null=True)),
            ],
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
                ('graph', models.ForeignKey(related_name='nodes', to='ore.Graph')),
            ],
        ),
        migrations.CreateModel(
            name='NodeConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('setting', models.TextField()),
                ('configuration', models.ForeignKey(related_name='node_configurations', to='ore.Configuration')),
                ('node', models.ForeignKey(to='ore.Node')),
            ],
        ),
        migrations.CreateModel(
            name='NodeGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.BigIntegerField(default=-9223372036854775807)),
                ('deleted', models.BooleanField(default=False)),
                ('graph', models.ForeignKey(related_name='groups', to='ore.Graph')),
                ('nodes', models.ManyToManyField(to='ore.Node')),
            ],
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
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(related_name='own_projects', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('deleted', models.BooleanField(default=False)),
                ('edge', models.ForeignKey(related_name='properties', default=None, blank=True, to='ore.Edge', null=True)),
                ('node', models.ForeignKey(related_name='properties', default=None, blank=True, to='ore.Node', null=True)),
                ('node_group', models.ForeignKey(related_name='properties', default=None, blank=True, to='ore.NodeGroup', null=True)),
            ],
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
                ('points', models.TextField(null=True, blank=True)),
                ('issues', models.TextField(null=True, blank=True)),
                ('configuration', models.ForeignKey(related_name='results', blank=True, to='ore.Configuration', null=True)),
                ('graph', models.ForeignKey(related_name='results', to='ore.Graph')),
                ('job', models.ForeignKey(related_name='results', to='ore.Job')),
            ],
        ),
        migrations.CreateModel(
            name='Sharing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('graph', models.ForeignKey(related_name='sharings', to='ore.Graph')),
                ('project', models.ForeignKey(related_name='sharings', default=None, to='ore.Project', null=True)),
                ('user', models.ForeignKey(related_name='sharings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('newsletter', models.BooleanField(default=False)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='graph',
            name='project',
            field=models.ForeignKey(related_name='graphs', to='ore.Project'),
        ),
        migrations.AddField(
            model_name='edge',
            name='graph',
            field=models.ForeignKey(related_name='edges', to='ore.Graph'),
        ),
        migrations.AddField(
            model_name='edge',
            name='source',
            field=models.ForeignKey(related_name='outgoing', to='ore.Node'),
        ),
        migrations.AddField(
            model_name='edge',
            name='target',
            field=models.ForeignKey(related_name='incoming', to='ore.Node'),
        ),
        migrations.AddField(
            model_name='configuration',
            name='graph',
            field=models.ForeignKey(related_name='configurations', to='ore.Graph'),
        ),
    ]
