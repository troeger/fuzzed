from django.db import models

from .node import Node
from .configuration import Configuration


class NodeConfiguration(models.Model):

    """
    Class: Project

    Fields:
     {Node}          node
     {JSON}          setting
     {Configuration} configuration
    """

    class Meta:
        app_label = 'ore'

    node = models.ForeignKey(Node)
    setting = models.TextField()
    configuration = models.ForeignKey(
        Configuration,
        related_name='node_configurations')
