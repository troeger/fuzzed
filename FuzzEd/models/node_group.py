import json

from django.db import models

from FuzzEd.models import Node, Graph


class NodeGroup(models.Model):
    class Meta:
        app_label = 'FuzzEd'

    client_id = models.BigIntegerField()
    graph     = models.ForeignKey(Graph, null=False, related_name='groups')
    nodes     = models.ManyToManyField(Node)
    deleted   = models.BooleanField(default=False)

    def to_dict(self):
    	return {'id'      : self.client_id,
                'nodeIds': [node.client_id for node in self.nodes.all()]}

    def to_json(self):
    	return json.dumps(self.to_dict())
