from django.core.management.base import BaseCommand, CommandError
from FuzzEd.models import Graph

class Command(BaseCommand):
	args = '<graph_id>'
	help = 'Dumps the graph with the given ID into XML'

	def handle(self, *args, **options):
		graphid=int(args[0])
		print("Dumping graph %u"%(graphid))
		g=Graph.objects.get(pk=graphid)
		print g.to_xml()
