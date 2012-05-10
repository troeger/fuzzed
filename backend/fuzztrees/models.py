from django.db import models
from django.contrib.auth.models import User

class Diagram(models.Model):
	owner = models.ForeignKey(User, related_name='diagrams')

class Graph(models.Model):
	diagram = models.ForeignKey(Diagram, related_name='graphs')

class Node(models.Model):
	graph = models.ForeignKey(Graph, null=False, related_name='nodes')
	
class Edge(models.Model):
	src  = models.ForeignKey(Node, null=False, related_name='outgoing')
	dest = models.ForeignKey(Node, null=False, related_name='incoming')

class Property(models.Model):
	node = models.ForeignKey(Node, null=True, related_name='properties')
	edge = models.ForeignKey(Edge, null=True, related_name='properties')
	key = models.CharField(max_length=255)
	val = models.CharField(max_length=255)
