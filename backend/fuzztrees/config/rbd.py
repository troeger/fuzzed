RBD_CONFIG = {
	'nodes': {
		'startNode': {
			'image': 'node.svg',
			'excludeFromShapesMenu': True,
			'numberOfIncomingConnections':  0,
			'numberOfOutgoingConnections': -1, #infinite
			'allowConnectionTo': ['endNode', 'block', 'outOf'],
			'name': {
				'type': 'text',
				'displayName': u'Name',
				'default': u'Start',
				'mirror': {
			        'position': 'bottom',
			        'style': ['bold']
		        },
			}
		},

		'endNode': {
			'image': 'node.svg',
			'excludeFromShapesMenu': True,
			'numberOfIncomingConnections': -1, #infinite
			'numberOfOutgoingConnections':  0,
			'name': {
				'type': 'text',
				'displayName': u'Name',
				'default': u'End',
				'mirror': {
			        'position': 'bottom',
			        'style': ['bold']
		        },
			}
		},

		'block': {
			'image': 'block.svg',
			'numberOfIncomingConnections': -1, #infinite
			'numberOfOutgoingConnections': -1, #infinite
			'name': {
				'type': 'text',
				'displayName': u'Name',
				'default': u'Block',
				'mirror': {
			        'position': 'bottom',
			        'style': ['bold']
		        },
			},
			'probability': {
				'type': 'number',
				'displayName': u'Probability',
	            'min': 0,
	            'max': 1,
	            'step': 0.01,
	            'default': 0
			}
		},

		'outOf': {
			'image': 'out_of.svg',
			'numberOfIncomingConnections': -1, #infinite
			'numberOfOutgoingConnections': -1, #infinite
			'allowConnectionTo': ['block', 'endNode'],
			'outOf': {
			    'type': 'range',
		        'displayName': u'Out Of',
		        'min': 1,
		        'step': 1,
		        'default': [1, 1] # min, max
			}
		}
	},

    'propertyDisplayOrder': [
		'name',
        'probability',
        'outOf'
    ],

    'shapeMenuNodeDisplayOrder': [
	    'basicEvent',
        'basicEventSet'
    ]
}
