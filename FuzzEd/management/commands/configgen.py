import json
import copy
import collections
import os
import xml.dom.minidom as xml
from django.core.management.base import BaseCommand, CommandError

from FuzzEd.models import notations
from FuzzEd.settings import STATICFILES_DIRS

class Generator(object):
    def __init__(self, config):
        self.config = copy.deepcopy(config)
        self.kind   = config['kind']
        self.nodes  = config['nodes']
        self.__flat__()

    def __flat__(self):
        for node_type, node in self.config['nodes'].items():
            self.__resolve_inheritance__(node_type, node)

    def __resolve_inheritance__(self, node_type, node):
        if ('inherits' in node):
            # resolve parent inheritance
            parent_type = node['inherits']
            parent      = self.config['nodes'][parent_type]
            parent      = self.__resolve_inheritance__(parent_type, parent)
            del node['inherits']

            # merge parent and node
            merged_node = self.__merge__(parent, node)
            self.config['nodes'][node_type] = merged_node

            # return merged node
            return merged_node

        else:
            return node

    def __merge__(self, parent, node):
        merged = copy.deepcopy(parent)
        
        for key, value in node.iteritems():
            if isinstance(value, collections.Mapping):
                merged[key] = self.__merge__(parent.get(key, {}), value)
            else:
                merged[key] = node[key]
        return merged

    def generate(self):
        cwd = os.getcwd()

        for directory in STATICFILES_DIRS:
            # generate the configuration files
            path = '%s/%s/config/%s.json' % (cwd, directory, self.kind)
            handle = open(path, 'w')
            handle.write(json.dumps(self.config))
            print "Writing "+path
            handle.close()

            # adjust the svgs
            for node_kind, node in self.nodes.items():
                if not 'image' in node: continue

                img_path         = '%s/%s/img/nodes/%s' % (cwd, directory, node['image'])

                img_read_handle  = open(img_path, 'r')
                document = xml.parse(img_read_handle)
                img_read_handle.close()

                svg      = document.getElementsByTagName('svg')[0]
                svg.setAttribute('id', node_kind)
                svg.setAttribute('label', node['name'])

                img_write_handle = open(img_path, 'w')
                img_write_handle.write(document.toxml())
                img_write_handle.close()

class Command(BaseCommand):
    help = 'Updates internal data structures when the graph configurations were changed'

    def handle(self, *args, **options):
        for notation in notations.installed:
            Generator(notation).generate()

