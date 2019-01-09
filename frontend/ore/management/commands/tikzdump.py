from django.core.management.base import BaseCommand
from ore.models import Graph


class Command(BaseCommand):
    args = '<graph_id>'
    help = 'Dumps the graph with the given ID into TIKZ'

    def handle(self, *args, **options):
        graph_id = int(args[0])
        graph = Graph.objects.get(pk=graph_id)

        print('Dumping graph %d' % (graph_id))
        print graph.to_tikz()
