import json
import datetime
import sys

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.db import models

from FuzzEd.models import Node, Graph


class NodeGroup(models.Model):

    class Meta:
        app_label = 'FuzzEd'

    client_id = models.BigIntegerField(default=-sys.maxsize)
    graph = models.ForeignKey(Graph, null=False, related_name='groups')
    nodes = models.ManyToManyField(Node)
    deleted = models.BooleanField(default=False)

    def to_dict(self, use_value_dict=False):
        if use_value_dict:
            prop_values = {prop.key: {'value': prop.value}
                           for prop in self.properties.filter(deleted=False)}
        else:
            prop_values = {
                prop.key: prop.value for prop in self.properties.filter(
                    deleted=False)}

        return {'id': self.client_id,
                'nodeIds': [node.client_id for node in self.nodes.all()],
                'properties': prop_values,
                }

    def to_json(self, use_value_dict=False):
        return json.dumps(self.to_dict(use_value_dict))

    def get_property(self, key, default=None):
        try:
            return self.properties.get(key=key).get_value()
        except ObjectDoesNotExist:
            node_kind = nodes.all()[0].kind
            logger.debug(
                "Assuming node kind %s for node group properties" %
                node_kind)
            try:
                prop = notations.by_kind[
                    self.graph.kind]['nodes'][node_kind]['properties'][key]
                if prop is None:
                    logger.warning(
                        'Notation configuration has empty default for node property ' +
                        key)
                    result = default
                else:
                    result = prop['default']
                logger.debug(
                    'Node has no property "%s", using default "%s"' %
                    (key, str(result)))
                return result
            except KeyError:
                logger.debug(
                    'No default given in notation, using given default "%s" instead' %
                    default)
                return default
        except MultipleObjectsReturned:
            logger.error(
                "ERROR: Property %s in node group %u exists in multiple instances" %
                (key, self.pk))
            raise MultipleObjectsReturned()

    def set_attr(self, key, value):
        """
        Method: set_attr

        Use this method to set a group's attribute. It looks in the group object and its related properties for an
        attribute with the given name and changes it. If non exist, a new property is added saving this attribute.

        Parameters:
            {string} key - The name of the attribute.
            {attr} value - The new value that should be stored.

        TODO: Deprecate this method, set_attrs() should only be used to have an efficient modification signal handling.
        """
        assert(self.pk)
        from FuzzEd.models import Property
        if hasattr(self, key):
            # Native NodeGroup attribute, such as client_id
            setattr(self, key, value)
        else:
            prop, created = self.properties.get_or_create(
                key=key, defaults={
                    'node_group': self})
            prop.save_value(value)

    def set_attrs(self, d):
        '''
            Set groups attributes according to the provided dictionary.

            TODO: Replace by true bulk insert implementation.
        '''
        for key, value in d.items():
            self.set_attr(key, value)
        post_save.send(sender=self.__class__, instance=self)

    def same_as(self, group):
        '''
            Checks if this group is equal to the given group in terms of nodes and attributes.
            This is a very expensive operation that is only intended for testing purposes.
        '''
        for my_node in self.nodes.all().filter(deleted=False):
            found_match = False
            for their_node in group.nodes.all().filter(deleted=False):
                if my_node.same_as(their_node):
                    found_match = True
                    break
            if not found_match:
                return False
        return True


@receiver(post_save, sender=NodeGroup)
@receiver(pre_delete, sender=NodeGroup)
def graph_modify(sender, instance, **kwargs):
    instance.graph.modified = datetime.datetime.now()
    instance.graph.save()
    # updating project modification date
    instance.graph.project.modified = instance.graph.modified
    instance.graph.project.save()
