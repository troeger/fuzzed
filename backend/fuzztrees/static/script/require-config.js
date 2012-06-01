define(function() {
    var GRID_SIZE = 60;

    return {
        ShapeMenu: {
            THUMBNAIL_SCALE_FACTOR: 0.7
        },

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
            ENDPOINT_FILL:   '#409FFF',
            ENDPOINT_STYLE:  'Dot'
        },

        Node: {
            LABEL_HEIGHT:    15,
            STROKE_NORMAL:   '#000000',
            STROKE_HOVER:    '#409FFF',
            STROKE_SELECTED: '#FF9640'
        },

        Dragging: {
            OPACITY:        0.5,
            CURSOR:         'move',
            SNAP_TOLERANCE: 10
        },

        Keys: {
            EDITOR:      'editor',
            CONSTRUCTOR: 'constructor',
            NODE:        'node'
        },

        Types: {
            BASIC_EVENT:       'basic',
            MULTI_EVENT:       'multi',
            UNDEVELOPED_EVENT: 'undeveloped',
            FAULT_EVENT:       'fault',
            AND_GATE:          'and',
            PRIORITY_AND_GATE: 'p-and',
            OR_GATE:           'or',
            XOR_GATE:          'xor',
            VOTING_OR_GATE:    'v-or',
            INHIBIT_GATE:      'inhibit',
            CHOICE_EVENT:      'choice',
            REDUNDANCY_EVENT:  'redundancy',
            HOUSE_EVENT:       'house'
        },

        IDs: {
            CONTENT:         'FuzzedContent',
            TOOLBAR:         'FuzzedToolbar',
            SHAPES_MENU:     'FuzzedShapes',
            CANVAS:          'FuzzedCanvas',
            PROPERTIES_MENU: 'FuzzedProperties'
        },

        Classes: {
            NODE:             'fuzzed-node',
            NODE_THUMBNAIL:   'fuzzed-node-thumbnail',
            NODE_IMAGE:       'fuzzed-node-image',
            NODE_LABEL:       'fuzzed-node-label',

            JSPLUMB_ENDPOINT:             'jsplumb-endpoint',
            JSPLUMB_ENDPOINT_DROP_ACTIVE: 'jsplumb-endpoint-drop-active',
            JSPLUMB_ENDPOINT_DROP_HOVER:  'jsplumb-endpoint-drop-hover',
            JSPLUMB_ENDPOINT_HOVER:       'jsplumb-endpoint-hover',

            PROPERTY_LABEL: 'fuzzed-property-label',
            PROPERTY_TEXT:  'fuzzed-property-text' 
        }
    };
});