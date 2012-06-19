define(function() {
    var GRID_SIZE = 70;

    return {
        Classes: {
            NODE:             'fuzzed-node',
            NODE_THUMBNAIL:   'fuzzed-node-thumbnail',
            NODE_IMAGE:       'fuzzed-node-image',
            NODE_LABEL:       'fuzzed-node-label',
            NODE_DROP_ACTIVE: 'fuzzed-node-drop-active',
            NODE_HALO_CONNECT:'fuzzed-node-halo-connect',

            JSPLUMB_ENDPOINT:       'jsplumb-endpoint',
            JSPLUMB_ENDPOINT_HOVER: 'jsplumb-endpoint-hover',

            PROPERTIES:                 'fuzzed-properties',
            PROPERTY_LABEL:             'fuzzed-property-label',
            PROPERTY_LABEL_PROBABILITY: 'fuzzed-node-label-probability',
            PROPERTY_SELECT:            'fuzzed-property-select',
            PROPERTY_TEXT:              'fuzzed-property-text'
        },

        Backend: {
            BASE_URL:   '/api',
            GRAPHS_URL: '/graphs',
            NODES_URL:  '/nodes',
            EDGES_URL:  '/edges'
        },

        Dragging: {
            OPACITY:        0.5,
            CURSOR:         'move',
            SNAP_TOLERANCE: 10
        },

        Grid: {
            SIZE:         GRID_SIZE,
            HALF_SIZE:    GRID_SIZE >> 1,
            STROKE:       '#ddd',
            STROKE_WIDTH: 1,
            STROKE_STYLE: '7 3' // svg dash-array value
        },

        IDs: {
            SPLASH:          'FuzzedSplash',
            CONTENT:         'FuzzedContent',
            TOOLBAR:         'FuzzedToolbar',
            SHAPES_MENU:     'FuzzedShapes',
            CANVAS:          'FuzzedCanvas',
            PROPERTIES_MENU: 'FuzzedProperties'
        },

        JSPlumb: {
            STROKE:             '#000',
            STROKE_HIGHLIGHTED: '#409FFF',
            STROKE_SELECTED:    '#FF9640',
            STROKE_DISABLED:    '#CCC',
            STROKE_WIDTH:       2,
            STROKE_STYLE:       'Flowchart',

            ENDPOINT_RADIUS: 7,
            ENDPOINT_FILL:   '#409FFF',
            ENDPOINT_STYLE:  'Dot'
        },

        Keys: {
            EDITOR:      'editor',
            CONSTRUCTOR: 'constructor',
            NODE:        'node'
        },

        Node: {
            LABEL_HEIGHT:       15,
            STROKE_NORMAL:      '#000000',
            STROKE_HIGHLIGHTED: '#409FFF',
            STROKE_SELECTED:    '#FF9640',
            STROKE_DISABLED:    '#CCC',

            Names: {
                BASIC_EVENT:       'Basic Event',
                MULTI_EVENT:       'Multi Event',
                FAULT_EVENT:       'Fault Event',
                MULTI_FAULT_EVENT: 'Multi Fault Event',
                AND_GATE:          'AND Gate',
                PRIORITY_AND_GATE: 'Priority AND Gate',
                OR_GATE:           'OR Gate',
                XOR_GATE:          'XOR Gate',
                VOTING_OR_GATE:    'Voting OR Gate',
                INHIBIT_GATE:      'Inhibit Gate',
                CHOICE_EVENT:      'Choice Event',
                REDUNDANCY_EVENT:  'Redundancy Event',
                UNDEVELOPED_EVENT: 'Undeveloped Event',
                HOUSE_EVENT:       'House Event'
            },

            Types: {
                BASIC_EVENT:       'basic',
                MULTI_EVENT:       'multi',
                FAULT_EVENT:       'fault',
                MULTI_FAULT_EVENT: 'multi_fault',
                AND_GATE:          'and',
                PRIORITY_AND_GATE: 'p-and',
                OR_GATE:           'or',
                XOR_GATE:          'xor',
                VOTING_OR_GATE:    'v-or',
                INHIBIT_GATE:      'inhibit',
                CHOICE_EVENT:      'choice',
                REDUNDANCY_EVENT:  'redundancy',
                UNDEVELOPED_EVENT: 'undeveloped',
                HOUSE_EVENT:       'house'
            }
        },

        Properties: {
            Defaults: {
                Basic: {
                    disabled:     false,
                    mirror:       null,
                    mirrorPrefix: '',
                    mirrorSuffix: '',
                    mirrorClass:  [],
                    name:         '',
                    value:        ''
                },

                Number: {
                    type: 'text',
                    max:   Number.MAX_VALUE,
                    min:  -Number.MAX_VALUE,
                    step: 1 
                },

                Pattern: {
                    pattern: '[.*]'
                },

                Select: {
                    options: []
                },

                Text: {
                    type: ''
                }
            },

            Events: [
                'blur',
                'change',
                'click',
                'focus',
                'keydown',
                'keyup',
                'select'
            ]
        },

        ShapeMenu: {
            THUMBNAIL_SCALE_FACTOR: 0.7
        },

        Splash: {
            FADE_TIME: 500
        }
    };
});