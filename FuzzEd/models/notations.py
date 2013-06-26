# DO NOT EDIT! This file is auto-generated by "setup.py build"


class fuzztree_node():
    numberOfIncomingConnections = 1
    numberOfOutgoingConnections = -1
    allowConnectionTo = [u'node']
    connector = {u'offset': {u'top': 0, u'bottom': 0}}
    deletable = True
    nodeDisplayName = 'Node'
    properties = {u'name': {u'default': u'Node', u'kind': u'text', u'displayName': u'Name', u'mirror': {u'position': u'bottom', u'style': [u'bold', u'large']}}}

class fuzztree_topEvent(fuzztree_event):
    excludeFromShapesMenu = True
    numberOfOutgoingConnections = 1
    image = 'top_event.svg'
    numberOfIncomingConnections = 0
    deletable = False
    nodeDisplayName = 'Top Event'
    properties = {u'optional': None, u'name': {u'default': u'Top Event'}, u'decompositions': {u'default': 1, u'kind': u'numeric', u'displayName': u'Decompose', u'step': 1, u'min': 1}}

class fuzztree_variationPoint(fuzztree_node):
    nodeDisplayName = 'Variation Point'
    properties = {u'name': {u'default': u'Variation Point'}}

class fuzztree_votingOrGate(fuzztree_gate):
    image = 'voting_or_gate.svg'
    nodeDisplayName = 'Voting OR Gate'
    help = 'Output event occurs if the given number of input events occur'
    properties = {u'k': {u'kind': u'numeric', u'displayName': u'k', u'min': 1, u'default': 1, u'step': 1, u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'k={{$0}}'}}, u'name': {u'default': u'Voting OR Gate'}}

class fuzztree_orGate(fuzztree_gate):
    help = 'Output event occurs if one or more input events occur'
    image = 'or_gate.svg'
    connector = {u'offset': {u'bottom': -7}}
    nodeDisplayName = 'OR Gate'
    properties = {u'name': {u'default': u'OR Gate'}}

class fuzztree_intermediateEvent(fuzztree_event):
    image = 'intermediate_event.svg'
    nodeDisplayName = 'Intermediate Event'
    help = 'Failure resulting from a combination of previous events'
    properties = {u'name': {u'default': u'Intermediate Event'}}

class fuzztree_intermediateEventSet(fuzztree_intermediateEvent):
    image = 'intermediate_event_set.svg'
    nodeDisplayName = 'Intermediate Event Set'
    help = 'Set of intermediate events'
    properties = {u'cardinality': {u'kind': u'numeric', u'displayName': u'Cardinality', u'min': 1, u'default': 1, u'step': 1, u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'#{{$0}}'}}, u'name': {u'default': u'Intermediate Event Set'}}

class fuzztree_featureVariation(fuzztree_variationPoint):
    changedChildProperties = {u'optional': None}
    help = 'Placeholder for one of the input events'
    image = 'feature_variation.svg'
    allowConnectionTo = [u'event', u'variationPoint', u'transferIn']
    childProperties = {u'optional': {u'hidden': True, u'value': False}}
    connector = {u'dashstyle': u'4 2'}
    nodeDisplayName = 'Feature Variation'
    properties = {u'name': {u'default': u'Feature Variation'}}

class fuzztree_andGate(fuzztree_gate):
    image = 'and_gate.svg'
    nodeDisplayName = 'AND Gate'
    help = 'Output event occurs if all input events occur'
    properties = {u'name': {u'default': u'AND Gate'}}

class fuzztree_xorGate(fuzztree_gate):
    image = 'xor_gate.svg'
    nodeDisplayName = 'XOR Gate'
    help = 'Output event occurs if exactly one of the input events occur'
    properties = {u'name': {u'default': u'XOR Gate'}}

class fuzztree_redundancyVariation(fuzztree_variationPoint):
    changedChildProperties = {u'optional': None}
    help = 'Placeholder for a voting OR gate over a chosen number of the input events'
    numberOfOutgoingConnections = 1
    image = 'redundancy_variation.svg'
    allowConnectionTo = [u'intermediateEventSet', u'basicEventSet']
    connector = {u'dashstyle': u'4 2'}
    nodeDisplayName = 'Redundancy Variation'
    properties = {u'kFormula': {u'default': u'N-1', u'kind': u'text', u'displayName': u'K-Formula', u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'k: {{$0}}'}}, u'name': {u'default': u'Redundancy Variation'}, u'nRange': {u'kind': u'range', u'displayName': u'N-Range', u'min': 1, u'default': [1, 2], u'step': 1, u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'N: {{$0}}-{{$1}}'}}}

