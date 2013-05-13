from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

import pyxb.utils.domutils
from xml_fuzztree import FuzzTree as XmlFuzzTree, Namespace as XmlFuzzTreeNamespace
from xml_faulttree import FaultTree as XmlFaultTree, Namespace as XmlFaultTreeNamespace

import json, notations

class Graph(models.Model):
    """
    Class: Graph

    This class models a generic graph that is suitable for any diagram notation. It basically serves a container for
    its contained nodes and edges. Additionally, it provides functionality for serializing it.

    Fields:
     {str}            kind     - unique identifier that indicates the graph's notation (e.g. fuzztree). Must be an
                                 element of the set of available notations (See also: <notations>)
     {str}            name     - the name of the graph
     {User}           owner    - a link to the owner of the graph
     {const datetime} created  - timestamp of the moment of graph creation (default: now)
     {bool}           deleted  - flag indicating whether this graph was deleted or not. Simplifies restoration of the
                                 graph if needed by toggling this member (default: False)
    """
    class Meta:
        app_label = 'FuzzEd'

    kind    = models.CharField(max_length=127, choices=notations.choices)
    name    = models.CharField(max_length=255)
    owner   = models.ForeignKey(User, related_name='graphs')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode('%s%s' % ('[DELETED] ' if self.deleted else '', self.name))

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
        
        Encodes the whole graph as dictionary having five top level items: its id, name, type and two lists containing
        all edges and nodes in the graph
        
        Returns:
         {dict} the graph as dictionary
        """
        node_set = self.nodes.filter(deleted=False)
        edge_set = self.edges.filter(deleted=False)
        nodes   = [node.to_dict() for node in node_set]
        edges   = [edge.to_dict() for edge in edge_set]

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

    def to_xml(self, xmltype=None):
        """
        Method: to_xml
            Serializes the graph into its XML representation.

        Returns:
            {string} The XML representation of the graph
        """
        if xmltype:
            kind=xmltype
        else:
            kind=self.kind
        if kind == "fuzztree":
            tree = XmlFuzzTree(name = self.name, id = self.pk)
            pyxb.utils.domutils.BindingDOMSupport.DeclareNamespace(XmlFuzzTreeNamespace, 'fuzzTree')
        elif kind == "faulttree":
            tree = XmlFaultTree(name = self.name, id = self.pk)
            pyxb.utils.domutils.BindingDOMSupport.DeclareNamespace(XmlFaultTreeNamespace, 'faultTree')
        else:
            raise ValueError('No XML support for this graph type.')

        # Find root node and start from there
        top_event = self.nodes.get(kind='topEvent')
        tree.topEvent = top_event.to_xml(kind)

        return unicode(tree.toxml('utf-8'),'utf-8')

# validation handler that ensures that the graph kind is known
@receiver(pre_save, sender=Graph)
def validate_kind(sender, instance, **kwargs):
    if not instance.kind in notations.by_kind:
        raise ValueError('Graph %s may not be of kind %s' % (instance, instance.kind))

# ensures that the signal handler are not exported
__all__ = ['Graph']
