from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .graph import Graph
import json


class Configuration(models.Model):

    """
    Class: Project

    Fields:
     {Graph} graph       -
     {int}   costs       -
    """

    class Meta:
        app_label = 'FuzzEd'

    graph = models.ForeignKey(Graph, related_name='configurations')
    costs = models.IntegerField()

    def to_dict(self):
        '''
          Returns the specific node configurations in this graph configuration
          as JSON dictionary data structure. The keys are node client ID's, so that the
          JS code can identify them.
        '''
        result = {}
        for node_conf in self.node_configurations.all():
            result[node_conf.node.client_id] = json.loads(node_conf.setting)
        return result
