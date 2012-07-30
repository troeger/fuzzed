NODE_TYPES = {
    1: {
        'name': u'Basic Event',
        'type': 'basicEvent',
        'image': 'basic_event.svg',
        'help': 'Initiating failure in a basic component',
        'optional': 'no'
    },
    2: {
        'name': u'Basic Event Set',
        'type': 'basicEventSet',
        'image': 'basic_event_set.svg',
        'help': 'Set of basic events with identical properties',
        'optional': 'no'
    },
    3: {
        'name': u'Intermediate Event',
        'type': 'intermediateEvent',
        'image': 'intermediate_event.svg',
        'help': 'Failure resulting from a combination of previous events.',
        'optional': 'no'
    },
    4: {
        'name': u'Intermediate Event Set',
        'type': 'intermediateEventSet',
        'image': 'intermediate_event_set.svg',
        'help': 'Set of intermediate events',
        'optional': 'no'
    },
    5: {
        'name': u'AND Gate',
        'type': 'andGate',
        'image': 'and_gate.svg',
        'help': 'Output event occurs if all input events occur',
        'optional': 'undefined'
    },
    6: {
        'name': u'Priority AND Gate',
        'type': 'priorityAndGate',
        'image': 'priority_and_gate.svg',
        'help': 'Output event occurs if all input events occur in the specific order',
        'optional': 'undefined'
    },
    7: {
        'name': u'OR Gate',
        'type': 'orGate',
        'image': 'or_gate.svg',
        'help': 'Output event occurs if one or more input events occur',
        'optional': 'undefined'
    },
    8: {
        'name': u'XOR Gate',
        'type': 'xorGate',
        'image': 'xor_gate.svg',
        'help': 'Output event occurs if exactly one of the input events occur',
        'optional': 'undefined'
    }, 
    9: {
        'name': u'Voting OR Gate',
        'type': 'votingOrGate',
        'image': 'voting_or_gate.svg',
        'help': 'Output event occurs if the given number of input events occur',
        'optional': 'undefined'
    },
    10: {
        'name': u'Inhibit Gate',
        'type': 'inhibitGate',
        'image': 'inhibit_gate.svg',
        'help': 'Output event occurs if the single input event occurs and the enabling condition is given',
        'optional': 'undefined'
    },
    11: {
        'name': u'Choice Event',
        'type': 'choiceEvent',
        'image': 'choice_event.svg',
        'help': 'Placeholder for one of the input events',
        'optional': 'no'
    },
    12: {
        'name': u'Redundancy Event',
        'type': 'redundancyEvent',
        'image': 'redundancy_event.svg',
        'help': 'Placeholder for a voting OR gate over a chosen number of the input events',
        'optional': 'no'
    },
    13: {
        'name': u'Undeveloped Event',
        'type': 'undevelopedEvent',
        'image': 'undeveloped_event.svg',
        'help': 'Event with no information available or insignificant impact',
        'optional': 'no'
    },
    14: {
        'name': u'House Event',
        'type': 'houseEvent',
        'image': 'house_event.svg',
        'help':  'An event that is expected to occur and typically does not denote a failure',
        'optional': 'no'
    },
    15: {
        'name': u'Top Event',
        'type': 'topEvent',
        'image': 'intermediate_event.svg',
        'hidden': True
    }
}

NODE_TYPE_IDS = {}
for node_id, node in NODE_TYPES.items():
    NODE_TYPE_IDS[node['type']] = node_id

def nodeTypeChoices():
    return map(lambda (type, entry): (type, entry['name']), NODE_TYPES.iteritems())
