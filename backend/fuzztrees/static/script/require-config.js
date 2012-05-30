define(function() {
    var GRID_SIZE = 80;

    return {
        Grid: {
            SIZE:         GRID_SIZE,
            HALF_SIZE:    GRID_SIZE >> 1,
            STROKE:       '#ddd',
            STROKE_WIDTH: 1,
            STROKE_STYLE: '7 3' // svg dash-array value
        },

        JSPlumb: {
            STROKE:         '#000',
            STROKE_WIDTH:   2,
            STROKE_STYLE:   'Flowchart',

            ENDPOINT_RADIUS: 7,
            ENDPOINT_FILL:   '#00d1e0',
            ENDPOINT_STYLE:  'Dot'
        },

        Dragging: {
            OPACITY:        0.5,
            CURSOR:         'move',
            SNAP_TOLERANCE: 10
        },

        Keys: {
            CONSTRUCTOR: 'constructor',
            NODE:        'node'
        },

        Types: {
            BASIC_EVENT:       'basic',
            MULTI_EVENT:       'multi',
            UNDEVELOPED_EVENT: 'undeveloped',
            HOUSE_EVENT:       'house',
            AND_GATE:          'and', 
            OR_GATE:           'or', 
            XOR_GATE:          'xor',
            PRIORITY_AND_GATE: 'p-and',
            VOTING_OR_GATE:    'v-or',
            INHIBIT_GATE:      'inhibit',
            CHOICE_EVENT:      'choice',
            REDUNDANCY_EVENT:  'redundancy'
        },

        Selectors: {
            IDs: {
                CONTENT:         '#FuzzedContent',
                TOOLBAR:         '#FuzzedToolbar',
                SHAPES_MENU:     '#FuzzedShapes',
                CANVAS:          '#FuzzedCanvas',
                PROPERTIES_MENU: '#FuzzedProperties'
            },

            Classes: {
                PREFIX:         '.fuzzed-',
                NODE:           '.fuzzed-node',
                NODE_THUMBNAIL: '.fuzzed-node-thumbnail',
                SELECTED:       '.fuzzed-node-selected'
            }
        }
    };
});