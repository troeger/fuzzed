CONFIG = {
    'kind': 'fuzztree',
    'name': u'Fuzz Tree',
    'nodes': {
        'node': {
            'optional': None,
            'numberOfIncomingConnections': -1, #infinite
            'numberOfOutgoingConnections':  1,
            'allowConnectionTo': ['node'],

            'connector': {
                'offset': {
                    'top':    0,
                    'bottom': 0
                }
            }
        },

        'event': {
            'inherits': 'node',

            'optional': False,
            'numberOfIncomingConnections':  1,
            'numberOfOutgoingConnections': -1,
            'allowConnectionTo': ['gate'],

            'cost': 1,
            'probability': 0,

            'propertyMenuEntries': {
                'name': {
                    'kind': 'text',
                    'displayName': u'Name'
                },
                'cost': {
                    'kind': 'number',
                    'displayName': u'Cost',
                    'min': 0,
                    'step': 1
                },
                'probability': {
                    'kind': 'text',
                    'displayName': u'Probability',
                    'disabled': True
                },
                'optional': {
                    'kind': 'checkbox',
                    'displayName': u'Optional'
                }
            },

            'propertyMirrors': {
                # events show their names below the image
                'name': {
                    'position': 'bottom',
                    'style': ['bold', 'large']
                },
                'probability': {
                    'position': 'bottom',
                    'style': ['italic'],
                    'prefix': 'p='
                }
            }
        },

        'gate': {
            'inherits': 'node'
        },

        'basicEvent': {
            'inherits': 'event',

            'name': u'Basic Event',
            'numberOfIncomingConnections': 0,
            'image': 'basic_event.svg',
            'help': 'Initiating failure in a basic component',

            'propertyMenuEntries': {
                'probability': {
                    'kind': 'compound',
                    'disabled': False,

                    'choices': {
                        u'Exact': {
                            'kind': 'number',
                            'min': 0,
                            'max': 1,
                            'step': 0.01
                        },
                        u'Fuzzy': {
                            'kind': 'select',
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
                    }
                }
            }
        },

        'basicEventSet': {
            'inherits': 'basicEvent',

            'name': u'Basic Event Set',
            'image': 'basic_event_set.svg',
            'help': 'Set of basic events with identical properties',
            'cardinality': 1,

            'propertyMenuEntries': {
                'cardinality': {
                    'kind': 'number',
                    'displayName': u'Cardinality',
                    'min': 1,
                    'step': 1,
                }
            },

            'propertyMirrors': {
                'cardinality': {
                    'position': 'bottom',
                    'style': ['italic'],
                    'prefix': '#'
                }
            }
        },

        'intermediateEvent': {
            'inherits': 'event',

            'name': u'Intermediate Event',
            'image': 'intermediate_event.svg',
            'help': 'Failure resulting from a combination of previous events'
        },

        'intermediateEventSet': {
            'inherits': 'intermediateEvent',

            'name': u'Intermediate Event Set',
            'numberOfIncomingConnections': 0,
            'image': 'intermediate_event_set.svg',
            'help': 'Set of intermediate events',
            'cardinality': 1,

            'propertyMenuEntries': {
                'cardinality': {
                    'kind': 'number',
                    'displayName': u'Cardinality',
                    'min': 1,
                    'step': 1
                }
            },

            'propertyMirrors': {
                'cardinality': {
                    'position': 'bottom',
                    'style': ['italic'],
                    'prefix': '#'
                }
            }
        },

        'andGate': {
            'inherits': 'gate',

            'name': u'AND Gate',
            'image': 'and_gate.svg',
            'help': 'Output event occurs if all input events occur'
        },

        'priorityAndGate': {
            'inherits': 'gate',

            'name': u'Priority AND Gate',
            'image': 'priority_and_gate.svg',
            'help': 'Output event occurs if all input events occur in the specific order'
        },

        'orGate': {
            'inherits': 'gate',

            'name': u'OR Gate',
            'image': 'or_gate.svg',
            'help': 'Output event occurs if one or more input events occur'
        },

        'xorGate': {
            'inherits': 'gate',

            'name': u'XOR Gate',
            'image': 'xor_gate.svg',
            'help': 'Output event occurs if exactly one of the input events occur'
        },

        'votingOrGate': {
            'inherits': 'gate',

            'name': u'Voting OR Gate',
            'image': 'voting_or_gate.svg',
            'help': 'Output event occurs if the given number of input events occur',
            'count': 1,

            'propertyMenuEntries': {
                'count': {
                    'kind': 'number',
                    'displayName': u'Count',
                    'min': 1,
                    'step': 1
                }
            },
            'propertyMirrors': {
                'cardinality': {
                    'position': 'bottom',
                    'style': ['italic'],
                    'prefix': 'k='
                }
            }
        },

        'undevelopedEvent': {
            'inherits': 'event',

            'name': u'Undeveloped Event',
            'numberOfIncomingConnections': 0,
            'image': 'undeveloped_event.svg',
            'help': 'Event with no information available or insignificant impact'
        },

        'choiceEvent': {
            'inherits': 'event',

            'name': u'Choice Event',
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

        'redundancyEvent': {
            'inherits': 'event',

            'name': u'Redundancy Event',
            'allowConnectionTo': ['node'],
            'image': 'redundancy_event.svg',
            'help': 'Placeholder for a voting OR gate over a chosen number of the input events',

            'kFormula': u'N-2',
            'nRange': [1, 2], # min, max

            'propertyMenuEntries': {
                'kFormula': {
                    'kind': 'text',
                    'displayName': u'K-Formula'
                },
                'nRange': {
                    'kind': 'range',
                    'displayName': u'N-Range',
                    'min': 1,
                    'step': 1
                }
            },

            'propertyMirrors': {
                'kFormula': {
                    'position': 'bottom',
                    'style': ['italic'],
                    'prefix': 'k: '
                },
                'nRange': {
                    'position': 'bottom',
                    'style': ['italic'],
                    'prefix': 'N: '
                }
            },

            'connector': {
                'dashstyle': '4 2'
            },

            'changedChildProperties': {
                'optional': None
            }
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
            'image': 'top_event.svg',
            'excludeFromShapesMenu': True,
            'optional': None,

            'propertyMenuEntries': {
                'optional': None
            }
        }

        # 'inhibitGate': {
        #     'inherits': 'gate',
        #     'name': u'Inhibit Gate',
        #     'excludeFromShapesMenu': False,
        #     'image': 'inhibit_gate.svg',
        #     'help': 'Output event occurs if the single input event occurs and the enabling condition is given'
        # }
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
        'undevelopedEvent',
        'choiceEvent',
        'redundancyEvent',
        'houseEvent',
        'topEvent',
        #'inhibitGate'
    ],

    # Field: defaults
    #
    # Default elements and properties a new graph is initialized with.
    'defaults': {
        'nodes': [
                {
                'kind': 'topEvent',
                'x': 10,
                'y': 1
            }
        ]
    }
}
