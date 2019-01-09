'''
    A builder that creates several python config files from central JSON
    config files, the so-called 'notations' files. Each notation file
    describes all the relevant semantical rules for the particular graph type.
    The Python derivates are generated in a way that they can be smoothly used
    for correctness and consistency checks.
'''

from SCons.Script import *
import json
import pprint


def generate_graphml_keys(notations):
    '''
        Derive the GraphML preamble from our notations file. This is cool,
        because our GraphML import / export magically matches to the notations file.

        GraphML allows to define extensions as part of the document, by having
        <key> elements that describe the extensions. Later <data> elements
        can refer to these keys.

        Our GraphML export behaves nicely and always adds this preamble, so that
        other GraphML tools can render the values nicely. For this reason,
        the 'graphml_keys' list is generated. It is just an ugly collection of XML
        definitions, which means that Marcus violates his own understand of
        beautiful code ...

        Our GraphML import does not rely on the existence of this preamble, but
        simply wants to know if a given GraphML <data> element refers to a valid key.
        For this reason, the 'graphml_graph_data' and 'graphml_node_data' list is generated.
        It tells the import code if a graph / node element in the input XML is allowed
        to have a particulary named data element.
    '''
    graphml_keys = {}
    graphml_graph_data = {}
    graphml_node_data = {}

    def generate_key_xml(name, kind, default, for_what='node'):
        return \
            '        <key id="%s" for="%s" attr.name="%s" attr.type="%s">\n' \
            '            <default>%s</default>\n' \
            '        </key>' % (name, for_what, name, kind, default,)

    for notation in notations:
        notation_kind = notation['kind']
        graphml_graph_data[notation_kind] = set(['kind'])
        graphml_node_data[notation_kind] = set(['id', 'kind', 'x', 'y'])
        properties = set()
        all_keys = [
            generate_key_xml('id', 'string', '0'),
            generate_key_xml('kind', 'string', 'node'),
            generate_key_xml('x', 'long', '0'),
            generate_key_xml('y', 'long', '0'),
            generate_key_xml('kind', 'string', 'faulttree', 'graph')
        ]

        for node_kind, node in notation['nodes'].items():
            for property_name, propertie in node.get('properties', {}).items():
                if property_name in properties:
                    continue
                else:
                    properties.add(property_name)

                property_default = propertie.get('default', '')
                property_kind = propertie['kind']
                key = None
                keys = None

                if property_kind in {'text', 'textfield'}:
                    key = generate_key_xml(
                        property_name, 'string', property_default if propertie != 'name' else 'Node')
                    graphml_node_data[notation_kind].add(property_name)
                elif property_kind == 'compound':
                    parts_index = property_default[0]
                    compound_parts = propertie['parts']

                    keys = [
                        generate_key_xml(
                            property_name, 'string', property_default[1]),
                        generate_key_xml(
                            property_name + 'Kind', 'string', compound_parts[parts_index]['partName']),
                    ]
                    graphml_node_data[notation_kind].add(property_name)
                elif property_kind == 'bool':
                    key = generate_key_xml(
                        property_name, 'boolean', 'true' if property_default else 'false')
                    graphml_node_data[notation_kind].add(property_name)
                elif property_kind == 'choice':
                    index = propertie['values'].index(property_default)
                    property_default = property_default[index]
                    key = generate_key_xml(
                        property_name, 'string', property_default)
                    graphml_node_data[notation_kind].add(property_name)
                elif property_kind == 'epsilon':
                    keys = [
                        generate_key_xml(
                            property_name, 'double', property_default[0]),
                        generate_key_xml(
                            property_name + 'Epsilon', 'double', property_default[1])
                    ]
                    graphml_node_data[notation_kind].add(property_name)
                elif property_kind in {'numeric', 'range'}:
                    kind = 'long' if propertie.get(
                        'step', 1) == 1 else 'double'

                    if property_name != 'missionTime':
                        key = generate_key_xml(
                            property_name, kind, property_default)
                        graphml_node_data[notation_kind].add(property_name)
                    else:
                        key = generate_key_xml(
                            property_name, kind, property_default, 'graph')
                        graphml_graph_data[notation_kind].add(property_name)
                elif property_kind == 'transfer':
                    key = generate_key_xml(property_name, 'string', '')
                    graphml_node_data[notation_kind].add(property_name)

                if key is not None:
                    all_keys.append(key)
                else:
                    all_keys.extend(keys)

        graphml_keys[notation_kind] = '\n'.join(all_keys)

    return graphml_keys, graphml_graph_data, graphml_node_data


def extend(target, source, *others, **options):
    all_sources = (source,) + others
    deep = options.get('deep', False)

    for other in all_sources:
        if not deep:
            # perform classical dict update, since nested dicts are not used
            target.update(other)
            continue

        for key, value in other.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                target[key] = extend({}, target[key], other[key], deep=True)
            else:
                target[key] = value

    return target


def generate_choices(notations):
    return [(notation['kind'], notation['name']) for notation in notations]


def generate_node_choices(notations):
    node_choices = []

    for notation in notations:
        nodes = notation['nodes']
        node_category = (notation['name'],)
        node_category_choices = ()

        for node_kind, node in nodes.items():
            node_category_choices += ((node_kind, node['nodeDisplayName']),)

        node_category += (node_category_choices,)
        node_choices.append(node_category)

    return node_choices


def inherit(node_name, node, nodes, node_cache):
    inherits_from = node.get('inherits')

    if not inherits_from:
        node_cache[node_name] = node
        return node

    elif inherits_from not in node_cache:
        inherit(inherits_from, nodes[inherits_from], nodes, node_cache)

    resolved = extend({}, node_cache[inherits_from], node, deep=True)
    node_cache[node_name] = resolved

    return resolved


def resolve_inheritance(notations):
    for notation in notations:
        notation[u'edges'] = notation.get(u'edges', {})
        nodes = notation['nodes']
        node_cache = {}

        for node_name, node in nodes.items():
            nodes[node_name] = inherit(node_name, node, nodes, node_cache)


def notations(target, source, env):
    '''
        The central build task for the Python notations file equivalents.
    '''
    notations = []

    for input_file in source:
        with open(str(input_file)) as handle:
            notations.append(json.loads(handle.read()))
    resolve_inheritance(notations)

    with open(str(target[0]), 'w') as out:
        out.write(
            '# DO NOT EDIT! This file is auto-generated by "setup.py build"\n')
        out.write('notations = ')
        pprint.pprint(notations, out)
        out.write(
            '\nby_kind = {notation[\'kind\']: notation for notation in notations}\n')
        out.write('choices = ')
        pprint.pprint(generate_choices(notations), out)
        out.write('\nnode_choices = ')
        pprint.pprint(generate_node_choices(notations), out)
        key_xml, graph_data, node_data = generate_graphml_keys(notations)
        out.write('\ngraphml_keys = ')
        pprint.pprint(key_xml, out)
        out.write('\ngraphml_graph_data = ')
        pprint.pprint(graph_data, out)
        out.write('\ngraphml_node_data = ')
        pprint.pprint(node_data, out)
        out.write('\n# END OF GENERATED CONTENT')


notationsbuilder = Builder(action=notations)
