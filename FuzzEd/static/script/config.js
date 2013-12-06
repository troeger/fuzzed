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
    };

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
            TOP_EVENT_PROBABILITY_URL: '/topEventProbability',
            GRAPH_EXPORT_URL:          '/exports'
        },

        /**
         *  Group: Classes
         *    Names of certain CSS classes.
         *
         *  Constants:
         *    {String} HIGHLIGHTED             - Class assigned to highlighted elements.
         *    {String} SELECTED                - Class assigned to selected elements (using jQuery UI Selectable).
         *    {String} SELECTING               - Class assigned to elements that are currently being selected
         *                                       (using jQuery UI Selectable).
         *    {String} DISABLED                - Class assigned to disabled (grayed-out) elements.
         *
         *    {STRING} CANVAS_NOT_EDITABLE     - Class assigned to the canvas in order to hide any interactive elements
         *                                       while highlighting nodes in any kinds of analytical summary
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
         *    {String} NODE                    - Class of a node's container.
         *    {String} NODE_IMAGE              - Class of the node's image (the SVG).
         *    {String} NODE_DROP_ACTIVE        - Class assigned to nodes that are valid connection targets
         *                                       (when dragging a new connection).
         *    {String} NODE_HALO_CONNECT       - Class of the connection handle.
         *
         *    {String} NO_PRINT                - Class assigned to elements that should not be printed.
         *
         *    {String} PROPERTY_WARNING        - Class for property input fields if they are erroneous.
         *    {String} PROPERTY_OPEN_BUTTON    - Class for transfer property 'open' buttons.
         *
         *    {String} ICON_SUCCESS            - Class for the icon that indicates a successful action.
         *    {String} ICON_ERROR              - Class for the icon that indicates an erroneous action.
         *    {String} ICON_PROGRESS           - Class for the icon that indicates an action in progress.
         *
         *    {String} DRAGGABLE_WRAP_DIV	   - Class for div in shapes menu that contains thumbnail
		 *    {String} RESIZABLE               - Class indicating that a node is resizable
		 *    {String} EDITABLE                - Class indicating that a node is inline editable
         */
        Classes: {
            HIGHLIGHTED:             'highlighted',
            SELECTED:                'ui-selected',
            SELECTING:               'ui-selecting',
            DISABLED:                'disabled',

            CANVAS_NOT_EDITABLE:     'fuzzed-canvas-not-editable',

            GRID_HIDDEN:             'fuzzed-grid-hidden',

            JSPLUMB_ENDPOINT:        'jsplumb-endpoint',
            JSPLUMB_CONNECTOR:       'jsplumb-connector',

            MENU_CONTROLS:           'menu-controls',
            MENU_CLOSE:              'menu-close',
            MENU_MINIMIZE:           'menu-minimize',

            MIRROR:                  'fuzzed-mirror',
            MIRROR_BOLD:             'fuzzed-mirror-bold',
            MIRROR_ITALIC:           'fuzzed-mirror-italic',
            MIRROR_LARGE:            'fuzzed-mirror-large',

            NODE:                    'fuzzed-node',
            NODE_IMAGE:              'fuzzed-node-image',
            NODE_DROP_ACTIVE:        'fuzzed-node-drop-active',
            NODE_HALO_CONNECT:       'fuzzed-node-halo-connect',

            NO_PRINT:                'no-print',

            PROPERTY_WARNING:        'error',
            PROPERTY_OPEN_BUTTON:    'fuzzed-property-open',

            ICON_SUCCESS:            'icon-ok',
            ICON_ERROR:              'icon-warning-sign',
            ICON_PROGRESS:           'icon-progress',

			DRAGGABLE_WRAP_DIV: 	 'draggableDiv',
			RESIZABLE:			 	 'resizable',
			EDITABLE:			 	 'editable'
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
         *    {String} CANVAS_SELECTION_STOPPED  - Event triggered when a selection was performed.
         *    {String} CANVAS_SHAPE_DROPPED      - Event triggered when a new shape was dropped on the canvas.
         *    {String} CANVAS_EDGE_SELECTED      - Event triggered when an edge got selected.
         *    {String} CANVAS_EDGE_UNSELECTED    - Event triggered when an edge got unselected.
         *
         *    {String} GRAPH_NODE_ADDED          - Event triggered when a node was added to the graph.
         *    {String} GRAPH_NODE_DELETED        - Event triggered when a node was deleted from the graph.
         *    {String} GRAPH_EDGE_ADDED          - Event triggered when an edge was added to the graph.
         *    {String} GRAPH_EDGE_DELETED        - Event triggered when an edge was deleted from the graph.
         *
         *    {String} NODE_DRAG_STOPPED         - Event triggered when a dragged node is dropped again.
         *
         *    {String} PROPERTY_CHANGED          - Event triggered when a property of a node changed.
         *    {String} PROPERTY_HIDDEN_CHANGED   - Event triggered when a property's hidden state changed.
         *    {String} PROPERTY_READONLY_CHANGED - Event triggered when a property's readonly state changed.
         *    {String} PROPERTY_SYNCHRONIZED     - Event triggered when a property synced itself with the backend.
         *
         *    {String} NODE_UNSELECTED           - Event triggered when a node on the canvas is unselected
		 *    {String} NODE_SELECTED             - Event triggered when a node on the canvas is selected		
		 */
        Events: {
            CANVAS_SELECTION_STOPPED:  'canvas-selection-stopped',
            CANVAS_SHAPE_DROPPED:      'canvas-shape-dropped',
            CANVAS_EDGE_SELECTED:      'canvas-edge-selected',
            CANVAS_EDGE_UNSELECTED:    'canvas-edge-unselected',

            GRAPH_NODE_ADDED:          'graph-node-added',
            GRAPH_NODE_DELETED:        'graph-node-deleted',
            GRAPH_EDGE_ADDED:          'graph-edge-added',
            GRAPH_EDGE_DELETED:        'graph-edge-deleted',

            NODE_DRAG_STOPPED:         'node-drag-stopped',

            PROPERTY_CHANGED:          'property-changed',
            PROPERTY_HIDDEN_CHANGED:   'property-hidden-changed',
            PROPERTY_READONLY_CHANGED: 'property-readonly-changed',
            PROPERTY_SYNCHRONIZED:     'property-synchronized',
			
			NODE_UNSELECTED:		   'node_unselected',
			NODE_SELECTED:             'node_selected'
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
         *    {String} ALERT_CONTAINER             - The DOM element containing the alerts messages.
         *    {String} CANVAS                      - The DOM element containing the canvas.
         *    {String} CONTENT                     - The container element for the content (without navbar).
         *    {String} PROPERTIES_MENU             - The container for the properties menu.
         *    {String} SHAPES_MENU                 - The container for the shapes menu.
         *    {String} SPLASH                      - The splash screen element.
         *    {String} ACTION_GRID_TOGGLE          - The list element that contains the grid toggle menu entry.
         *    {String} ACTION_CUTSETS              - The list element that contains the cut set analysis menu entry.
         *    {String} ACTION_ANALYTICAL           - The list element that contains the analytical analysis menu entry.
         *    {String} PROGRESS_INDICATOR_SINGLE   - The nav entry containing the progress indicator for single active jobs.
         *    {String} PROGRESS_INDICATOR_DROPDOWN - The nav entry containing the dropdown for multiple active jobs.
         */
        IDs: {
            ALERT_CONTAINER:             'FuzzEdAlertContainer',
            CANVAS:                      'FuzzEdCanvas',
            CONTENT:                     'FuzzEdContent',
            PROPERTIES_MENU:             'FuzzEdProperties',
            SHAPES_MENU:                 'FuzzEdShapes',
            SPLASH:                      'FuzzEdSplash',
            ACTION_GRID_TOGGLE:          'FuzzEdActionGridToggle',
            ACTION_CUTSETS:              'FuzzEdActionCutsets',
            ACTION_ANALYTICAL:           'FuzzEdActionAnalytical',
            ACTION_EXPORT_PDF:           'FuzzEdActionExportPDF',
            ACTION_EXPORT_EPS:           'FuzzEdActionExportEPS',
            PROGRESS_INDICATOR_SINGLE:   'FuzzEdProgressIndicatorSingle',
            PROGRESS_INDICATOR_DROPDOWN: 'FuzzEdProgressIndicatorDropdown'
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
            SELECTABLE: 'ui-selectable'
        },

        /**
         *  Group: Menus
         *    Menu configurations.
         *
         *  Constants:
         *    {Number} ANIMATION_DURATION      - Duration of the minimize animation (in ms).
         *    {Number} MENU_OFFSET             - Offset of the menus from the canvas borders.
         *    {Number} PROPERTIES_MENU_TIMEOUT - Number of milliseconds after which a change is propagated.
         */
        Menus: {
            ANIMATION_DURATION:      200,
            MENU_OFFSET:             20,
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
         *  Group: ProgressIndicator
         *    Configurations for the progress indicator in the navbar.
         *
         *  Constants:
         *    {Number} SUCCESS_FLASH_DELAY       - Delay in ms before hiding the progress indicator of a successful action.
         *    {Number} ERROR_FLASH_DELAY         - Delay in ms before hiding the progress indicator of an erroneous action.
         *    {Number} PROGRESS_APPEARANCE_DELAY - Delay in ms before showing a progress indicator.
         *
         *    {String} DEFAULT_PROGRESS_MESSAGE  - The default status message for active actions.
         *    {String} DEFAULT_SUCCESS_MESSAGE   - The default status message for successful actions.
         *    {String} DEFAULT_ERROR_MESSAGE     - The default status message for erroneous actions.
         *    {String} DEFAULT_NOT_FOUND_MESSAGE - The default status message for actions resulting in a 404.
         *    {String} DEFAULT_CANCELED_MESSAGE  - The default status message when canceling jobs.
         *
         *    {String} EXPORT_PROGRESS_MESSAGE   - The message displayed when exporting the graph. The file name will be appended.
         *    {String} EXPORT_SUCCESS_MESSAGE    - The message displayed when the graph has been successfully exported.
         *    {String} EXPORT_ERROR_MESSAGE      - The message displayed when there was an error while exporting the graph.
         *
         *    {String} CALCULATING_MESSAGE       - The message displayed for calculation jobs.
         */
        ProgressIndicator: {
            SUCCESS_FLASH_DELAY:       600,
            ERROR_FLASH_DELAY:         5000,
            PROGRESS_APPEARANCE_DELAY: 500,

            DEFAULT_PROGRESS_MESSAGE:  'Working…',
            DEFAULT_SUCCESS_MESSAGE:   'Done',
            DEFAULT_ERROR_MESSAGE:     'Error',
            DEFAULT_NOT_FOUND_MESSAGE: 'Not found',
            DEFAULT_CANCELED_MESSAGE:  'Canceled',

            EXPORT_PROGRESS_MESSAGE:   'Exporting graph as ', // file name will be appended
            EXPORT_SUCCESS_MESSAGE:    'Done',
            EXPORT_ERROR_MESSAGE:      'Failed to export as ', // file name will be appended

            CALCULATING_MESSAGE:       'Calculating...'
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
