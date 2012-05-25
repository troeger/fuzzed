define(function() {
    return {
        // Layouting
        LAYOUT_SPACING:            0,
        LAYOUT_WEST_SIZE:          250,
        LAYOUT_NORTH_SIZE:         24,
        LAYOUT_EAST_SIZE:          250,

        // Background Grid
        GRID_SIZE:                 50,
        GRID_STROKE:               '#dddddd',
        GRID_STROKE_WIDTH:         1,
        GRID_STROKE_STYLE:         '7, 3',

        // JsPlumb
        JSPLUMB_LINE_STROKE:       '#000000',
        JSPLUMB_LINE_STROKE_WIDTH: 2,
        JSPLUMB_LINE_STYLE:        'Flowchart', 

        JSPLUMB_ENDPOINT_RADIUS:   7,
        JSPLUMB_ENDPOINT_FILL:     '#00d1e0',
        JSPLUMB_ENDPOINT_STYLE:    'Dot',

        // Dragging
        DRAGGING_OPACITY:          0.5,
        DRAGGING_CURSOR:           'move',

        // Type Strings
        BASIC_EVENT:               'basic',
        UNDEVELOPED_EVENT:         'undeveloped',
        HOUSE_EVENT:               'house',
        AND_GATE:                  'and', 
        OR_GATE:                   'or', 
        XOR_GATE:                  'xor',
        PRIORITY_AND_GATE:         'p-and',
        VOTING_OR_GATE:            'v-or',
        INHIBIT_GATE:              'inhibit',
        CHOICE_EVENT:              'choice',
        REDUNDANCY_EVENT:          'redundancy',
        BLOCK:                     'block',

        // Selectors
        TOOLBAR:                   '#FuzzedToolbar',
        SHAPES_MENU:               '#FuzzedShapes',
        CANVAS:                    '#FuzzedCanvas',
        PROPERTIES_MENU:           '#FuzzedProperties',
        FUZZED_CLASS:              '.fuzzed-',
        NODES_CLASS:               '.fuzzed-node'
    };
});