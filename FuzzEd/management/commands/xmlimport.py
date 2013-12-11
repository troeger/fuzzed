from django.core.management.base import BaseCommand
from FuzzEd.models import Graph
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = '<user_name> <type> <graph_id>'
    help = 'Imports the given XML as new graph'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=args[0])
        except:
            print "Unknown user, try one of these:"
            print User.objects.all()
            exit(1)
        assert(args[1] in ('faulttree','fuzztree'))
        graph = Graph(owner=user, kind=args[1])
        graph.save()
        xmldata=open(args[2]).read()
        graph.from_xml(xmldata)
        # Sanity check
        print "#########################"
        print graph.to_xml()
        print "#########################"
        print xmldata


