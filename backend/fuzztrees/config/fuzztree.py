FUZZTREE_CONFIG = {
	'nodes': {
		'node': {
			'excludeFromShapesMenu': True,
		    'optional': None,
			'name': u'Node',
		    'numberOfIncomingConnections': -1, #infinite
		    'numberOfOutgoingConnections':  1,
		    'allowConnectionTo': ['node'],
			'connector': {
				'offset': {
					'top': 0,
					'bottom': 0
				}
			},
			'propertiesMenuEntries': {
				'name': {
					'type': 'text',
					'displayName': u'Name'
				},
				'cost': {
					'type': 'number',
					'displayName': u'Cost',
					'min': 0,
					'step': 1,
					'disabled': True #only editable for basic events and sets
				},
				'probability': {
					'type': 'text',
					'displayName': u'Probability',
					'disabled': True
				},
				'optional': {
					'type': 'select'
				},
				'count': {
					'type': 'number',
					'displayName': u'Count',
					'min': 1,
					'step': 1
				},
				'cardinality': {
					'type': 'number',
					'displayName': u'Cardinality',
					'min': 1,
					'step': 1
				},
				'kFormula': {
					'type': 'text',
					'displayName': u'K-Formula'
				},
				'nRange': {
					'type': 'range',
					'displayName': u'N-Range',
					'min': 1,
					'step': 1
				}
			}
		},

	    'event': {
		    'inherits': 'node',
		    'excludeFromShapesMenu': True,
	        'optional': False,
			'name': u'Event',
			'cost': 1,
			'probability': '',
	        'numberOfIncomingConnections':  1,
	        'numberOfOutgoingConnections': -1,
	        'allowConnectionTo': ['gate'],
			'propertyMirrors': {
				# events show their names below the image
				'name': {
					'position': 'bottom',
					'style': ['bold']
				}
			}
	    },

	    'gate': {
		    'inherits': 'node',
		    'excludeFromShapesMenu': True,
	        'optional': None,
			'name': u'Gate',
	        'numberOfIncomingConnections': -1,
	        'numberOfOutgoingConnections':  1
	    },

	    'basicEvent': {
		    'inherits': 'event',
			'excludeFromShapesMenu': False,
			'name': u'Basic Event',
			'probability': 0, # numerical means 'Exact' option TODO: find better way
		    'numberOfIncomingConnections': 0,
			'image': 'basic_event.svg',
	        'help': 'Initiating failure in a basic component',
			'propertiesMenuEntries': {
				'cost': {
					'disabled': False
				},
				'probability': {
					'type': 'option',
					'choices': {
						u'Exact': {
							'type': 'number',
							'min': 0,
							'max': 1,
							'step': 0.01
						},
						u'Fuzzy': {
							'type': 'select',
							'choices': [
								u'never',
								u'very unlikely',
								u'unlikely',
								u'more or less',
								u'likely',
								u'very likely',
								u'always'
							]
						}
					},
					'disabled': False
				}
			}
	    },

	    'basicEventSet': {
		    'inherits': 'basicEvent',
			'name': u'Basic Event Set',
			'cardinality': 1,
		    'image': 'basic_event_set.svg',
		    'help': 'Set of basic events with identical properties'
	    },

	    'intermediateEvent': {
		    'inherits': 'event',
			'name': u'Intermediate Event',
			'excludeFromShapesMenu': False,
		    'image': 'intermediate_event.svg',
		    'help': 'Failure resulting from a combination of previous events'
	    },

	    'intermediateEventSet': {
		    'inherits': 'intermediateEvent',
			'name': u'Intermediate Event Set',
			'cardinality': 1,
		    'numberOfIncomingConnections': 0,
		    'image': 'intermediate_event_set.svg',
		    'help': 'Set of intermediate events'
	    },

		'redundancyEvent': {
			'inherits': 'event',
			'name': u'Redundancy Event',
			'kFormula': u'N-2',
			'nRange': [1, 2], # min, max
			'excludeFromShapesMenu': False,
			'allowConnectionTo': ['node'],
			'image': 'redundancy_event.svg',
			'help': 'Placeholder for a voting OR gate over a chosen number of the input events',
		    'connector': {
				'dashstyle': '4 2'
		    },
		    'changedChildProperties': {
			    'optional': None
		    }
		},

		'choiceEvent': {
			'inherits': 'event',
			'name': u'Choice Event',
			'excludeFromShapesMenu': False,
			'allowConnectionTo': ['event'],
			'image': 'choice_event.svg',
			'help': 'Placeholder for one of the input events',
			'connector': {
				'dashstyle': '4 2'
			},
			'changedChildProperties': {
				'optional': None
			}
		},

		'undevelopedEvent': {
			'inherits': 'event',
			'name': u'Undeveloped Event',
			'excludeFromShapesMenu': False,
			'numberOfIncomingConnections': 0,
			'image': 'undeveloped_event.svg',
			'help': 'Event with no information available or insignificant impact'
		},

		'houseEvent': {
			'inherits': 'event',
			'name': u'House Event',
			'excludeFromShapesMenu': False,
			'numberOfIncomingConnections': 0,
			'image': 'house_event.svg',
			'help': 'An event that is expected to occur and typically does not denote a failure'
		},

		'topEvent': {
			'inherits': 'event',
			'name': u'Top Event',
			'image': 'intermediate_event.svg',
			'excludeFromShapesMenu': True,
		    'optional': None
		},

	    'andGate': {
		    'inherits': 'gate',
			'name': u'AND Gate',
			'excludeFromShapesMenu': False,
		    'image': 'and_gate.svg',
		    'help': 'Output event occurs if all input events occur'
	    },

	    'priorityAndGate': {
		    'inherits': 'gate',
			'name': u'Priority AND Gate',
			'excludeFromShapesMenu': False,
		    'image': 'priority_and_gate.svg',
		    'help': 'Output event occurs if all input events occur in the specific order'
	    },

	    'orGate': {
		    'inherits': 'gate',
			'name': u'OR Gate',
			'excludeFromShapesMenu': False,
		    'image': 'or_gate.svg',
		    'help': 'Output event occurs if one or more input events occur'
	    },

	    'xorGate': {
		    'inherits': 'gate',
			'name': u'XOR Gate',
			'excludeFromShapesMenu': False,
		    'image': 'xor_gate.svg',
		    'help': 'Output event occurs if exactly one of the input events occur'
	    },

	    'votingOrGate': {
		    'inherits': 'gate',
			'name': u'Voting OR Gate',
			'count': 2,
			'excludeFromShapesMenu': False,
		    'image': 'voting_or_gate.svg',
		    'help': 'Output event occurs if the given number of input events occur'
	    },

	    'inhibitGate': {
		    'inherits': 'gate',
			'name': u'Inhibit Gate',
			'excludeFromShapesMenu': False,
		    'image': 'inhibit_gate.svg',
		    'help': 'Output event occurs if the single input event occurs and the enabling condition is given'
	    }

	},

	'propertiesDisplayOrder': [
		'name',
		'cost',
		'probability',
		'optional',
		'count',
		'cardinality',
		'kFormula',
		'nRange'
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
        'choiceEvent',
        'redundancyEvent',
        'undevelopedEvent',
        'houseEvent'
    ]
}
