FUZZTREE_CONFIG = {
	'nodes': {
		'node': {
			'excludeFromShapesMenu': True,
		    'optional': None,
		    'numberOfIncomingConnections': -1, #infinite
		    'numberOfOutgoingConnections':  1,
		    'allowConnectionTo': ['node'],
			'connector': {
				'offset': {
					'top': 0,
					'bottom': 0
				}
			},
		    'name': {
			    'type': 'text',
		        'displayName': u'Name',
			    'default': u'Node'
		    }
		},

	    'event': {
		    'inherits': 'node',
		    'excludeFromShapesMenu': True,
	        'optional': False,
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
	        },
	        'cost': {
		        'type': 'number',
				'displayName': u'Cost',
	            'min': 0,
	            'step': 1,
	            'default': 1,
	            'disabled': True #only editable for basic events and sets
	        },
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
	        'optional': None,
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
			            'step': 0.01,
			            'default': 0
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
		                ],
		                'default': 'never'
		            }
		        },
	            'default': u'Exact'
	        }
	    },

	    'basicEventSet': {
		    'inherits': 'basicEvent',
		    'image': 'basic_event_set.svg',
		    'help': 'Set of basic events with identical properties',
		    'name': {
			    'default': u'Basic Event Set'
		    },
		    'cost': {
			    'disabled': False
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

		'redundancyEvent': {
			'inherits': 'event',
			'excludeFromShapesMenu': False,
			'allowConnectionTo': ['node'],
			'image': 'redundancy_event.svg',
			'help': 'Placeholder for a voting OR gate over a chosen number of the input events',
		    'connector': {
				'dashstyle': '4 2'
		    },
		    'changedChildProperties': {
			    'optional': None
		    },
			'name': {
				'default': u'Redundancy Event'
			},
		    'kFormula': {
			    'type': 'text',
		        'displayName': u'K-Formula',
		        'default': u'N-2'
		    },
		    'nRange': {
			    'type': 'range',
		        'displayName': u'N-Range',
		        'min': 1,
		        'step': 1,
		        'default': [1, 2] # min, max
		    }
		},

		'choiceEvent': {
			'inherits': 'event',
			'excludeFromShapesMenu': False,
			'allowConnectionTo': ['event'],
			'image': 'choice_event.svg',
			'help': 'Placeholder for one of the input events',
			'connector': {
				'dashstyle': '4 2'
			},
			'changedChildProperties': {
				'optional': None
			},
			'name': {
				'default': u'Choice Event'
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
        'optional',
        'count',
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
