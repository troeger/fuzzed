from django.core.exceptions import ObjectDoesNotExist

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

import logging
logger = logging.getLogger('FuzzEd')

from xml_fuzztree import *
#TopEvent_ as XmlTopEvent, BasicEvent_ as XmlBasicEvent, And_ as XmlAndGate, Or_ as XmlOrGate, Xor_ as XmlXorGate, VotingOr_ as XmlVotingOrGate, CrispProbability_ as XmlCrispProbability

try:
    import json
# backwards compatibility with older versions of Python
except ImportError:
    import simplejson as json
import sys, ast, time

from graph import Graph
import notations

def new_client_id():
    return str( int(time.mktime(time.gmtime())))

# TODO: CREATE ALL THE PROPERTIES OF THIS NODE ON CREATION (OR FACTORY METHOD?)

class Node(models.Model):
    """
    Class: Node

    This class models a generic node for any diagram notation.

    Fields:
     {long}    client_id - an id for this node that is generated by the client
     {str}     kind      - a unique identifier for the kind of the node in its notation - e.g. "choice" for FuzzTrees. Must be in the set of available node kinds of the owning graph's notation
     {<Graph>} graph     - the graph that owns the node
     {int}     x         - the x coordinate of the node (default: 0)
     {int}     y         - the y coordinate of the node (default: 0) 
     {bool}    deleted   - flag indicating whether this node is deleted. Simpilifies restoration of nodes by toggling the flag (default: False)
    """
    class Meta:
        app_label = 'FuzzEd'

    # Nodes that are created by the server (e.g. default nodes in the notation) should receive ids
    # starting at -sys.maxint and autoincrement from there on. The whole negative number range is 
    # reserved for the server. IDs from the client MUST be zero or greater (usually UNIX timestamp 
    # in milliseconds from JS)
    client_id = models.BigIntegerField(default=-sys.maxint)
    kind      = models.CharField(max_length=127, choices=notations.node_choices)
    graph     = models.ForeignKey(Graph, null=False, related_name='nodes')
    x         = models.IntegerField(default=0)
    y         = models.IntegerField(default=0)
    deleted   = models.BooleanField(default=False)

    def __unicode__(self):
        prefix = '[DELETED] ' if self.deleted else ''
        try:
            name = unicode(self.properties.get(key='name').value)
            return unicode('%s%s' % (prefix, name))

        except ObjectDoesNotExist:
            return unicode('%s%s_%s' % (prefix, self.pk, notations.by_kind[self.graph.kind]['nodes'][self.kind]['name']))

    def to_json(self):
        """
        Method: to_json
        
        Serializes the values of this node into JSON notation.

        Returns:
         {str} the node in JSON representation
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Method: to_dict
        
        Serializes this node into a native dictionary
        
        Returns:
         {dict} the node as dictionary
        """
        serialized = dict([prop.to_tuple() for prop in self.properties.filter(deleted=False)])

        serialized['id']       = self.client_id
        serialized['kind']     = self.kind
        serialized['x']        = self.x
        serialized['y']        = self.y
        serialized['outgoing'] = [edge.client_id for edge in self.outgoing.filter(deleted=False)]
        serialized['incoming'] = [edge.client_id for edge in self.incoming.filter(deleted=False)]

        return serialized

    def to_bool_term(self):
        edgeset = self.outgoing.filter(deleted=False).all()
        children=[]
        for edge in edgeset:
            children.append(edge.target.to_bool_term())
        if self.kind == 'orGate':
            return "("+" or ".join(children)+")"
        elif self.kind == 'andGate':        
            return "("+" and ".join(children)+")"
        elif self.kind in ['basicEvent']:
            return str(self.client_id)
        elif self.kind == 'topEvent':
            return str(children[0])
        else:
            raise ValueError('Node %s has unsupported kind' % (str(self)))

    def to_xml(self):
        """
        Method: to_xml
        
        Serializes this node into an XML representation according to the schema file for the graph type
        
        Returns:
         the node object
        """
        try:
            name = self.properties.get(key='name').value
        except:
            name = ""
        if self.kind == 'topEvent':
            logger.debug("Adding top event XML")
            xmlnode = TopEvent(id=self.id, name=name)
        elif self.kind == 'andGate':
            logger.debug("Adding AND gate XML")
            xmlnode = And(id=self.id, name=name)
        elif self.kind == 'orGate':
            logger.debug("Adding OR gate XML")
            xmlnode = Or(id=self.id, name=name)
        elif self.kind == 'xorGate':
            logger.debug("Adding XOR gate XML")
            xmlnode = Xor(id=self.id, name=name)
        elif self.kind == 'votingOrGate':
            logger.debug("Adding %s XML with properties: %s"%(self.kind, str(self.properties.all())))
            try:
                kN = int(self.properties.get(key='kN').value)
            except:
                default = notations.by_kind[self.graph.kind]['nodes']['votingOrGate']['kN']
                logger.debug("No costs for this node, using default "+str(default))
                kN = default
            xmlnode = VotingOr(id=self.id, name=name, k=kN[0])
        elif self.kind == 'basicEvent' or self.kind == 'basicEventSet':
            logger.debug("Adding %s XML with properties: %s"%(self.kind, str(self.properties.all())))
            try:
                costs = int(self.properties.get(key='cost').value)
            except:
                default = notations.by_kind[self.graph.kind]['nodes']['event']['cost']
                logger.debug("No costs for this node, using default "+str(default))
                costs = default
            try:
                prob = self.properties.get(key='probability').value
                if prob[1] == 0:
                    probability = CrispProbability(value_=prob[0])
                else:
                    probability = TriangularFuzzyInterval(a=prob[0]-prob[1],b1=prob[0],b2=prob[0],c=prob[0]+prob[1])
            except:
                default = notations.by_kind[self.graph.kind]['nodes']['basicEvent']['propertyMenuEntries']['probability']['defaults']['Exact']
                logger.debug("No probability for this node, using default value "+str(default))
                probability = CrispProbability(value_=default[0])
            if self.kind == 'basicEvent':
                xmlnode=BasicEvent(id=self.id, name=name, costs=costs, probability=probability)
            elif self.kind == 'basicEventSet':
                xmlnode=BasicEventSet(id=self.id, name=name, costs=costs, probability=probability)
        elif self.kind == 'intermediateEvent':
            logger.debug("Adding intermediate event XML")
            xmlnode=IntermediateEvent(id=self.id, name=name)
        elif self.kind == 'intermediateEventSet':
            logger.debug("Adding intermediate event set XML")
            xmlnode=IntermediateEventSet(id=self.id, name=name)
        elif self.kind == 'undevelopedEvent':
            logger.debug("Adding undeveloped event XML")
            xmlnode=UndevelopedEvent(id=self.id, name=name)
        elif self.kind == 'choiceEvent':
            logger.debug("Adding choice event XML")
            xmlnode=ChoiceEvent(id=self.id, name=name)
        elif self.kind == 'redundancyEvent':
            logger.debug("Adding %s XML with properties: %s"%(self.kind, str(self.properties.all())))
            try:
                kFormula = int(self.properties.get(key='kFormula').value)
            except:
                default = notations.by_kind[self.graph.kind]['nodes']['redundancyEvent']['kFormula']
                logger.debug("No kFormula for this node, using default "+str(default))
                kFormula = default
            try:
                nRange = int(self.properties.get(key='nRange').value)
            except:
                default = notations.by_kind[self.graph.kind]['nodes']['redundancyEvent']['nRange']
                logger.debug("No nRange for this node, using default "+str(default))
                nRange = default
            xmlnode=RedundancyGate(id=self.id, name=name, formula=kFormula, start=nRange[0], end=nRange[1])
        elif self.kind == 'houseEvent':
            logger.debug("Adding %s XML with properties: %s"%(self.kind, str(self.properties.all())))
            try:
                costs = int(self.properties.get(key='cost').value)
            except:
                default = notations.by_kind[self.graph.kind]['nodes']['event']['cost']
                logger.debug("No costs for this node, using default "+str(default))
                costs = default
            try:
                prob = self.properties.get(key='probability').value
                if prob[1] == 0:
                    probability = CrispProbability(value_=prob[0])
                else:
                    probability = TriangularFuzzyInterval(a=prob[0]-prob[1],b1=prob[0],b2=prob[0],c=prob[0]+prob[1])
            except:
                default = notations.by_kind[self.graph.kind]['nodes']['basicEvent']['propertyMenuEntries']['probability']['defaults']['Exact']
                logger.debug("No probability for this node, using default value "+str(default))
                probability = CrispProbability(value_=default[0])
            xmlnode=HouseEvent(id=self.id, name=name, costs=costs, probability=probability)
        else:
            raise ValueError('Unsupported node %s for xml serialization'%str(self))
        outgoing = self.outgoing.filter(deleted=False)
        for edge in outgoing:
            xmlnode.children.append(edge.target.to_xml())
        return xmlnode

    def get_attr(self, key):
        """
        Method: get_attr

        Use this method to fetch a node's attribute. It looks in the node object and its related properties.

        Parameters:
            {string} key - The name of the attribute.

        Returns:
            {attr} The found attribute. Raises a ValueError if no attribute for the given key exist.
        """
        if hasattr(self, key):
            return getattr(self, key)
        else:
            try:
                prop = self.properties.get(key=key)
                return prop.value
            except Exception:
                raise ValueError()

    def set_attr(self, key, value):
        """
        Method: set_attr

        Use this method to set a node's attribute. It looks in the node object and its related properties for
        an attribute with the given name and changes it. If non exist, a new property is added saving this attribute.

        Parameters:
            {string} key - The name of the attribute.
            {attr} value - The new value that should be stored.
        """
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            prop, created = self.properties.get_or_create(key=key)
            prop.value = value
            prop.save()

# the handler will ensure that the kind of the node is present in its containing graph notation
@receiver(pre_save, sender=Node)
def validate(sender, instance, raw, **kwargs):
    # raw is true if fixture loading happens, where the graph does not exist so far
    if not raw:
        graph = instance.graph
        if not instance.kind in notations.by_kind[graph.kind]['nodes']:
            raise ValueError('Graph %s does not support nodes of type %s' % (graph, instance.kind))

# ensures that the validate handler is not exported
__all__ = ['Node']
