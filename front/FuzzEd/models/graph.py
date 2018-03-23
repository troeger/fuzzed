from django.contrib.auth.models import User
from django.db import models
from django.db.models.aggregates import Max

import pyxb.utils.domutils
import json

try:
    from .xml.fuzztree import FuzzTree as XmlFuzzTree, Namespace as XmlFuzzTreeNamespace, CreateFromDocument as fuzzTreeFromXml
    from .xml.faulttree import FaultTree as XmlFaultTree, Namespace as XmlFaultTreeNamespace, CreateFromDocument as faultTreeFromXml
    from .node_rendering import tikz_shapes
except Exception:
    print("ERROR: Perform a build process first.")
    exit(-1)
from defusedxml.ElementTree import fromstring as parseXml

from .project import Project
from . import notations

import logging
logger = logging.getLogger('FuzzEd')


class Graph(models.Model):

    """
    Class: Graph

    This class models a generic graph that is suitable for any diagram notation. It basically serves a container for
    its contained nodes and edges. Additionally, it provides functionality for serializing it.

    Fields:
     {str}            kind         - unique identifier that indicates the graph's notation (e.g. fuzztree). Must be an
                                     element of the set of available notations (See also: <notations>)
     {str}            name         - the name of the graph
     {User}           owner        - a link to the owner of the graph
     {Project}        project      - the project corresponding to the graph
     {const datetime} created      - timestamp of the moment of graph creation (default: now)
     {bool}           deleted      - flag indicating whether this graph was deleted or not. Simplifies restoration of the
                                     graph if needed by toggling this member (default: False)
     {JSON}           graph_issues -
    """
    class Meta:
        app_label = 'FuzzEd'

    kind = models.CharField(max_length=127, choices=notations.choices)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='graphs')
    project = models.ForeignKey(Project, related_name='graphs')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    read_only = models.BooleanField(default=False)

    def __unicode__(self):
        return str(
            '%s%s' % ('[DELETED] ' if self.deleted else '', self.name))

    def ensure_default_nodes(self):
        """
            Add nodes that are contained in this kind of graph by default,
            in case they are missing.
        """
        notation = notations.by_kind[self.kind]
        if 'defaults' in notation:
            from .node import Node
            for index, default_node in enumerate(
                    notation['defaults']['nodes']):
                default_node.update({'properties': {}})
                # use index as node client ID
                # this is unique since all other client IDs are time stamps
                node, created = Node.objects.get_or_create(kind=default_node['kind'],
                    graph=self, deleted=False,
                    defaults={'client_id':int(index), 
                        'x':default_node['x'],
                        'y':default_node['y']
                    }
                )
                if created:
                    node.save()

    def top_node(self):
        """
        Method: top_node

        Return the top node of this graph, if applicable for the given type.

        Returns:
         {Node} instance
        """
        if self.kind in {'faulttree', 'fuzztree'}:
            return self.nodes.all().get(kind='topEvent')
        else:
            return None

    def to_json(self, use_value_dict=False):
        """
        Method: to_json

        Serializes the graph into a JSON object.

        Returns:
         {dict} the graph in JSON representation
        """
        return json.dumps(self.to_dict(use_value_dict))

    def to_dict(self, use_value_dict=False):
        """
        Method: to_dict

        Encodes the whole graph as dictionary.

        Returns:
         {dict} the graph as dictionary
        """
        node_set = self.nodes.filter(deleted=False)
        edge_set = self.edges.filter(deleted=False)
        group_set = self.groups.filter(deleted=False)
        nodes = [node.to_dict(use_value_dict) for node in node_set]
        edges = [edge.to_dict(use_value_dict) for edge in edge_set]
        groups = [group.to_dict(use_value_dict) for group in group_set]

        node_seed = self.nodes.aggregate(Max('client_id'))['client_id__max']
        edge_seed = self.edges.aggregate(Max('client_id'))['client_id__max']
        group_seed = self.groups.aggregate(Max('client_id'))['client_id__max']
        graph_seed = max(0 if node_seed is None else node_seed,
                         0 if edge_seed is None else edge_seed,
                         0 if group_seed is None else group_seed)

        return {
            'id': self.pk,
            'seed': graph_seed,
            'name': self.name,
            'type': self.kind,
            'readOnly': self.read_only,
            'nodes': nodes,
            'edges': edges,
            'nodeGroups': groups
        }

    def to_bool_term(self):
        root = self.nodes.get(kind__exact='topEvent')
        return root.to_bool_term()

    def to_graphml(self):
        graphKindData = '        <data key="kind">%s</data>\n' % (self.kind)
        if self.kind in {'faulttree', 'fuzztree'}:
            missionData = '        <data key="missionTime">%d</data>\n' % (
                self.top_node().get_property('missionTime'),)
        else:
            missionData = ''

        return ''.join([
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<graphml xmlns="http://graphml.graphdrawing.org/xmlns"\n'
            '         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
            '         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns\n'
            '                             http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n'
            '    <graph id="graph" edgedefault="directed">\n',
            notations.graphml_keys[self.kind],
            '\n',
            graphKindData,
            missionData] +
            [node.to_graphml() for node in self.nodes.filter(deleted=False)] +
            [edge.to_graphml() for edge in self.edges.filter(deleted=False)] +

            ['    </graph>\n'
             '</graphml>\n'
             ])

    def to_tikz(self):
        """
        Method: to_tikz
            Translates the graph into a LaTex TIKZ representation.

        Returns:
            {string} The TIKZ representation of the graph
        """
        # Latex preambel
        result = """
\\documentclass{article}
\\usepackage[landscape, top=1in, bottom=1in, left=1in, right=1in]{geometry}
\\usepackage{helvet}
\\usepackage{adjustbox}
\\renewcommand{\\familydefault}{\\sfdefault}
\\usepackage{tikz}
\\usetikzlibrary{positioning, trees, svg.path}
\\tikzset{shapeStyle/.style={inner sep=0em, outer sep=0em}}
\\tikzset{shapeStyleDashed/.style={inner sep=0em, outer sep=0em, dashed, dash pattern=on 4.2 off 1.4}}
\\tikzset{mirrorStyle/.style={fill=white,text width=50pt, below, align=center, inner sep=0.2em, outer sep=0.3em}}
\\tikzset{fork edge/.style={line width=1.4, to path={|- ([shift={(\\tikztotarget)}] +0pt,+18pt) -| (\\tikztotarget) }}}
\\begin{document}
\\pagestyle{empty}
        """
        result += tikz_shapes + """
\\begin{figure}
\\begin{adjustbox}{max size={\\textwidth}{\\textheight}}
\\begin{tikzpicture}[auto, trim left]
        """
        # Find most left node and takes it's x coordinate as start offset
        # This basically shifts the whole tree to the left border
        minx = self.nodes.aggregate(min_x=models.Min('x'))['min_x']
        # Find root node and start from there
        # Use the TOP node Y coordinate as starting point at the upper border
        # Note: (0,0) is the upper left corder in TiKZ, but the lower left in
        # the DB
        top_event = self.nodes.get(kind='topEvent')
        result += top_event.to_tikz(x_offset=-minx, y_offset=top_event.y)
