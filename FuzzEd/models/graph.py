from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

try:
    import json
# backwards compatibility with older versions of CPython
except ImportError:
    import simplejson as json

import notations

class Graph(models.Model):
    """
    Class: Graph

    This class models a generic graph that is suitable for any diagram notation. It basically serves a container for its contained nodes and edges. Additionally, it provides functionality for serializing it.

    Fields:
     {str}            kind     - unique identifier that indicates the graph's notation (e.g. fuzztree). Must be an element of the set of available notations (See also: <notations>)
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
        return self.name

    def dump(self, tree=None, indent=0):
        """
        Method: dump
        
        Prints a human readable, nested version of this graph starting from the root node (node without incoming edges). Alternatively, a specific node may be passed.

        Parameters:
         {dict} tree   - a node of this graph encoded as dictionary from where the graph shall be printed. If no node is passed the root node is assumed (default: None)
         {int} indent  - number of space characters the node will be indented on the root level (default: 0)

        Returns:
         {None}
        """
        if not tree:
            root = self.nodes.exclude(incoming_isnull=False)[0]
            tree = root.get_tree()
            print 'Tree dump:'

        print '|' * indent + '-%s (%s)' % (tree['name'], tree['id'])

        if 'children' in tree:
            for subtree in tree['children']:
                self.dump(subtree, indent + 1)

    def to_json(self):
        """
        Method: to_json
        
        Serializes the graph into a JSON object.

        Returns:
         {dict} the graph in JSON representation
        """
        return json.dumps(self.__to_json_dict__())

    def __to_json_dict__(self):
        nodes = [node.__to_json_dict__() for node in self.nodes.all().filter(deleted=False)]
        return {
            'id':    self.pk,
            'name':  unicode(self),
            'type':  self.kind,
            'nodes': nodes
        }

# validation handler that ensures that the graph kind is known
def validate_kind(sender, instance, **kwargs):
    if not instance.kind in notations.by_kind:
        raise ValueError('Graph %s may not be of kind %s' % (instance, instance.kind))

# register the validation handler with django before each attempt to save a graph
models.signals.pre_save.connect(validate_kind, sender=Graph)

__all__ = ['Graph']


from commands import AddNode

@receiver(post_save, sender=Graph)
def __set_graph_defaults__(sender, instance, **kwargs):
    # don't add defaults if it was already done (if there are nodes)
    #TODO: find a better way?
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
        command = AddNode.create_of(graph_id=instance.pk, node_id=index, **node)
        command.do()
