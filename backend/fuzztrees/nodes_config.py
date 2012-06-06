NODE_TYPES = {
    1: {
        'name': u'Basic Event',
        'type': 'basic',
        'image': 'basic_event.svg'
    },
    2: {
        'name': u'Multi Event',
        'type': 'multi',
        'image': 'multi_event.svg'
    },
    3: {
        'name': u'Fault Event',
        'type': 'fault',
        'image': 'fault_event.svg'
    },
    4: {
        'name': u'Multi Fault Event',
        'type': 'multi_fault',
        'image': 'multi_fault_event.svg'
    },
    5: {
        'name': u'AND Gate',
        'type': 'and',
        'image': 'and_gate.svg'
    },
    6: {
        'name': u'Priority AND Gate',
        'type': 'p-and',
        'image': 'priority_and_gate.svg'
    },
    7: {
        'name': u'OR Gate',
        'type': 'or',
        'image': 'or_gate.svg'
    },
    8: {
        'name': u'XOR Gate',
        'type': 'xor',
        'image': 'xor_gate.svg'
    }, 
    9: {
        'name': u'Voting OR Gate',
        'type': 'v-or',
        'image': 'voting_or_gate.svg'
    },
    10: {
        'name': u'Inhibit Gate',
        'type': 'inhibit',
        'image': 'inhibit_gate.svg'
    },
    11: {
        'name': u'Choice Event',
        'type': 'choice',
        'image': 'choice_event.svg'
    },
    12: {
        'name': u'Redundancy Event',
        'type': 'redundancy',
        'image': 'redundancy_event.svg'
    },
    13: {
        'name': u'Undeveloped Event',
        'type': 'undeveloped',
        'image': 'undeveloped_event.svg'
    },
    14: {
        'name': u'House Event',
        'type': 'house',
        'image': 'house_event.svg'
    }
}

def nodeTypeChoices():
    return map(lambda (type, entry): (type, entry['name']), NODE_TYPES.iteritems())