class fuzztree_undevelopedEvent(fuzztree_event):
    help = 'Event with no information available or insignificant impact'
    numberOfOutgoingConnections = 0
    image = 'undeveloped_event.svg'
    nodeDisplayName = 'Undeveloped Event'
    properties = {u'optional': None, u'name': {u'default': u'Undeveloped Event'}}

class fuzztree_gate(fuzztree_node):
    nodeDisplayName = 'Gate'
    properties = {u'name': {u'default': u'Gate'}}

class fuzztree_transferIn(fuzztree_node):
    numberOfIncomingConnections = 1
    help = 'Connects the output of a related FuzzTree, e.g. a subsystem, to this one'
    numberOfOutgoingConnections = 0
    image = 'transfer_in.svg'
    nodeDisplayName = 'Transfer In'
    properties = {u'transfer': {u'default': -1, u'kind': u'transfer', u'displayName': u'Transfer', u'mirror': {u'position': u'bottom', u'style': [u'bold', u'large'], u'format': u'\u25c4 {{$0}}'}}, u'name': {u'default': u'Transfer In'}, u'transferMaxCost': {u'kind': u'numeric', u'displayName': u'Max Cost', u'min': 0, u'default': 1, u'step': 1, u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'max(c)={{$0}}'}}}

class fuzztree_basicEventSet(fuzztree_basicEvent):
    image = 'basic_event_set.svg'
    nodeDisplayName = 'Basic Event Set'
    help = 'Set of basic events with identical properties'
    properties = {u'cardinality': {u'kind': u'numeric', u'displayName': u'Cardinality', u'min': 1, u'default': 1, u'step': 1, u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'#{{$0}}'}}, u'name': {u'default': u'Basic Event Set'}}

class fuzztree_basicEvent(fuzztree_event):
    help = 'Initiating failure in a basic component'
    numberOfOutgoingConnections = 0
    image = 'basic_event.svg'
    nodeDisplayName = 'Basic Event'
    properties = {u'cost': {u'kind': u'numeric', u'displayName': u'Cost', u'min': 0, u'default': 1, u'step': 0.01, u'mirror': {u'position': u'bottom', u'format': u'c={{$0}}'}}, u'name': {u'default': u'Basic Event'}, u'probability': {u'default': [0, [0.5, 0]], u'kind': u'compound', u'parts': [{u'kind': u'epsilon', u'min': 0, u'default': [0.5, 0], u'max': 1, u'partName': u'Exact', u'step': 1e-10, u'epsilonStep': 1e-10, u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'p={{$0}}\xb1{{$1}}'}}, {u'kind': u'choice', u'default': [0.5, 0.3], u'partName': u'Fuzzy', u'choices': [u'never', u'very unlikely', u'unlikely', u'more or less', u'likely', u'very likely', u'always'], u'values': [[0, 0], [0.2, 0.1], [0.33, 0.2], [0.5, 0.3], [0.66, 0.2], [0.8, 0.1], [1, 0]], u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'p={{$0}}'}}], u'displayName': u'Probability'}}

class fuzztree_event(fuzztree_node):
    nodeDisplayName = 'Event'
    properties = {u'optional': {u'default': False, u'kind': u'bool', u'displayName': u'Optional'}, u'name': {u'default': u'Event'}}

class fuzztree_houseEvent(fuzztree_basicEvent):
    help = 'An event that is expected to occur and typically does not denote a failure'
    numberOfOutgoingConnections = 0
    image = 'house_event.svg'
    nodeDisplayName = 'House Event'
    properties = {u'name': {u'default': u'House Event'}}

class fuzztree():
    kind = 'fuzztree'
    name = 'Fuzz Tree'
    propertiesDisplayOrder = [u'name', u'cost', u'probability', u'optional', u'cardinality', u'nRange', u'k', u'kFormula', u'decompositions', u'transfer', u'transferMaxCost']
    defaults = {u'nodes': [{u'y': 1, u'x': 10, u'kind': u'topEvent'}]}
    shapeMenuNodeDisplayOrder = [u'basicEvent', u'basicEventSet', u'intermediateEvent', u'intermediateEventSet', u'andGate', u'orGate', u'xorGate', u'votingOrGate', u'featureVariation', u'redundancyVariation', u'houseEvent', u'undevelopedEvent', u'transferIn', u'topEvent']
    nodes = {'node':fuzztree_node(),'topEvent':fuzztree_topEvent(),'variationPoint':fuzztree_variationPoint(),'votingOrGate':fuzztree_votingOrGate(),'orGate':fuzztree_orGate(),'intermediateEvent':fuzztree_intermediateEvent(),'intermediateEventSet':fuzztree_intermediateEventSet(),'featureVariation':fuzztree_featureVariation(),'andGate':fuzztree_andGate(),'xorGate':fuzztree_xorGate(),'redundancyVariation':fuzztree_redundancyVariation(),'undevelopedEvent':fuzztree_undevelopedEvent(),'gate':fuzztree_gate(),'transferIn':fuzztree_transferIn(),'basicEventSet':fuzztree_basicEventSet(),'basicEvent':fuzztree_basicEvent(),'event':fuzztree_event(),'houseEvent':fuzztree_houseEvent()}

