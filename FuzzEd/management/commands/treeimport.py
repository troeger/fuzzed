from django.core.management.base import BaseCommand, CommandError
from FuzzEd.models import Graph, Node, Edge, Property
from django.contrib.auth.models import User

def gen_client_id():
	i=0
	while(True):
		yield i
		i=i+1

class Command(BaseCommand):
	args = '<owner> <textfile>'
	help = 'Imports a fault tree in European Benchmark Fault Trees Format, see http://bit.ly/UrAxM1'
	nodes = {}
	g = None
	gate_x=0
	event_x=0
	client_id=gen_client_id()

	def addNode(self, title, lineno):
		lineno=lineno+10
		if title not in self.nodes.keys():
			#TODO: Use some reasonable X / Y coordinates
			if "*" in title:
				self.gate_x=self.gate_x+1
				self.nodes[title] = Node(graph=self.g, x=self.gate_x, y=lineno, kind="andGate", client_id=self.client_id.next())
			elif "+" in title:
				self.gate_x=self.gate_x+1
				self.nodes[title] = Node(graph=self.g, x=self.gate_x, y=lineno, kind="orGate", client_id=self.client_id.next())
			elif "/" in title:
				self.gate_x=self.gate_x+1
				self.nodes[title] = Node(graph=self.g, x=self.gate_x, y=lineno, kind="votingOrGate", client_id=self.client_id.next())
			elif title.startswith("T"):
				self.event_x=self.event_x+1
				self.nodes[title] = Node(graph=self.g, x=self.event_x, y=lineno, kind="basicEvent", client_id=self.client_id.next())							
			self.nodes[title].save()

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
		# we assume OR root gate
		rootnode = Node.objects.get(kind__exact = 'topEvent', graph=self.g)
		rootgate = Node(graph=self.g, kind='orGate', x=10, y=10, client_id=self.client_id.next())
		rootgate.save()
		n=Edge(graph=self.g, source=rootnode, target=rootgate, client_id=self.client_id.next())
		n.save()
		for lineno, line in enumerate(data):
			if line.startswith("G"):
				# Gate node
				linenodes=[el for el in line.rstrip("\n").split(" ") if el != '']
				for ln in linenodes:
					self.addNode(ln, lineno)
				# Add edges now, since all nodes in the line are in the DB
				parent=self.nodes[linenodes[0]]
				for ln in linenodes[1:]:
					n=Edge(graph=self.g, source=parent, target=self.nodes[ln], client_id=self.client_id.next())
					n.save()
			elif line.startswith("T"):
				# Basic event node with probability
				title, prob = line.split(" ")[0:2]
				self.addNode(title, lineno)
				prob=Property(key="probability", value=str(float(prob)), node=self.nodes[title])
				prob.save()
		orphans=Node.objects.filter(incoming=None).exclude(kind__exact='topEvent')
		print orphans
		for orphan in orphans:
			n=Edge(graph=self.g, source=rootgate, target=orphan, client_id=self.client_id.next())
			n.save()
