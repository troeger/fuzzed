NODE_TYPES = {
    1: {
        'name': u'Basic Event',
        'type': 'basic',
        'image': 'basic_event.svg',
        'help': 'Initiating failure in a basic component',
        'optional': 'False'
    },
    2: {
        'name': u'Basic Event Set',
        'type': 'basic-set',
        'image': 'basic_event_set.svg',
        'help': 'Set of basic events with identical properties',
        'optional': 'False'
    },
    3: {
        'name': u'Intermediate Event',
        'type': 'intermediate',
        'image': 'intermediate_event.svg',
        'help': 'Failure resulting from a combination of previous events.',
        'optional': 'False'
    },
    4: {
        'name': u'Intermediate Event Set',
        'type': 'multi_fault',
        'image': 'multi_fault_event.svg',
        'help': 'Set of intermediate events',
        'optional': 'False'
    },
    5: {
        'name': u'AND Gate',
        'type': 'and',
        'image': 'and_gate.svg',
        'help': 'Output event occurs if all input events occur',
        'optional': 'Undefined'
    },
    6: {
        'name': u'Priority AND Gate',
        'type': 'p-and',
        'image': 'priority_and_gate.svg',
        'help': 'Output event occurs if all input events occur in the specific order',
        'optional': 'Undefined'
    },
    7: {
        'name': u'OR Gate',
        'type': 'or',
        'image': 'or_gate.svg',
        'help': 'Output event occurs if one or more input events occur',
        'optional': 'Undefined'
    },
    8: {
        'name': u'XOR Gate',
        'type': 'xor',
        'image': 'xor_gate.svg',
        'help': 'Output event occurs if exactly one of the input events occur',
        'optional': 'Undefined'
    }, 
    9: {
        'name': u'Voting OR Gate',
        'type': 'v-or',
        'image': 'voting_or_gate.svg',
        'help': 'Output event occurs if the given number of input events occur',
        'optional': 'Undefined'
    },
    10: {
        'name': u'Inhibit Gate',
        'type': 'inhibit',
        'image': 'inhibit_gate.svg',
        'help': 'Output event occurs if the single input event occurs and the enabling condition is given',
        'optional': 'Undefined'
    },
    11: {
        'name': u'Choice Event',
        'type': 'choice',
        'image': 'choice_event.svg',
        'help': 'Placeholder for one of the input events',
        'optional': 'False'
    },
    12: {
        'name': u'Redundancy Event',
        'type': 'redundancy',
        'image': 'redundancy_event.svg',
        'help': 'Placeholder for a voting OR gate over a chosen number of the input events',
        'optional': 'False'
    },
    13: {
        'name': u'Undeveloped Event',
        'type': 'undeveloped',
        'image': 'undeveloped_event.svg',
        'help': 'Event with no information available or insignificant impact',
        'optional': 'False'
    },
    14: {
        'name': u'House Event',
        'type': 'house',
        'image': 'house_event.svg',
        'help':  'An event that is expected to occur and typically does not denote a failure',
        'optional': 'False'
    }
}

NODE_TYPE_IDS = {}
for node_id, node in NODE_TYPES.items():
    NODE_TYPE_IDS[node['type']] = node_id

def nodeTypeChoices():
    return map(lambda (type, entry): (type, entry['name']), NODE_TYPES.iteritems())
