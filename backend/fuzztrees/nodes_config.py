NODE_TYPES = {
    1: {
        'name': u'Basic event',
        'type': 'basic',
        'image': 'basic_event.svg'
    },
    2: {
        'name': u'Multi Event',
        'type': 'multi',
        'image': 'multi_event.svg'
    },
    3: {
        'name': u'Undeveloped event',
        'type': 'undeveloped',
        'image': 'undeveloped_event.svg'
    },
    4: {
        'name': u'Fault event',
        'type': 'fault',
        'image': 'fault_event.svg'
    },
    5: {
        'name': u'AND gate',
        'type': 'and',
        'image': 'and_gate.svg'
    },
    6: {
        'name': u'Priority AND gate',
        'type': 'p-and',
        'image': 'priority_and_gate.svg'
    },
    7: {
        'name': u'OR gate',
        'type': 'or',
        'image': 'or_gate.svg'
    },
    8: {
        'name': u'XOR gate',
        'type': 'xor',
        'image': 'xor_gate.svg'
    }, 
    9: {
        'name': u'Voting OR gate',
        'type': 'v-or',
        'image': 'voting_or_gate.svg'
    },
    10: {
        'name': u'Inhibit gate',
        'type': 'inhibit',
        'image': 'inhibit_gate.svg'
    },
    11: {
        'name': u'Choice event',
        'type': 'choice',
        'image': 'choice_event.svg'
    },
    12: {
        'name': u'Redundancy event',
        'type': 'redundancy',
        'image': 'redundancy_event.svg'
    },
    13: {
        'name': u'House Event',
        'type': 'house',
        'image': 'house_event.svg'
    }
}

def nodeTypeChoices():
    return map(lambda (type, entry): (type, entry['name']), NODE_TYPES.iteritems())
