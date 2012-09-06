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

	def addNode(self, title):
		if title not in self.nodes.keys():
			#TODO: Use some reasonable X / Y coordinates
			if "*" in title:
				self.gate_x=self.gate_x+1
				self.nodes[title] = Node(graph=self.g, x=self.gate_x, y=5, kind="andGate", client_id=self.client_id.next())
			elif "+" in title:
				self.gate_x=self.gate_x+1
				self.nodes[title] = Node(graph=self.g, x=self.gate_x, y=5, kind="orGate", client_id=self.client_id.next())
			elif "/" in title:
				self.gate_x=self.gate_x+1
				self.nodes[title] = Node(graph=self.g, x=self.gate_x, y=5, kind="votingOrGate", client_id=self.client_id.next())
			elif title.startswith("T"):
				self.event_x=self.event_x+1
				self.nodes[title] = Node(graph=self.g, x=self.event_x, y=10, kind="basicEvent", client_id=self.client_id.next())							
			print self.nodes[title]
			self.nodes[title].save()


	def handle(self, *args, **options):
		assert(len(args)==2)
		owner = User.objects.get(username__exact = args[0])
		data=open(args[1])
		self.g=Graph(name=args[1], kind="faulttree", owner=owner)
		self.g.save()
		for line in data:
			if line.startswith("G"):
				# Gate node
				linenodes=[el for el in line.rstrip("\n").split(" ") if el != '']
				for ln in linenodes:
					self.addNode(ln)
				# Add edges now, since all nodes in the line are in the DB
				parent=self.nodes[linenodes[0]]
				for ln in linenodes[1:]:
					n=Edge(graph=self.g, source=parent, target=self.nodes[ln], client_id=self.client_id.next())
					print n
					n.save()
			elif line.startswith("T"):
				# Basic event node with probability
				title, prob = line.split(" ")[0:2]
				self.addNode(title)
				prob=Property(key="probability", value=str(float(prob)), node=self.nodes[title])
				prob.save()