class faulttree_node():
    numberOfIncomingConnections = 1
    numberOfOutgoingConnections = -1
    allowConnectionTo = [u'node']
    connector = {u'offset': {u'top': 0, u'bottom': 0}}
    deletable = True
    nodeDisplayName = 'Node'
    properties = {u'name': {u'default': u'Node', u'kind': u'text', u'displayName': u'Name', u'mirror': {u'position': u'bottom', u'style': [u'bold', u'large']}}}

class faulttree_topEvent(faulttree_event):
    excludeFromShapesMenu = True
    numberOfOutgoingConnections = 1
    image = 'top_event.svg'
    numberOfIncomingConnections = 0
    deletable = False
    nodeDisplayName = 'Top Event'
    properties = {u'name': {u'default': u'Top Event'}}

class faulttree_votingOrGate(faulttree_gate):
    image = 'voting_or_gate.svg'
    nodeDisplayName = 'Voting OR Gate'
    help = 'Output event occurs if the given number of input events occur'
    properties = {u'k': {u'kind': u'numeric', u'displayName': u'k', u'min': 1, u'default': 1, u'step': 1, u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'k={{$0}}'}}, u'name': {u'default': u'Voting OR Gate'}}

class faulttree_orGate(faulttree_gate):
    help = 'Output event occurs if one or more input events occur'
    image = 'or_gate.svg'
    connector = {u'offset': {u'bottom': -7}}
    nodeDisplayName = 'OR Gate'
    properties = {u'name': {u'default': u'OR Gate'}}

class faulttree_basicEvent(faulttree_event):
    help = 'Initiating failure in a basic component'
    numberOfOutgoingConnections = 0
    image = 'basic_event.svg'
    nodeDisplayName = 'Basic Event'
    properties = {u'name': {u'default': u'Basic Event'}, u'probability': {u'kind': u'numeric', u'displayName': u'Probability', u'min': 0, u'default': 0, u'max': 1, u'step': 1e-10, u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'p={{$0}}'}}}

class faulttree_intermediateEventSet(faulttree_intermediateEvent):
    excludeFromShapesMenu = True
    help = 'Set of intermediate events'
    image = 'intermediate_event_set.svg'
    nodeDisplayName = 'Intermediate Event Set'
    properties = {u'cardinality': {u'kind': u'numeric', u'displayName': u'Cardinality', u'min': 1, u'default': 1, u'step': 1, u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'#{{$0}}'}}, u'name': {u'default': u'Intermediate Event Set'}}

class faulttree_andGate(faulttree_gate):
    image = 'and_gate.svg'
    nodeDisplayName = 'AND Gate'
    help = 'Output event occurs if all input events occur'
    properties = {u'name': {u'default': u'AND Gate'}}

class faulttree_xorGate(faulttree_gate):
    name = 'XOR Gate'
    image = 'xor_gate.svg'
    nodeDisplayName = 'XOR Gate'
    properties = {u'name': {u'default': u'XOR Gate'}}
    help = 'Output event occurs if exactly one of the input events occur'

class faulttree_undevelopedEvent(faulttree_event):
    help = 'Event with no information available or insignificant impact'
    numberOfOutgoingConnections = 0
    image = 'undeveloped_event.svg'
    nodeDisplayName = 'Undeveloped Event'
    properties = {u'name': {u'default': u'Undeveloped Event'}}

class faulttree_gate(faulttree_node):
    nodeDisplayName = 'Gate'
    properties = {u'name': {u'default': u'Gate'}}

class faulttree_transferIn(faulttree_node):
    numberOfIncomingConnections = 1
    help = 'Connects the output of a related FaultTree, e.g. a subsystem, to this one'
    numberOfOutgoingConnections = 0
    image = 'transfer_in.svg'
    nodeDisplayName = 'Transfer In'
    properties = {u'transfer': {u'default': -1, u'kind': u'transfer', u'displayName': u'Transfer', u'mirror': {u'position': u'bottom', u'style': [u'bold', u'large'], u'format': u'\u25c4 {{$0}}'}}, u'name': {u'default': u'Transfer In'}}

class faulttree_basicEventSet(faulttree_basicEvent):
    image = 'basic_event_set.svg'
    nodeDisplayName = 'Basic Event Set'
    help = 'Set of basic events with identical properties'
    properties = {u'cardinality': {u'kind': u'numeric', u'displayName': u'Cardinality', u'min': 1, u'default': 1, u'step': 1, u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'#{{$0}}'}}, u'name': {u'default': u'Basic Event Set'}}

