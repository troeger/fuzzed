FAULTTREE_CONFIG = {
	'nodes': {
		'node': {
			'excludeFromShapesMenu': True,
		    'numberOfIncomingConnections': -1, #infinite
		    'numberOfOutgoingConnections':  1,
		    'allowConnectionTo': ['node'],
		    'name': {
			    'type': 'text',
		        'displayName': u'Name',
			    'default': u'Node'
		    }
		},

	    'event': {
		    'inherits': 'node',
		    'excludeFromShapesMenu': True,
	        'numberOfIncomingConnections':  1,
	        'numberOfOutgoingConnections': -1,
	        'allowConnectionTo': ['gate'],
	        'name': {
		        # events show their names below the image
		        'mirror': {
			        'position': 'bottom',
			        'style': ['bold']
		        },
	            'default': u'Event'
	        }
	        'probability': {
		        'type': 'text',
	            'displayName': u'Probability',
	            'default': '',
	            'disabled': True
	        }
	    },

	    'gate': {
		    'inherits': 'node',
		    'excludeFromShapesMenu': True,
	        'numberOfIncomingConnections': -1,
	        'numberOfOutgoingConnections':  1,
	        'name': {
		        'default': u'Gate'
	        }
	    },

	    'basicEvent': {
		    'inherits': 'event',
			'excludeFromShapesMenu': False,
		    'numberOfIncomingConnections': 0,
			'image': 'basic_event.svg',
	        'help': 'Initiating failure in a basic component',
	        'name': {
		        'default': u'Basic Event'
	        },
	        'probability': {
				'type': 'number',
				'displayname': u'Exact',
	            'min': 0,
	            'max': 1,
	            'step': 0.01,
	            'default': 0
	        },
	    },

	    'basicEventSet': {
		    'inherits': 'basicEvent',
		    'image': 'basic_event_set.svg',
		    'help': 'Set of basic events with identical properties',
		    'name': {
			    'default': u'Basic Event Set'
		    },
	        'cardinality': {
		        'displayName': u'Cardinality',
	            'type': 'number',
	            'min': 1,
	            'default': 1,
	            'step': 1
	        }
	    },

	    'intermediateEvent': {
		    'inherits': 'event',
			'excludeFromShapesMenu': False,
		    'image': 'intermediate_event.svg',
		    'help': 'Failure resulting from a combination of previous events',
		    'name': {
			    'default': u'Intermediate Event'
		    }
	    },

	    'intermediateEventSet': {
		    'inherits': 'intermediateEvent',
		    'numberOfIncomingConnections': 0,
		    'image': 'intermediate_event_set.svg',
		    'help': 'Set of intermediate events',
		    'name': {
			    'default': u'Intermediate Event Set'
		    },
		    'cardinality': {
			    'displayName': u'Cardinality',
			    'type': 'number',
			    'min': 1,
			    'default': 1,
			    'step': 1
		    }
	    },

		'undevelopedEvent': {
			'inherits': 'event',
			'excludeFromShapesMenu': False,
			'numberOfIncomingConnections': 0,
			'image': 'undeveloped_event.svg',
			'help': 'Event with no information available or insignificant impact',
			'name': {
				'default': u'Undeveloped Event'
			}
		},

		'houseEvent': {
			'inherits': 'event',
			'excludeFromShapesMenu': False,
			'numberOfIncomingConnections': 0,
			'image': 'house_event.svg',
			'help': 'An event that is expected to occur and typically does not denote a failure',
			'name': {
				'default': u'House Event'
			}
		},

		'topEvent': {
			'inherits': 'event',
			'image': 'intermediate_event.svg',
			'excludeFromShapesMenu': True,
		    'optional': None,
		    'name': {
			    'default': u'Top Event'
		    }
		},

	    'andGate': {
		    'inherits': 'gate',
			'excludeFromShapesMenu': False,
		    'image': 'and_gate.svg',
		    'help': 'Output event occurs if all input events occur',
		    'name': {
			    'default': u'AND Gate'
		    }
	    },

	    'priorityAndGate': {
		    'inherits': 'gate',
			'excludeFromShapesMenu': False,
		    'image': 'priority_and_gate.svg',
		    'help': 'Output event occurs if all input events occur in the specific order',
		    'name': {
			    'default': u'Priority AND Gate'
		    }
	    },

	    'orGate': {
		    'inherits': 'gate',
			'excludeFromShapesMenu': False,
		    'image': 'or_gate.svg',
		    'help': 'Output event occurs if one or more input events occur',
		    'name': {
			    'default': u'OR Gate'
		    }
	    },

	    'xorGate': {
		    'inherits': 'gate',
			'excludeFromShapesMenu': False,
		    'image': 'xor_gate.svg',
		    'help': 'Output event occurs if exactly one of the input events occur',
		    'name': {
			    'default': u'XOR Gate'
		    }
	    },

	    'votingOrGate': {
		    'inherits': 'gate',
			'excludeFromShapesMenu': False,
		    'image': 'voting_or_gate.svg',
		    'help': 'Output event occurs if the given number of input events occur',
		    'name': {
			    'default': u'Voting OR Gate'
		    },
	        'count': {
		        'type': 'number',
	            'displayName': u'Count',
	            'min': 1,
	            'step': 1,
	            'default': 2
	        }
	    },

	    'inhibitGate': {
		    'inherits': 'gate',
			'excludeFromShapesMenu': False,
		    'image': 'inhibit_gate.svg',
		    'help': 'Output event occurs if the single input event occurs and the enabling condition is given',
		    'name': {
			    'default': u'Inhibit Gate'
		    }
	    }

	},

    'propertyDisplayOrder': [
		'name',
        'cost',
        'probability',
    ],

    'shapeMenuNodeDisplayOrder': [
	    'basicEvent',
        'basicEventSet',
        'intermediateEvent',
        'intermediateEventSet',
        'andGate',
        'priorityAndGate',
        'orGate',
        'xorGate',
        'votingOrGate',
        'inhibitGate',
        'undevelopedEvent',
        'houseEvent'
    ]
}
