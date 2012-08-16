from django.db import models

from node import Node

class Property(models.Model):
    """
    Property class

    This class models the properties (i.e. the attributes) of the nodes of a diagram.
    They are mainly a key-value tuple with additional meta info.

    Attributes:
    key     -- the name of the property (string, required)
    value   -- the value of the property (string, required)
    node    -- node that owns this property (Node, required)
    deleted -- flag indicating whether the property shall be hidden from views (boolean, required, default: False)
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
        Converts this property to a native python tuple.

        Returns:
        tuple(string, string)
        """
        return (self.key, self.value)