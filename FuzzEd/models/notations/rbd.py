# TODO: needs rework
CONFIG = {
    'kind': 'rbd',
    'name': u'Reliability Block Diagram',
    'nodes': {
        'node': {
            'name': u'Node',
            'excludeFromShapesMenu': True,
            'numberOfIncomingConnections': -1, #infinite
            'numberOfOutgoingConnections': -1, #infinite
            'propertyMenuEntries': {
                'name': {
                    'kind': 'text',
                    'displayName': u'Name'
                }
            },
            'propertyMirrors': {
                'name': {
                    'position': 'bottom',
                    'style': ['bold']
                }
            }
        },

        'startNode': {
            'inherits': 'node',
            'name': u'Start',
            'image': 'node.svg',
            'numberOfIncomingConnections':  0,
            'numberOfOutgoingConnections': -1, #infinite
            'allowConnectionTo': ['endNode', 'block', 'outOf']
        },

        'endNode': {
            'inherits': 'node',
            'name': u'End',
            'image': 'node.svg',
            'numberOfIncomingConnections': -1, #infinite
            'numberOfOutgoingConnections':  0
        },

        'block': {
            'inherits': 'node',
            'name': u'Block',
            'excludeFromShapesMenu': False,
            'image': 'block.svg',
            'propertyMenuEntries': {
                'probability': {
                    'kind': 'number',
                    'displayName': u'Probability',
                    'min': 0,
                    'max': 1,
                    'step': 0.01
                }
            },
            'probabilityMirrors': {
                'probability': {
                    'position': 'bottom',
                    'style': ['italic']
                }
            }
        },

        'outOf': {
            'inherits': 'node',
            'name': u'out of',
            'excludeFromShapesMenu': False,
            'image': 'out_of.svg',
            'allowConnectionTo': ['block', 'endNode'],
            'propertyMenuEntries': {
                'outOf': {
                    'kind': 'range',
                    'displayName': u'Out Of',
                    'min': 1,
                    'step': 1,
                    'default': [1, 1] # min, max
                }
            }
        }
    },

    'propertyDisplayOrder': [
        'name',
        'probability',
        'outOf'
    ],

    'shapeMenuNodeDisplayOrder': [
        'block',
        'outOf'
    ],

        # Field: defaults
    #
    # Default elements and properties a new graph is initialized with.
    'defaults': {
        'nodes': [
            {
                'kind': 'startNode',
                'x': 5,
                'y': 1
            },
            {
                'kind': 'endNode',
                'x': 10,
                'y': 1
            }
        ]
    }
}
