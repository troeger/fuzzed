from django.core.management.base import BaseCommand
from FuzzEd.models import Graph
import tempfile, os, shutil

class Command(BaseCommand):
    args = '<graph_id>'
    help = 'Dumps the graph with the given ID into PDF, through TIKZ / Latex'

    def handle(self, *args, **options):
        graph_id = int(args[0])
        # perform Latex compilation in temporary directory
        tmpdir = tempfile.mkdtemp() 
        # Dump tikz Latex from graph and store it there
        tmpfile = tmpdir+os.sep+'graph.tex'        
        print('Dumping graph %d to %s' % (graph_id, tmpfile))
        f = open(tmpfile,'w')
        text = Graph.objects.get(pk=graph_id).to_tikz()
        f.write(text)
        f.close()
        # Copy the neccessary image files for Latex compilation
        #TODO: This should be smarter
        for root, dirs, files in os.walk('FuzzEd/static/img/faulttree'):
            for f in files:
                if f.endswith('.eps'):
                    print "Copying "+f
                    shutil.copy(root+os.sep+f, tmpdir)
        # Run Latex, copy result pdf document to current directory
        # pdflatex really sucks in being run with files in another directory,
        # so we simply got their for the time being
        olddir = os.getcwd()
        os.chdir(tmpdir)
        os.system("pdflatex graph.tex")
        os.chdir(olddir)
        shutil.copy(tmpdir+os.sep+"graph.pdf",".")
        shutil.rmtree(tmpdir, ignore_errors=True)
