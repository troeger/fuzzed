from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

try:
    import json
# backwards compatibility with older versions of Python
except ImportError:
    import simplejson as json
import sys

import notations

class Graph(models.Model):
    """
    Class: Graph

    This class models a generic graph that is suitable for any diagram notation. It basically serves a container for its contained nodes and edges. Additionally, it provides functionality for serializing it.

    Fields:
     {str}            kind     - unique identifier that indicates the graph's notation (e.g. fuzztree). Must be an element of the set of available notations (See also: <notations>)
     {str}            name     - the name of the graph
     {User}           owner    - a link to the owner of the graph
     {const datetime} created  - timestamp of the moment of graph creation (default: now)
     {bool}           deleted  - flag indicating whether this graph was deleted or not. Simplifies restoration of the graph if needed by toggling this member (default: False)
    """
    class Meta:
        app_label = 'FuzzEd'

    kind    = models.CharField(max_length=127, choices=notations.choices)
    name    = models.CharField(max_length=255)
    owner   = models.ForeignKey(User, related_name='graphs')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s%s' % ('[DELETED] ' if self.deleted else '', self.name)

    def to_json(self):
        """
        Method: to_json
        
        Serializes the graph into a JSON object.

        Returns:
         {dict} the graph in JSON representation
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Method: to_dict
        
        Encodes the whole graph as dictionary having five top level items: its id, name, type and two lists containing all edges and nodes in the graph
        
        Returns:
         {dict} the graph as dictionary
        """
        nodeset = self.nodes.filter(deleted=False).all()
        nodes   = [node.to_dict() for node in nodeset]
        edges   = []
        for node in nodeset:
            edgeset = node.outgoing.filter(deleted=False).all()
            edges.extend([edge.to_dict() for edge in edgeset])

        return {
            'id':    self.pk,
            'name':  self.name,
            'type':  self.kind,
            'nodes': nodes,
            'edges': edges
        }

    def to_bool_term(self):
        root = self.nodes.get(kind__exact = 'topEvent')
        return root.to_bool_term()

from commands import AddNode

# validation handler that ensures that the graph kind is known
@receiver(pre_save, sender=Graph)
def validate_kind(sender, instance, **kwargs):
    if not instance.kind in notations.by_kind:
        raise ValueError('Graph %s may not be of kind %s' % (instance, instance.kind))

# preinitialize the graph with default nodes
@receiver(post_save, sender=Graph)
def set_graph_defaults(sender, instance, **kwargs):
    # TODO: find a better way!
    # don't add defaults if it was already done (if there are nodes)
    for node in instance.nodes.all():
        return

    notation = notations.by_kind[instance.kind]
    if not 'defaults' in notation:
        return
    defaults = notation['defaults']

    # create default nodes for this graph
    for index, node in enumerate(defaults['nodes']):
        # use index as node ID
        # this is unique since all other IDs are time stamps
        command = AddNode.create_from(graph_id=instance.pk, node_id=index, **node)
        command.undoable = False
        command.do()

# ensures that the signal handler are not exported
__all__ = ['Graph']