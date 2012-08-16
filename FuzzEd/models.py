import random

import django.contrib.auth.models as auth
import django.core.exceptions as exceptions
import django.db.models as models
import django.shortcuts as shortcuts

import nodes_config as config

class GraphTypes(object):
    FAULT_TREE = 1
    FUZZ_TREE  = 2
    RBD        = 3

GRAPH_TYPE = (
    (GraphTypes.FAULT_TREE, u'Fault Tree'),
    (GraphTypes.FUZZ_TREE,  u'FuzzTree'),    
    (GraphTypes.RBD,        u'Reliability Block Diagram')
)

GRAPH_JS_TYPE = {
    1: 'faulttree',
    2: 'fuzztree',
    3: 'rbd'
}

class Commands():
    ADD_GRAPH          = 1
    ADD_NODE           = 2
    ADD_EDGE           = 3
    DELETE_GRAPH       = 4
    DELETE_NODE        = 5
    DELETE_EDGE        = 6    
    CHANGE_COORDINATES = 7
    CHANGE_PROP        = 8
    GROUP              = 9

COMMAND_TYPE = (
    (Commands.ADD_GRAPH,          'Add graph'),      
    (Commands.ADD_NODE,           'Add node'),        
    (Commands.ADD_EDGE,           'Add edge'),        
    (Commands.DELETE_GRAPH,       'Delete graph'),       
    (Commands.DELETE_NODE,        'Delete node'),         
    (Commands.DELETE_EDGE,        'Delete edge'),
    (Commands.CHANGE_COORDINATES, 'Change node coordinates'),
    (Commands.CHANGE_PROP,        'Change node property'),
    (Commands.GROUP,              'Start of command group')      
)

class UserProfile(models.Model):
    user       = models.OneToOneField(auth.User)
    newsletter = models.BooleanField(default=False)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=auth.User)


def create_fuzztree(owner, title):
    # create graph
    graph = Graph(type=GraphTypes.FUZZ_TREE, owner=owner)
    graph.save_creation()

    # set graph name, without change history
    title_property = Property(graph=graph, key='name', value=title)
    title_property.save()

    # create root node
    node = Node(graph=graph, type=config.NODE_TYPE_IDS['topEvent'], xcoord=10, ycoord=1)
    node.save_creation()

    # set root node name, disable configurability indication
    name_property = Property(node=node)
    name_property.save_change('name', 'System Failure')

    optional_property = Property(node=node)
    optional_property.save_change('optional', 'undefined')

def delete_graph(graph):
    graph.deleted = True
    graph.save_deletion()

def rename_graph(graph, new_name):
    name_property = shortcuts.get_object_or_404(Property, graph=graph, key='name')
    name_property.save_change('name', new_name)

def set_node_property(node, key, value):
    node_property, created = Property.objects.get_or_create(node=node, key=key, defaults={'value': value})
    if not created:
        node_property.save_change(key, value)