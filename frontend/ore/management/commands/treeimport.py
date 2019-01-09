from django.core.management.base import BaseCommand
from ore.models import Graph, Node, Edge, Property
from django.contrib.auth.models import User

import os.path


class Command(BaseCommand):
    args = '<owner> <textfile>'
    help = 'Imports a fault tree in European Benchmark Fault Trees Format, see http://bit.ly/UrAxM1'
    got_root_gate = False
    nodes = {}
    graph = None
    gate_x = 0
    event_x = 0
    current_id = 0

    def client_id(self):
        self.current_id += 1
        return self.current_id

    def get_id(self, title):
        if '/' in title:
            return title[title.find(')') + 1:]
        else:
            return filter(lambda x: x.isdigit(), title)

    def addNode(self, title, lineno):
        lineno += 10
        node_id = self.get_id(title)
        kind = None

        if node_id not in self.nodes.keys():
            # TODO: Use some reasonable X / Y coordinates
            self.gate_x += 1

            if '*' in title:
                kind = 'andGate'
            elif '+' in title:
                kind = 'orGate'
            elif '/' in title:
                kind = 'votingOrGate'
            elif title.startswith('T'):
                kind = 'basicEvent'

            node = Node(
                graph=self.g,
                x=self.gate_x,
                y=lineno,
                kind=kind,
                client_id=self.client_id())
            self.nodes[node_id] = node
            node.save()

            prob = Property(key='title', value=title, node=node)
            prob.save()

            if not self.got_root_gate:
                # connect the very first gate to the top event
                root_node = Node.objects.get(
                    kind__exact='topEvent',
                    graph=self.graph)
                edge = Edge(
                    graph=self.graph,
                    source=root_node,
                    target=self.nodes[node_id],
                    client_id=self.client_id())
                edge.save()

                self.got_root_gate = True

    def handle(self, *args, **options):
        user_name = 'admin'
        file_name = 'ore/fixtures/europe-1.txt'
        argc = len(args)

        if argc == 1:
            user_name = args[0]

        elif argc == 2:
            user_name = args[0]
            file_name = args[1]

        owner = User.objects.get(username__exact=user_name)

        with open(file_name) as file_handle:
            self.graph = Graph(
                name=os.path.split(file_name)[-1], kind='fuzztree', owner=owner)
            self.graph.save()

            for lineno, line in enumerate(file_handle):
                if line.startswith('G'):
                    # Gate node
                    nodes = [
                        node for node in line.rstrip('\n').split(' ') if node != '']
                    for node in nodes:
                        self.addNode(node, lineno)
                    # Add edges now, since all nodes in the line are in the DB
                    parent = self.nodes[self.get_id(nodes[0])]
                    for node in nodes[1:]:
                        edge = Edge(graph=self.graph, source=parent,
                                    target=self.nodes[
                                        self.get_id(node)], client_id=self.client_id()
                                    )
                        edge.save()

                elif line.startswith('T'):
                    # Basic event node with probability
                    title, probability = line.split(' ')[0:2]

                    self.addNode(title, lineno)
                    node = self.nodes[self.get_id(title)]

                    prop = Property(
                        key='probability',
                        value=str(
                            float(probability)),
                        node=node)
                    prop.save()
