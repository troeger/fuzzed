from django.db import models

from node import Node

class Property(models.Model):
    """
    Class: Property

    This class models generic properties (i.e. attributes) of the nodes of any diagram notation.They are basically key-values tuples that allow the dynamic addition or deletion of whole sets of new property names without having to alter the schema of nodes.

    Fields:
     {str}    key      - the name of the property
     {str}    value    - the value of the property
     {<Node>} node     - link to the node that owns the property
     {bool}   deleted  - flag indicating whether this property is deleted or not. Simplifies the restoration of this property by just having to toggle this flag (default: False)
    """
    class Meta:
        app_label = 'FuzzEd'

    key     = models.CharField(max_length=255)
    value   = models.CharField(max_length=255)
    node    = models.ForeignKey(Node, related_name='properties')
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s%s: %s' % ('[DELETED] ' if self.deleted else '', self.key, self.value)

    def to_tuple(self):
        """
        Method: to_tuple
        
        Converts the property instance to a native Python tuple.

        Returns:
         {tuple(str, str)} the property as tuple
        """
        return (self.key, self.value)