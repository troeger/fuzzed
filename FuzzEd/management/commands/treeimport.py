from django.core.management.base import BaseCommand, CommandError
from FuzzEd.models import Graph, Node, Edge, Property
from django.contrib.auth.models import User

def gen_client_id():
	i=1
	while(True):
		yield i
		i=i+1

class Command(BaseCommand):
	args = '<owner> <textfile>'
	help = 'Imports a fault tree in European Benchmark Fault Trees Format, see http://bit.ly/UrAxM1'
	got_rootgate=False
	nodes = {}
	g = None
	gate_x=0
	event_x=0
	client_id=gen_client_id()

	def getid(self, title):
		if '/' in title:
			return title[title.find(')')+1:]
		else:
			return filter(lambda x: x.isdigit(), title)

	def addNode(self, title, lineno):
		lineno=lineno+10
		nodeid=self.getid(title)
		if nodeid not in self.nodes.keys():
			#TODO: Use some reasonable X / Y coordinates			
			if "*" in title:
				self.gate_x=self.gate_x+1
				self.nodes[nodeid] = Node(graph=self.g, x=self.gate_x, y=lineno, kind="andGate", client_id=self.client_id.next())
			elif "+" in title:
				self.gate_x=self.gate_x+1
				self.nodes[nodeid] = Node(graph=self.g, x=self.gate_x, y=lineno, kind="orGate", client_id=self.client_id.next())
			elif "/" in title:
				self.gate_x=self.gate_x+1
				self.nodes[nodeid] = Node(graph=self.g, x=self.gate_x, y=lineno, kind="votingOrGate", client_id=self.client_id.next())
			elif title.startswith("T"):
				self.event_x=self.event_x+1
				self.nodes[nodeid] = Node(graph=self.g, x=self.event_x, y=lineno, kind="basicEvent", client_id=self.client_id.next())							
			self.nodes[nodeid].save()
			prob=Property(key="title", value=title, node=self.nodes[nodeid])
			prob.save()
			if not self.got_rootgate:
				# connect the very first gate to the top event
				rootnode = Node.objects.get(kind__exact = 'topEvent', graph=self.g)
				n=Edge(graph=self.g, source=rootnode, target=self.nodes[nodeid], client_id=self.client_id.next())
				n.save()
				self.got_rootgate=True

	def handle(self, *args, **options):
		uname="admin"
		fname="FuzzEd/fixtures/europe-1.txt"
		if len(args)==1:
			uname=args[0]
		elif len(args)==2:
			uname=args[0]
			fname=args[1]
		owner = User.objects.get(username__exact = uname)
		data=open(fname)
		self.g=Graph(name=fname.split("/")[-1], kind="fuzztree", owner=owner)
		self.g.save()
		for lineno, line in enumerate(data):
			if line.startswith("G"):
				# Gate node
				linenodes=[el for el in line.rstrip("\n").split(" ") if el != '']
				for ln in linenodes:
					self.addNode(ln, lineno)
				# Add edges now, since all nodes in the line are in the DB
				parent=self.nodes[self.getid(linenodes[0])]
				for ln in linenodes[1:]:
					n=Edge(graph=self.g, source=parent, target=self.nodes[self.getid(ln)], client_id=self.client_id.next())
					n.save()
			elif line.startswith("T"):
				# Basic event node with probability
				title, prob = line.split(" ")[0:2]
				self.addNode(title, lineno)
				prob=Property(key="probability", value=str(float(prob)), node=self.nodes[self.getid(title)])
				prob.save()
		#orphans=Node.objects.filter(graph=self.g,incoming=None).exclude(kind__exact='topEvent')
		#for orphan in orphans:
		#	print orphan.properties.all()
		#	n=Edge(graph=self.g, source=rootgate, target=orphan, client_id=self.client_id.next())
		#	n.save()
