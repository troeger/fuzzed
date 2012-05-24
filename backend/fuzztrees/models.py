from django.db import models
from django.contrib.auth.models import User

from nodes_config import NODE_TYPES, nodeTypeChoices

GRAPH_TYPE = (
    ( 1, u'Fault Tree'),
    ( 2, u'Fuzz Tree'),	
    ( 3, u'Reliability Block Diagram')
)

GRAPH_JS_TYPE = {
	1: 'faulttree',
	2: 'fuzztree',
	3: 'rbd'
}

COMMAND_TYPE = (
	(1, 'Add graph'),		# graph type ID in numeric field
	(2, 'Add node'), 		# parent node in node field, graph in graph field, node type in numeric field
	(3, 'Delete node')		# graph in graph field, node in node field
)

class Graph(models.Model):
	name = models.CharField(max_length=255)
	owner = models.ForeignKey(User, related_name='graphs')
	type = models.PositiveSmallIntegerField(choices=GRAPH_TYPE)
	def __unicode__(self):
		return self.name

class Node(models.Model):
	name = models.CharField(max_length=255)
	graph = models.ForeignKey(Graph, null=False, related_name='nodes')
	root = models.BooleanField(default=False)
	type = models.PositiveSmallIntegerField(choices=nodeTypeChoices())
	optional = models.BooleanField(default=False)
	def __unicode__(self):
		if self.type == 1:
			if self.root:
				return self.name+" (root)"
			else:
				return self.name
		else:
			return NODE_TYPES[self.type]['type'] + "_" + str(self.pk)
	def getChildren(self):
		edges=self.outgoing.all()
		if len(edges)>0:
			return [e.dest.getTreeDict() for e in edges]
		else:
			return ''
	def getTreeDict(self):
		d={'id':self.pk,'name':self.name}
		kids=self.getChildren()
		if kids:
			d['children']=kids
		return d

class Edge(models.Model):
	src  = models.ForeignKey(Node, null=False, related_name='outgoing')
	dest = models.ForeignKey(Node, null=False, related_name='incoming')
	def __unicode__(self):
		return str(self.src) + "->" + str(self.dest)

class Property(models.Model):
	node = models.ForeignKey(Node, null=True, related_name='properties')
	edge = models.ForeignKey(Edge, null=True, related_name='properties')
	key = models.CharField(max_length=255)
	val = models.CharField(max_length=255)
	def __unicode__(self):
		if self.node:
			return "Node "+str(node)+":%s = %s"%(self.key, self.val)
		else:
			return "Edge "+str(node)+":%s = %s"%(self.key, self.val)

class History(models.Model):
	command = models.PositiveSmallIntegerField(choices=COMMAND_TYPE, null=False)
	numeric = models.IntegerField() 		
	text1 = models.CharField(max_length=255)
	text2 = models.CharField(max_length=255)
	graph = models.ForeignKey(Graph, null=True, related_name='commands')
	node = models.ForeignKey(Node, null=True)
	insert_date = models.DateTimeField(null=False, blank=False, auto_now_add=True, editable=False)
	modification_date = models.DateTimeField(null=False, blank=False, auto_now=True, editable=False)
