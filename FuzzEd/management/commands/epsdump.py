from django.core.management.base import BaseCommand
from FuzzEd.models import Graph
import beanstalkc

class Command(BaseCommand):
    args = '<graph_id>'
    help = 'Dumps the graph with the given ID into EPS through TIKZ / Latex'

    def handle(self, *args, **options):
        # Dump tikz Latex from graph and put it into the rendering tube
        graph_id = int(args[0])
        text = Graph.objects.get(pk=graph_id).to_tikz()
        print text
        b=beanstalkc.Connection()
        b.use('rendering')
        b.watch('renderingResults')
        jobid = b.put(str(text))
        # Wait for result ...
        result = b.reserve()
        f=open('graph.eps','w')
        f.write(result.body)
        f.close()
        result.delete()
        b.close()