#        result += top_event.to_tikz_tree()
        result += """
\\end{tikzpicture}
\\end{adjustbox}
\\end{figure}
\\end{document}
        """
        return result

    def to_xml(self, xmltype=None):
        """
        Method: to_xml
            Serializes the graph into its XML representation.

        Returns:
            {string} The XML representation of the graph
        """
        bds = pyxb.utils.domutils.BindingDOMSupport()
        if xmltype:
            kind = xmltype
        else:
            kind = self.kind
        if kind == "fuzztree":
            tree = XmlFuzzTree(name=self.name, id=self.pk)
            bds.DeclareNamespace(XmlFuzzTreeNamespace, 'fuzzTree')
        elif kind == "faulttree":
            tree = XmlFaultTree(name=self.name, id=self.pk)
            bds.DeclareNamespace(XmlFaultTreeNamespace, 'faultTree')
        else:
            raise ValueError('No XML support for this graph type.')

        # Find root node and start from there
        top_event = self.nodes.get(kind='topEvent')
        tree.topEvent = top_event.to_xml(kind)

        dom = tree.toDOM(bds)
        return dom.toprettyxml()

    def from_xml(self, xml):
        ''' Fill this graph with the information gathered from the XML.'''
        from .node import Node
        if self.kind == "fuzztree":
            tree = fuzzTreeFromXml(xml)
        elif self.kind == "faulttree":
            tree = faultTreeFromXml(xml)
        else:
            raise ValueError('No XML support for this graph type.')

        self.name = tree.name
        self.save()
        top = Node(graph=self)
        top.load_xml(tree.topEvent)

    def from_graphml(self, graphml):
        '''
            Parses the given GraphML with the DefusedXML library, for better security.
        '''
        from .node import Node, new_client_id
        from .edge import Edge
        dom = parseXml(graphml)
        graph = dom.find('{http://graphml.graphdrawing.org/xmlns}graph')
        if graph is None:
            raise Exception(
                'Could not find <graph> element in the input data.')
        if graph.get('edgedefault') != 'directed':
            raise Exception(
                'Only GraphML documents with directed edges are supported.')
        # Determine graph type, in order to check for the right format rules
        graph_kind_element = graph.find(
            "{http://graphml.graphdrawing.org/xmlns}data[@key='kind']")
        if graph_kind_element is None:
            raise Exception(
                'Missing <data> element for graph kind declaration.')
        graph_kind = graph_kind_element.text
        if graph_kind not in notations.graphml_node_data:
            raise Exception('Invalid graph kind declaration.')
        else:
            self.kind = graph_kind
        # Save graph object to get a valid, which is needed in the node refs
        self.save()
        # go through all GraphML nodes and create them as model nodes for this
        # graph
        id_map = {}           # GraphML node ID's to node model PK's
        for gml_node in graph.iter(
                '{http://graphml.graphdrawing.org/xmlns}node'):
            gml_node_id = gml_node.get('id')
            node = Node(graph=self, client_id=int(gml_node_id))
            node.save()     # get a valid pk
            id_map[gml_node_id] = node.pk
            # Scan all data elements for the node
            for gml_node_data in gml_node.iter(
                    '{http://graphml.graphdrawing.org/xmlns}data'):
                name = gml_node_data.get('key')
                value = gml_node_data.text
                if name not in notations.graphml_node_data[graph_kind]:
                    raise Exception("Invalid graph node element '%s'" % name)
                # set according node properties
                if name == 'kind':
                    node.kind = value
                    node.save()
                else:
                    node.set_attr(name, value)
            #logger.debug("New node from GraphML import: "+str(node.to_dict()))
        # Graph properties belong to the TOP node
        # GraphML files without graph <data> properties may refer to a graph type that has no
        # TOP node concept
        for data in graph.findall(
                '{http://graphml.graphdrawing.org/xmlns}data'):
            name = data.get('key')
            if name != 'kind':          # already handled above
                if name not in notations.graphml_graph_data[graph_kind]:
                    raise Exception("Invalid graph data element '%s'" % name)
                logger.debug(
                    "Setting attribute %s to %s on top node" %
                    (name, data.text))
                self.top_node().set_attr(
                    name,
                    data.text)   # Fetch TOP node here, not existent in RBD's

        # go through all GraphML edges and create them as model edges for this
        # graph
        for gml_edge in graph.iter(
                '{http://graphml.graphdrawing.org/xmlns}edge'):
            source = Node.objects.get(pk=id_map[gml_edge.get('source')])
            target = Node.objects.get(pk=id_map[gml_edge.get('target')])
            edge = Edge(
                graph=self,
                source=source,
                target=target,
                client_id=new_client_id())
            edge.save()

    def copy_values(self, other):
        # copy all nodes, groups and their properties
        node_cache = {}

        for node in other.nodes.all():
            # first cache the old node's properties
            properties = node.properties.all()

            # create node copy by overwriting the ID field
            old_id = node.pk
            node.pk = None
            node.graph = self
            node.save()
            node_cache[old_id] = node

            # now save the property objects for the new node
            for prop in properties:
                prop.pk = None
                prop.node = node
                prop.save()

        for edge in other.edges.all():
            properties = edge.properties.all()
            edge.pk = None
            edge.source = node_cache[edge.source.pk]
            edge.target = node_cache[edge.target.pk]
            edge.graph = self
            edge.save()

            # now save the property objects for the new edge
            for prop in properties:
                prop.pk = None
                prop.edge = edge
                prop.save()

        from .node_group import NodeGroup
        for group in other.groups.all():
            # create group copy by overwriting the ID field
            newgroup = NodeGroup(graph=self)
            newgroup.save()         # prepare M2M field
            for node in group.nodes.all():
                newgroup.nodes.add(node_cache[node.pk])
            newgroup.save()

            # now save the property objects for the new group
            for prop in group.properties.all():
                prop.pk = None
                prop.node_group = newgroup
                prop.save()

        self.read_only = other.read_only
        self.save()

    def delete_configurations(self):
        """
            Deletes all informations about configurations of this graph.
        """
        self.configurations.all().delete()

    def delete_results(self, kind):
        '''
            Deletes all graph analysis results of a particular kind.
        '''
        old_results = self.results.filter(kind=kind).all()
        logger.debug(
            "Deleting %u old results of kind %s" %
            (len(old_results), kind))
        old_results.delete()

    def same_as(self, graph):
        '''
            Checks if this graph is equal to the given one in terms of nodes and their properties.
            This is a very expensive operation that is only intended for testing purposes.
            Comparing the edges is not easily possible, since the source / target ID's in the edge
            instances would need to be mapped between original and copy.
        '''

        def error_reporting():
            logger.debug("Graphs are differing:")
            text1 = self.to_graphml()
            text2 = graph.to_graphml()
            import difflib
            difflines = difflib.unified_diff(text1, text2)
            logger.debug('\n'.join(difflines))

        for my_node in self.nodes.all().filter(deleted=False):
            found_match = False
            for their_node in graph.nodes.all().filter(deleted=False):
                logger.debug(
                    "Checking our %s (%u) against %s (%u)" %
                    (str(my_node), my_node.pk, str(their_node), their_node.pk))
                if my_node.same_as(their_node):
                    logger.debug("Match")
                    found_match = True
                    break
            if not found_match:
                logger.debug(
                    "Couldn't find a match for node %s" %
                    (str(my_node)))
                error_reporting()
                return False

        for my_group in self.groups.all().filter(deleted=False):
            found_match = False
            for their_group in graph.groups.all().filter(deleted=False):
                if my_group.same_as(their_group):
                    found_match = True
                    break
            if not found_match:
                error_reporting()
                return False

        return True
