define(function() {
    var GRID_SIZE   = 53;

    var STROKE_COLOR      = '#000';
    var HIGHLIGHTED_COLOR = '#409FFF';
    var SELECTED_COLOR    = '#FF9640';
    var DISABLED_COLOR    = '#CCC';

    return {
        Backend: {
            BASE_URL:   '/api',
            GRAPHS_URL: '/graphs',
            NODES_URL:  '/nodes',
            EDGES_URL:  '/edges'
        },

        Classes: {
            NODE:                    'fuzzed-node',
            NODE_SELECTED:           'fuzzed-node-selected',
            NODE_IMAGE:              'fuzzed-node-image',
            NODE_DROP_ACTIVE:        'fuzzed-node-drop-active',
            NODE_HALO_CONNECT:       'fuzzed-node-halo-connect',
            NODE_OPTIONAL_INDICATOR: 'fuzzed-node-optional-indicator',

            JSPLUMB_ENDPOINT:        'jsplumb-endpoint',
            JSPLUMB_ENDPOINT_HOVER:  'jsplumb-endpoint-hover'
        },

        Dragging: {
            OPACITY:        0.5,
            CURSOR:         'move',
            SNAP_TOLERANCE: 0
        },

        Grid: {
            SIZE:         GRID_SIZE,
            STROKE:       DISABLED_COLOR,
            STROKE_WIDTH: 1,
            STROKE_STYLE: '7 3' // svg dash-array value
        },

        IDs: {
            CANVAS:          'FuzzEdCanvas',
            CONTENT:         'FuzzEdContent',
            PROPERTIES_MENU: 'FuzzEdProperties',
            SHAPES_MENU:     'FuzzEdShapes',
            SPLASH:          'FuzzEdSplash'
        },

        JSPlumb: {
            STROKE:             STROKE_COLOR,
            STROKE_HIGHLIGHTED: HIGHLIGHTED_COLOR,
            STROKE_SELECTED:    SELECTED_COLOR,
            STROKE_DISABLED:    DISABLED_COLOR,
            STROKE_WIDTH:       2,

            CONNECTOR_STYLE:    'Flowchart',
            CONNECTOR_STUB:     10, // min. distance in px before connector bends

            ENDPOINT_RADIUS: 7,
            ENDPOINT_FILL:   HIGHLIGHTED_COLOR,
            ENDPOINT_STYLE:  'Blank'
        },

        Keys: {
            EDITOR:      'editor',
            CONSTRUCTOR: 'constructor',
            NODE:        'node'
        },

        Node: {
            STROKE_NORMAL:             STROKE_COLOR,
            STROKE_HIGHLIGHTED:        HIGHLIGHTED_COLOR,
            STROKE_SELECTED:           SELECTED_COLOR,
            STROKE_DISABLED:           DISABLED_COLOR,
            OPTIONAL_INDICATOR_FILL:   '#FFF',
            OPTIONAL_INDICATOR_RADIUS: Math.round(GRID_SIZE / 10)
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
                    value:        '',
                    displayname:  ''
                },

                Number: {
                    min:  -Number.MAX_VALUE,
                    max:   Number.MAX_VALUE,
                    step: 1 
                },

                Radio: {
                    options: []
                },

                Range: {
                    min:   -Number.MAX_VALUE,
                    max:    Number.MAX_VALUE,
                    step:  1,
                    value: [0, 1]
                },

                Select: {
                    options: []
                },

                Text: {
                    type: 'text'
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

        Splash: {
            FADE_TIME: 1000
        }
    };
});