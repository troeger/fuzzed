from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from graph import Graph
import notations

class Node(models.Model):
    """
    Node class

    This class models a generic node of a diagram notation.

    Attributes:
    client_id -- an additional id for this node as received from the client (integer)
    kind      -- a unique identifier for the kind of this node, e.g. start_event; 
                 must be from the set of available kinds defined in the notations (string, required)
    graph     -- link to the graph that contains this node (Graph, required)
    x         -- the x coordinate of the node (integer, required, default: 0)
    y         -- the y coordinate of the node (integer, required, default: 0) 
    deleted   -- flag indicating whether this node was deleted and therefore is hidden (boolean, required, default: False)
    """
    class Meta:
        app_label = 'FuzzEd'

    client_id = models.BigIntegerField(default=0)  # top nodes always get the 0 ID, frontend must not reassign the 0
    kind      = models.CharField(max_length=127, choices=notations.node_choices)
    graph     = models.ForeignKey(Graph, null=False, related_name='nodes')
    x         = models.IntegerField(default=0)
    y         = models.IntegerField(default=0)
    deleted   = models.BooleanField(default=False)

    def __unicode__(self):
        try:
            return Property.objects.get(node=self, key='name').value

        except ObjectDoesNotExist:
            return '%s_%s' % (notations.by_kind[graph.kind]['nodes'][kind]['name'], self.pk)

    def to_json(self):
        """
        Serializes the values of this node into a python dictionary that is JSON conform.

        Returns:
        dictionary
        """
        serialized = dict([prop.to_tuple() for prop in self.properties.all().filter(deleted=False)])

        serialized['id']            = self.client_id
        serialized['kind']          = self.kind
        serialized['outgoingEdges'] = [edge.to_json() for edge in self.outgoing.all().filter(deleted=False)]

        return serialized

    def get_children(self):
        """
        Retrieves all nodes that are directly or transitively targets of edges that 
        origin from this node. The nodes are encoded as dictionaries (refer: get_tree()).
        If there are no edges present then None is returned.

        Returns
        list(dict)
        """
        edges = self.outgoing.all().filter(deleted=False)

        if edges:
            return [edge.target.get_tree() for edge in edges]
        return None

    def get_tree(self):
        """
        Serializes this node into nested dictionaries that represent the tree which
        root is the node itself.

        Returns:
        dict
        """
        return {
            'id':       self.pk,
            'name':     unicode(self),
            'children': self.get_children()
        }