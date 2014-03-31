from django.db import models
from FuzzEd.models import Node


class NodeGroup(models.Model):
    class Meta:
        app_label = 'FuzzEd'

    client_id = models.BigIntegerField()
    nodes     = models.ManyToManyField(Node)
    deleted   = models.BooleanField(default=False)
