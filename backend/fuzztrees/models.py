from django.db import models
from django.contrib.auth.models import User

class Graph(models.Model):
	name = models.CharField(max_length=255)
	owner = models.ForeignKey(User, related_name='graphs')
	def __unicode__(self):
		return self.name

class Node(models.Model):
	name = models.CharField(max_length=255)
	graph = models.ForeignKey(Graph, null=False, related_name='nodes')
	def __unicode__(self):
		return self.name
	def getSubTree(self):
		edges=self.outgoing.all()
		if len(edges)>0:
			return [e.dest.getSubTree() for e in edges]
		else:
			return self

	
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