class faulttree_intermediateEvent(faulttree_event):
    image = 'intermediate_event.svg'
    nodeDisplayName = 'Intermediate Event'
    help = 'Failure resulting from a combination of previous events'
    properties = {u'name': {u'default': u'Intermediate Event'}}

class faulttree_event(faulttree_node):
    nodeDisplayName = 'Event'
    properties = {u'name': {u'default': u'Event'}}

class faulttree_houseEvent(faulttree_basicEvent):
    image = 'house_event.svg'
    nodeDisplayName = 'House Event'
    help = 'An event that is expected to occur and typically does not denote a failure'
    properties = {u'name': {u'default': u'House Event'}}

class faulttree():
    kind = 'faulttree'
    name = 'Fault Tree'
    propertiesDisplayOrder = [u'name', u'probability', u'cardinality', u'k', u'transfer']
    defaults = {u'nodes': [{u'y': 1, u'x': 10, u'kind': u'topEvent'}]}
    shapeMenuNodeDisplayOrder = [u'basicEvent', u'basicEventSet', u'intermediateEvent', u'intermediateEventSet', u'andGate', u'orGate', u'xorGate', u'votingOrGate', u'undevelopedEvent', u'houseEvent', u'transferIn', u'topEvent']
    nodes = {'node':faulttree_node(),'topEvent':faulttree_topEvent(),'votingOrGate':faulttree_votingOrGate(),'orGate':faulttree_orGate(),'basicEvent':faulttree_basicEvent(),'intermediateEventSet':faulttree_intermediateEventSet(),'andGate':faulttree_andGate(),'xorGate':faulttree_xorGate(),'undevelopedEvent':faulttree_undevelopedEvent(),'gate':faulttree_gate(),'transferIn':faulttree_transferIn(),'basicEventSet':faulttree_basicEventSet(),'intermediateEvent':faulttree_intermediateEvent(),'event':faulttree_event(),'houseEvent':faulttree_houseEvent()}

class rbd_node():
    numberOfIncomingConnections = -1
    numberOfOutgoingConnections = -1
    allowConnectionTo = []
    connector = {u'offset': {u'top': 0, u'bottom': 0}}
    nodeDisplayName = 'Node'
    properties = {u'name': {u'default': u'Node', u'kind': u'text', u'displayName': u'Name', u'mirror': {u'position': u'bottom', u'style': [u'bold', u'large']}}}

class rbd_start(rbd_node):
    numberOfIncomingConnections = 0
    image = 'start.svg'
    excludeFromShapesMenu = True
    allowConnectionTo = [u'end', u'block', u'out_of']
    connector = {u'offset': {u'right': -9.1}}
    deletable = False
    nodeDisplayName = 'Start'
    properties = {u'name': {u'default': u'Start'}}

class rbd_out_of(rbd_node):
    excludeFromShapesMenu = False
    numberOfOutgoingConnections = 1
    image = 'out_of.svg'
    allowConnectionTo = [u'block', u'end']
    properties = {u'out_of': {u'kind': u'range', u'displayName': u'Out-of', u'min': 1, u'default': [1, 1], u'step': 1, u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'{{$0}}/{{$1}}'}}, u'name': {u'default': u'Out of'}}
    nodeDisplayName = 'Out of'
    out_of = [1, 1]

class rbd_end(rbd_node):
    excludeFromShapesMenu = True
    numberOfOutgoingConnections = 0
    image = 'end.svg'
    connector = {u'offset': {u'left': 8.1}}
    deletable = False
    nodeDisplayName = 'End'
    properties = {u'name': {u'default': u'End'}}

class rbd_block(rbd_node):
    excludeFromShapesMenu = False
    image = 'block.svg'
    allowConnectionTo = [u'end', u'block', u'out_of']
    nodeDisplayName = 'Block'
    properties = {u'probability': {u'kind': u'numeric', u'displayName': u'Probability', u'min': 0, u'default': 0, u'max': 1, u'step': 1e-10, u'mirror': {u'position': u'bottom', u'style': [u'italic'], u'format': u'p={{$0}}'}}}

class rbd():
    kind = 'rbd'
    name = 'Reliability Block Diagram'
    propertiesDisplayOrder = [u'name', u'probability', u'out_of']
    defaults = {u'nodes': [{u'y': 1, u'x': 5, u'kind': u'start'}, {u'y': 1, u'x': 10, u'kind': u'end'}]}
    shapeMenuNodeDisplayOrder = [u'block', u'out_of', u'start', u'end']
    nodes = {'node':rbd_node(),'start':rbd_start(),'out_of':rbd_out_of(),'end':rbd_end(),'block':rbd_block()}

# END OF GENERATED CONTENT
