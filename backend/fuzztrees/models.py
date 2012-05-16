from django.db import models
from django.contrib.auth.models import User

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

NODE_TYPE = (
    ( 1, u'Basic event'),			
    ( 2, u'Undeveloped event'),		
    ( 3, u'House event'),			
    ( 4, u'AND gate'),				
    ( 5, u'OR gate'),				
    ( 6, u'XOR gate'),				
    ( 7, u'Priority AND gate'),		
    ( 8, u'Voting OR gate'),		
    ( 9, u'Inhibit gate'),			
    (10, u'Choice event'),			
    (11, u'Redundancy event'),		
    (12, u'Block')					
)

NODE_JS_TYPE = {
	 1: 'basic',
	 2: 'undeveloped',
	 3: 'house',
	 4: 'and',
	 5: 'or',
	 6: 'xor',
	 7: 'p-and',
	 8: 'v-or',
	 9: 'inhibit',
	10: 'choice',
	11: 'redundancy',
	12: 'block'
}

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
	type = models.PositiveSmallIntegerField(choices=NODE_TYPE)
	optional = models.BooleanField(default=False)
	def __unicode__(self):
		if self.type == 1:
			if self.root:
				return self.name+" (root)"
			else:
				return self.name
		else:
			return NODE_JS_TYPE[self.type]+"_"+str(self.pk)
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

		