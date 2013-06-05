from django.core.management.base import BaseCommand
import svg2tikz, os

class Command(BaseCommand):
    args = '<SVG file>'
    help = 'Converts the node SVG files to their TIKZ counterparts'

    def handle(self, *args, **options):
        for d in ['faulttree','fuzztree','rbd']:
            for root, dirs, files in os.walk('FuzzEd/static/img/'+d):
                print "Scanning "+root        
                for f in files:
                    if f.endswith(".svg"):
                        svg = open(root+os.sep+f).read()
                        tikzText = svg2tikz.convert_svg(svg)
                        start=tikzText.find("\\begin{document}")
                        end=tikzText.find("\\end{document}")
                        destname=root+'/'+f[:f.rfind('.')]+'.tikz'
                        print "Writing to "+destname
                        destfile=open(destname,'w')
                        tikzText = tikzText[start+17:end]
                        destfile.write(tikzText)
                        destfile.close()

