from django.core.management.base import BaseCommand
from FuzzEd.models import Graph, Project
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = '<user_name> <type> <graph_file>'
    help = 'Imports the given GraphML as new graph'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=args[0])
        except:
            print "Unknown user, try one of these:"
            print User.objects.all()
            exit(1)
        assert(args[1] in ('faulttree','fuzztree'))
        project = Project(owner=user, name="Imported graph")
        project.save()
        graph = Graph(owner=user, kind=args[1], project=project)
        graph.save()
        xmldata=open(args[2]).read()
        graph.from_graphml(xmldata)
        print "Graph created, ID is %u"%graph.pk


