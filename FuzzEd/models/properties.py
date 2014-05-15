from django.db import models

from FuzzEd.lib.jsonfield import JSONField
from node import Node
from edge import Edge
from node_group import NodeGroup


class Property(models.Model):
    """
    Class: Property

    This class models generic properties (i.e. attributes) of the nodes of any diagram notation. They are basically
    key-value tuple that allow the dynamic addition or deletion of whole sets of new property names without having to
    alter the schema of nodes.

    Fields:
     {str}    key      - the name of the property
     {json}   value    - the value of the property
     {<Node>} node     - link to the node that owns the property
     {bool}   deleted  - flag indicating whether this property is deleted or not. Simplifies the restoration of this
                        property by just having to toggle this flag (default: False)
    """
    class Meta:
        app_label = 'FuzzEd'

    key        = models.CharField(max_length=255)
    value      = JSONField()
    node       = models.ForeignKey(Node, related_name='properties', blank=True, null=True, default=None)
    edge       = models.ForeignKey(Edge, related_name='properties', blank=True, null=True, default=None)
    node_group = models.ForeignKey(NodeGroup, related_name='properties', blank=True, null=True, default=None)
    deleted    = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s%s: %s' % ('[DELETED] ' if self.deleted else '', self.key, self.value)

    def to_dict(self):
        """
        Method: to_dict

        Converts the property instance into a native dictionary

        Returns:
         {dict} the property as dictionary
        """
        return {self.key: self.value}

    def to_tuple(self):
        """
        Method: to_tuple

        Converts the property instance to a native tuple.

        Returns:
         {tuple(str, str)} the property as tuple
        """
        return (self.key, self.value)

    def same_as(self, prop):
        ''' 
            Checks if this property is equal to the given one. 
        '''
        if self.key != prop.key:
            return False
        return (str(self.value) == str(prop.value))


