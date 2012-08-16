from django.db import models
from django.core.exceptions import ObjectDoesNotExist

import notations

class Graph(models.Model):
    """
    Graph class

    Models a generic graph class for diagrams.

    Attributes:
    kind    -- unique identifier that indicates of which notation this graph is e.g. fuzztree;
               must be an element of the set of available notations (refer: notations module) (string, required)
    owner   -- link to the user that owns this graph (User, required)
    created -- timestamp of the moment this graph was created (datetime, required, constant, default: now)
    deleted -- flag indicating whether this diagram was deleted/hidden from view (boolean, required, default: False)
    """
    class Meta:
        app_label = 'FuzzEd'

    kind    = models.CharField(max_length=127, choices=notations.choices)
    owner   = models.ForeignKey(auth.User, related_name='graphs')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        try:
            Property.objects.get(graph=self, key='name').value

        except ObjectDoesNotExist:
            return 'Graph_%s' % (self.pk)

    def dump(self, tree=None, indent=0):
        """
        Prints a indented version of this graph starting at the root node (node without incoming edges)
        or a specific if passed.

        Arguments:
        tree   -- a node encoded as dictionary from where the graph shall be printed;
                  if no specific node is passed the root node is assumed (dictionary, default: None)
        indent -- the number of space characters the tree is indented with when printed;
                  in general no indention is assumed (integer, default: 0)

        Returns:
        None
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
        Serializes the graph into a Python dictionary that is JSON conform.
        
        Returns:
        dictionary
        """
        nodes = [node.to_json() for node in self.nodes.all().filter(deleted=False)]
        return {
            'id':    self.pk, 
            'name':  unicode(self), 
            'type':  self.kind, 
            'nodes': nodes
        }