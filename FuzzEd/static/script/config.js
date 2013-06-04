define(['underscore'], function() {
    /**
     *  Package: Base
     */

    /**
     *  Underscore template configuration:
     *    Configure underscores template language to match Django's style.
     */
    _.templateSettings = {
        interpolate: /\{\{(.+?)\}\}/g,
        evaluate:    /\{%(.+?)%\}/g,
        escape:      /\{-(.+?)-\}/g
    }

    /**
     *  Constants:
     *    {String} DEFAULT_COLOR      - Default color for non-highlighted, non-selected, non-disabled strokes.
     *    {String} HIGHLIGHTED_COLOR  - Highlight color of strokes.
     *    {String} SELECTED_COLOR     - Color of selected strokes.
     *    {String} DISABLED_COLOR     - Color of disabled strokes.
     *
     *  Remarks:
     *    Colors are usually given as strings containing the hex value, e.g., '#00AA55' or '#000'.
     */
    var DEFAULT_COLOR     = '#000';
    var HIGHLIGHTED_COLOR = '#409FFF';
    var SELECTED_COLOR    = '#FF9640';
    var DISABLED_COLOR    = '#CCC';

    /**
     *  Structure: Config
     *    Global configuration object containing all necessary constants.
     */
    return {
        /**
         *  Group: Alerts
         *    Configs related to alert messages.
         *
         *  Constants:
         *    {Number} TIMEOUT - Default timeout for alert messages (in ms).
         */
        Alerts: {
            TIMEOUT: 5000 //ms
        },

        /**
         *  Group: Attributes
         *    Names of certain DOM-element attributes.
         *
         *  Constants:
         *    {String} HEADER        - Used in menu containers to specify their button title (when minimized).
         *    {String} CONNECTION_ID - Used to retrieve the Connection object from the corresponding DOM element.
         */
        Attributes: {
            HEADER:        'header',
            CONNECTION_ID: 'fuzzed-id'
        },

        /**
         *  Group: Backend
         *    Backend-specific constants.
         *
         *  Constants:
         *    {String} ANALYSIS_URL              - Part of the sub-URL that is common for all analysis calls.
         *    {String} BASE_URL                  - Part of the sub-URL that is common for all API calls.
         *    {String} EDITOR_URL                - Part of the sub-URL that is common for all editor API calls.
         *    {String} GRAPHS_URL                - Part of the sub-URL used to perform graph-specific API calls.
         *    {String} NODES_URL                 - Part of the sub-URL used to perform node-specific API calls.
         *    {String} EDGES_URL                 - Part of the sub-URL used to perform edge-specific API calls.
         *    {String} TRANSFERS_URL             - Part of the sub-URL used to perform transferable specific API calls.
         *    {String} CUTSETS_URL               - Part of the sub-URL used to perform cutset-specific API calls.
         *    {String} TOP_EVENT_PROBABILITY_URL - Part of the sub-URL used to top event calculation API calls.
         */
        Backend: {
            ANALYSIS_URL:              '/analysis',
            BASE_URL:                  '/api',
            EDITOR_URL:                '/editor',
            GRAPHS_URL:                '/graphs',
            NODES_URL:                 '/nodes',
            EDGES_URL:                 '/edges',
            TRANSFERS_URL:             '/transfers',
            CUTSETS_URL:               '/cutsets',
            TOP_EVENT_PROBABILITY_URL: '/topEventProbability'
        },

        /**
         *  Group: Classes
         *    Names of certain CSS classes.
         *
         *  Constants:
         *    {String} JQUERY_UI_SELECTED      - Class assigned to selected elements by jQuery UI.
         *
         *    {String} JSPLUMB_ENDPOINT        - Class assigned to endpoints by jsPlumb.
         *    {String} JSPLUMB_ENDPOINT_HOVER  - Class assigned to hovered endpoints by jsPlumb.
         *    {String} JSPLUMB_CONNECTOR       - Class assigned to connectors by jsPlumb.
         *    {String} JSPLUMB_CONNECTOR_HOVER - Class assigned to hovered connectors by jsPlumb.
         *
         *    {String} MENU_CONTROLS           - Class of the controls of menus.
         *    {String} MENU_CLOSE              - Class of the close button of menus.
         *    {String} MENU_MINIMIZE           - Class of the minimize button of menus.
         *
         *    {String} MIRROR                  - Class of mirror containers.
         *    {String} MIRROR_BOLD             - Class of bold mirror labels.
         *    {String} MIRROR_ITALIC           - Class of italic mirror labels.
         *    {String} MIRROR_LARGE            - Class of larger mirror labels.
         *
         *    {String} NODE                    - Class of a node's container
         *    {String} NODE_SELECTED           - Class assigned to a node's container when selected.
         *    {String} NODE_IMAGE              - Class of the node's image (the SVG).
         *    {String} NODE_DROP_ACTIVE        - Class assigned to nodes that are valid connection targets
         *                                       (when dragging a new connection).
         *    {String} NODE_HALO_CONNECT       - Class of the connection handle.
         *
         *    {String} NO_PRINT                - Class assigned to elements that should not be printed.
         *
         *    {String} PROPERTY_WARNING        - Class for property input fields if they are erroneous.
         */
        Classes: {
            GRID_HIDDEN:             'fuzzed-grid-hidden',

            JQUERY_UI_SELECTED:      'ui-selected',

            JSPLUMB_ENDPOINT:        'jsplumb-endpoint',
            JSPLUMB_ENDPOINT_HOVER:  'jsplumb-endpoint-hover',
            JSPLUMB_CONNECTOR:       'jsplumb-connector',
            JSPLUMB_CONNECTOR_HOVER: 'jsplumb-connector-hover',

            MENU_CONTROLS:           'menu-controls',
            MENU_CLOSE:              'menu-close',
            MENU_MINIMIZE:           'menu-minimize',

            MIRROR:                  'fuzzed-mirror',
            MIRROR_BOLD:             'fuzzed-mirror-bold',
            MIRROR_ITALIC:           'fuzzed-mirror-italic',
            MIRROR_LARGE:            'fuzzed-mirror-large',

            NODE:                    'fuzzed-node',
            NODE_SELECTED:           'fuzzed-node-selected',
            NODE_IMAGE:              'fuzzed-node-image',
            NODE_DROP_ACTIVE:        'fuzzed-node-drop-active',
            NODE_HALO_CONNECT:       'fuzzed-node-halo-connect',

            NO_PRINT:                'no-print',

            PROPERTY_WARNING:        'error',
            PROPERTY_OPEN_BUTTON:    'fuzzed-property-open'
        },

        /**
         *  Group: Dragging
         *    Configurations for jQuery UI Draggable.
         *
         *  Constants:
         *    {Number} OPACITY        - Opacity of the node when dragging it.
         *    {String} CURSOR         - The cursor style while dragging.
         *    {String} CURSOR_EDGE    - The cursor style while dragging edges.
         *    {Number} SNAP_TOLERANCE - The distance to the border of the editor in which a menu snaps to it.
         */
        Dragging: {
            OPACITY:        0.5,
            CURSOR:         'move',
            CURSOR_EDGE:    'crosshair',
            SNAP_TOLERANCE: 0
        },

        /**
         *  Group: Events
         *    Name of global events triggered on the document with jQuery.trigger().
         *
         *  Constants:
         *    {String} CANVAS_SELECTION_STOPPED - Event triggered when a selection was performed.
         *    {String} CANVAS_SHAPE_DROPPED     - Event triggered when a new shape was dropped on the canvas.
         *    {String} CANVAS_EDGE_SELECTED     - Event triggered when an edge got selected.
         *    {String} CANVAS_EDGE_UNSELECTED   - Event triggered when an edge got unselected.
         *
         *    {String} NODE_PROPERTY_CHANGED    - Event triggered when a property of a node changed.
         *    {String} NODE_DRAG_STOPPED        - Event triggered when a dragged node is dropped again.
         *
         *    {String} GRAPH_NODE_ADDED         - Event triggered when a node was added to the graph.
         *    {String} GRAPH_NODE_DELETED       - Event triggered when a node was deleted from the graph.
         *    {String} GRAPH_EDGE_ADDED         - Event triggered when an edge was added to the graph.
         *    {String} GRAPH_EDGE_DELETED       - Event triggered when an edge was deleted from the graph.
         */
        Events: {
            CANVAS_SELECTION_STOPPED: 'canvas-selection-stopped',
            CANVAS_SHAPE_DROPPED:     'canvas-shape-dropped',
            CANVAS_EDGE_SELECTED:     'canvas-edge-selected',
            CANVAS_EDGE_UNSELECTED:   'canvas-edge-unselected',

            NODE_PROPERTY_CHANGED:    'node-property-changed',
            NODE_DRAG_STOPPED:        'node-drag-stopped',

            GRAPH_NODE_ADDED:         'graph-node-added',
            GRAPH_NODE_DELETED:       'graph-node-deleted',
            GRAPH_EDGE_ADDED:         'graph-edge-added',
            GRAPH_EDGE_DELETED:       'graph-edge-deleted'
        },

        /**
         *  Group: Grid
         *    Metrics for the grid.
         *
         *  Constants:
         *    {Number} SIZE         - Distance between the grid segments of the canvas.
         *    {String} STROKE       - Color of the grid strokes.
         *    {Number} STROKE_WIDTH - With of the grid strokes.
         *    {String} STROKE_STYLE - Dashing style of the grid strokes.
         */
        Grid: {
            SIZE:         53,
            STROKE:       DISABLED_COLOR,
            STROKE_WIDTH: 1,
            STROKE_STYLE: '7 3' // svg dash-array value
        },

        /**
         *  Group: IDs
         *    IDs of certain DOM-elements.
         *
         *  Constants:
         *    {String} ALERT_CONTAINER           - The DOM element containing the alerts messages.
         *    {String} CANVAS                    - The DOM element containing the canvas.
         *    {String} CONTENT                   - The container element for the content (without navbar).
         *    {String} PROPERTIES_MENU           - The container for the properties menu.
         *    {String} SHAPES_MENU               - The container for the shapes menu.
         *    {String} SPLASH                    - The splash screen element.
         *    {String} NAVBAR_ACTIONS            - The list element that contains the action buttons in the navbar.
         *    {String} NAVBAR_ACTION_GRID_TOGGLE - The list element that contains the grid toggle item.
         *    {String} PROGRESS_INDICATOR        - The animated progress indicator gif.
         *    {String} SAVE_INDICATOR            - The navbar entry indicating the save state.
         *    {String} ERROR_INDICATOR           - The navbar entry indicating the error state.
         */
        IDs: {
            ALERT_CONTAINER:           'FuzzEdAlertContainer',
            CANVAS:                    'FuzzEdCanvas',
            CONTENT:                   'FuzzEdContent',
            PROPERTIES_MENU:           'FuzzEdProperties',
            SHAPES_MENU:               'FuzzEdShapes',
            SPLASH:                    'FuzzEdSplash',
            NAVBAR_ACTIONS:            'FuzzEdNavbarActions',
            NAVBAR_ACTION_GRID_TOGGLE: 'FuzzEdNavbarActionGridToggle',
            PROGRESS_INDICATOR:        'FuzzEdProgressIndicator',
            SAVE_INDICATOR:            'FuzzEdSaveIndicator',
            ERROR_INDICATOR:           'FuzzEdErrorIndicator'
        },

        /**
         *  Group: JSPlumb
         *    Configurations for jsPlumb.
         *
         *  Constants:
         *    {String} STROKE_COLOR             - Default stroke color for connectors.
         *    {String} STROKE_COLOR_HIGHLIGHTED - Stroke color for highlighted connectors.
         *    {String} STROKE_COLOR_SELECTED    - Stroke color for selected connectors.
         *    {String} STROKE_COLOR_DISABLED    - Stroke color for disabled connectors.
         *    {Number} STROKE_WIDTH             - Stroke width of connectors.
         *
         *    {String} CONNECTOR_STYLE          - Connector style (see jsPlumb documentation).
         *    {Object} CONNECTOR_OPTIONS        - Additional, connector style-specific options.
         *
         *    {Number} ENDPOINT_RADIUS          - The radius of the endpoints of connections (drag handlers).
         *    {String} ENDPOINT_FILL            - The fill color of endpoints.
         *    {String} ENDPOINT_STYLE           - The style of the endpoints (see jsPlumb documentation).
         */
        JSPlumb: {
            STROKE_COLOR:             DEFAULT_COLOR,
            STROKE_COLOR_HIGHLIGHTED: HIGHLIGHTED_COLOR,
            STROKE_COLOR_SELECTED:    SELECTED_COLOR,
            STROKE_COLOR_DISABLED:    DISABLED_COLOR,
            STROKE_WIDTH:             2,

            CONNECTOR_STYLE:    'Flowchart',
            CONNECTOR_OPTIONS:  {stub: 10 /* min. distance in px before connector bends */},

            ENDPOINT_RADIUS:    7,
            ENDPOINT_FILL:      HIGHLIGHTED_COLOR,
            ENDPOINT_STYLE:     'Blank'
        },

        /**
         *  Group: Keys
         *    Certain keys used with jQuery.data().
         *
         *  Constants:
         *    {String} NODE       - Data key used to get the node object from a associated DOM element.
         *    {String} SELECTABLE - Data key used to store the jQuery UI Selectable object with the canvas
         *                          (needed for some hacks).
         */
        Keys: {
            NODE:       'node',
            SELECTABLE: 'selectable'
        },

        /**
         *  Group: Menus
         *    Menu configurations.
         *
         *  Constants:
         *    {Number} ANIMATION_DURATION      - Duration of the minimize animation (in ms).
         *    {Number} PROPERTIES_MENU_OFFSET  - Offset of the properties menu from the borders.
         *    {Number} PROPERTIES_MENU_TIMEOUT - Number of milliseconds after which a change is propagated.
         */
        Menus: {
            ANIMATION_DURATION:      200,
            PROPERTIES_MENU_OFFSET:  20,
            PROPERTIES_MENU_TIMEOUT: 500
        },

        /**
         *  Group: Node
         *    Configuration of node (visual) properties.
         *
         *  Constants:
         *    {String} STROKE_NORMAL        - Default color of strokes used in node images.
         *    {String} STROKE_HIGHLIGHTED   - Color of strokes used in highlighted node images.
         *    {String} STROKE_SELECTED      - Color of strokes used in selected node images.
         *    {String} STROKE_DISABLED      - Color of strokes used in disabled node images.
         */
        Node: {
            STROKE_NORMAL:             DEFAULT_COLOR,
            STROKE_HIGHLIGHTED:        HIGHLIGHTED_COLOR,
            STROKE_SELECTED:           SELECTED_COLOR,
            STROKE_DISABLED:           DISABLED_COLOR
        },

        /**
         *  Group: Splash
         *    Configurations of the splash screen.
         *
         *  Constants:
         *    {Number} FADE_TIME - The duration of the fade-out animation (in ms).
         */
        Splash: {
            FADE_TIME: 1000
        }
    };
});
