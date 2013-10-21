define(['class', 'menus', 'canvas', 'backend', 'alerts', 'progressIndicator', 'jquery-classlist'],
function(Class, Menus, Canvas, Backend, Alerts, Progress) {
    /**
     *  Package: Base
     */

    /**
     *  Class: Editor
     *
     *  This is the _abstract_ base class for all graph-kind-specific editors. It manages the visual components
     *  like menus and the graph itself. It is also responsible for global keybindings.
     */
    return Class.extend({
        /**
         *  Group: Members
         *
         *  Properties:
         *    {Object}          config                      - Graph-specific <Config> object.
         *    {Graph}           graph                       - <Graph> instance to be edited.
         *    {PropertiesMenu}  properties                  - The <Menu::PropertiesMenu> instance used by this editor
         *                                                    for changing the properties of nodes of the edited graph.
         *    {ShapesMenu}      shapes                      - The <Menu::ShapeMenu> instance use by this editor to show
         *                                                    the available shapes for the kind of the edited graph.
         *    {Backend}         _backend                    - The instance of the <Backend> that is used to communicate
         *                                                    graph changes to the server.
         *    {Object}          _currentMinContentOffsets   - Previously calculated minimal content offsets.
         *    {jQuery Selector} _nodeOffsetPrintStylesheet  - The dynamically generated and maintained stylesheet
         *                                                    used to fix the node offset when printing the page.
         *    {Underscore Template} _nodeOffsetStylesheetTemplate - The underscore.js template used to generate the
         *                                                          CSS transformation for <_nodeOffsetPrintStylesheet>.
         */
        config:                        undefined,
        graph:                         undefined,
        properties:                    undefined,
        shapes:                        undefined,

        _backend:                      undefined,
        _currentMinNodeOffsets:        {'top': 0, 'left': 0},
        _nodeOffsetPrintStylesheet:    undefined,
        _nodeOffsetStylesheetTemplate: undefined,

        /**
         *  Group: Initialization
         */

        /**
         *  Constructor: init
         *    Sets up the editor interface and necessary callbacks and loads the graph with the given ID
         *    from the backend.
         *
         *  Parameters:
         *    {int} graphId - The ID of the graph that is going to be edited by this editor.
         */
        init: function(graphId) {
            if (typeof graphId !== 'number')
                throw new TypeError('numeric graph ID', typeof graphId);

            this.config   = this.getConfig();
            this._backend = new Backend(graphId);

            // remember certain UI elements
            this._progressIndicator = jQuery('#' + this.config.IDs.PROGRESS_INDICATOR);
            this._progressMessage = jQuery('#' + this.config.IDs.PROGRESS_MESSAGE);

            // run a few sub initializer
            this._setupJsPlumb()
                ._setupNodeOffsetPrintStylesheet()
                ._setupEventCallbacks()
                ._setupMenuActions();

            // fetch the content from the backend
            this._loadGraph(graphId);
        },

        /**
         *  Group: Accessors
         */

        /**
         *  Method: getConfig
         *    _Abstract_, needs to be overridden in specific editor classes.
         *
         *  Returns:
         *    The <Config> object that corresponds to the loaded graph's kind.
         */
        getConfig: function() {
            throw new SubclassResponsibility();
        },

        /**
         *  Method: getGraphClass
         *    _Abstract_, needs to be overridden in specific editor classes.
         *
         *  Returns:
         *    The specific <Graph> class that should be used to instantiate the editor's graph with information
         *    loaded from the backend.
         */
        getGraphClass: function() {
            throw new SubclassResponsibility();
        },

        /**
         *  Group: Graph Loading
         */

        /**
         *  Method: _loadGraph
         *    Asynchronously loads the graph with the given ID from the backend.
         *    <_loadGraphFromJson> will be called when done.
         *
         *  Parameters:
         *    {int} graphId - ID of the graph that should be loaded.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _loadGraph: function(graphId) {
            this._backend.getGraph(
                this._loadGraphFromJson.bind(this),
                this._loadGraphError.bind(this)
            );

            return this;
        },

        /**
         *  Method: _loadGraphCompleted
         *    Callback that gets fired when the graph is loaded completely.
         *    We need to perform certain actions afterwards, like initialization of menus and activation of
         *    backend observers to prevent calls to the backend while the graph is initially constructed.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _loadGraphCompleted: function(readOnly) {
            // create manager objects for the bars
            this.properties = new Menus.PropertiesMenu(this.graph.getNotation().propertiesDisplayOrder);
            this.shapes     = new Menus.ShapeMenu();
            this._backend.activate();

            if (readOnly) {
                Alerts.showInfoAlert('Remember:', 'this diagram is read-only');
                this.shapes.disable();
                this.properties.disable();
                Canvas.disableInteraction();
            }

            this._setupKeyBindings(readOnly);
            // fade out the splash screen
            jQuery('#' + this.config.IDs.SPLASH).fadeOut(this.config.Splash.FADE_TIME, function() {
                jQuery(this).remove();
            });

            return this;
        },

        /**
         *  Method: _loadGraphError
         *    Callback that gets called in case <_loadGraph> results in an error.
         */
        _loadGraphError: function(response, textStatus, errorThrown) {
            throw new NetworkError('could not retrieve graph');
        },

        /**
         *  Method: _loadGraphFromJson
         *    Callback triggered by the backend, passing the loaded JSON representation of the graph.
         *    It will initialize the editor's graph instance using the <Graph> class returned in <getGraphClass>.
         *
         *  Parameters:
         *    {JSON} json - JSON representation of the graph, loaded from the backend.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _loadGraphFromJson: function(json) {
            this.graph = new (this.getGraphClass())(json);
            this._loadGraphCompleted(json.readOnly);

            return this;
        },

        /**
         *  Group: Setup
         */

        /**
         *  Method: _setupMenuActions
         *
         *  Registers the event handlers for graph type - independent menu entries that trigger JS calls
         *
         *  Returns:
         *    This {<Node>} instance for chaining.
         */
        _setupMenuActions: function() {
            jQuery("#"+this.config.IDs.ACTION_GRID_TOGGLE).click(function() {
                Canvas.toggleGrid();
            }.bind(this));

            return this;
        },

        /**
         *  Method: _setupJsPlumb
         *    Sets all jsPlumb defaults used by this editor.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _setupJsPlumb: function() {
            jsPlumb.importDefaults({
                EndpointStyle: {
                    fillStyle:   this.config.JSPlumb.ENDPOINT_FILL
                },
                Endpoint:        [this.config.JSPlumb.ENDPOINT_STYLE, {
                    radius:      this.config.JSPlumb.ENDPOINT_RADIUS,
                    cssClass:    this.config.Classes.JSPLUMB_ENDPOINT,
                    hoverClass:  this.config.Classes.HIGHLIGHTED
                }],
                PaintStyle: {
                    strokeStyle: this.config.JSPlumb.STROKE_COLOR,
                    lineWidth:   this.config.JSPlumb.STROKE_WIDTH
                },
                HoverClass:      this.config.Classes.HIGHLIGHTED,
                Connector:       [this.config.JSPlumb.CONNECTOR_STYLE, this.config.JSPlumb.CONNECTOR_OPTIONS],
                ConnectionsDetachable: false
            });

            jsPlumb.connectorClass = this.config.Classes.JSPLUMB_CONNECTOR;

            return this;
        },

        /**
         *  Method: _setupKeyBindings
         *    Setup the global key bindings
         *
         *  Keys:
         *    ESCAPE - Clear selection.
         *    DELETE - Delete all selected elements (nodes/edges).
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _setupKeyBindings: function(readOnly) {
            if (readOnly) return this;

            jQuery(document).keydown(function(event) {
                if (event.which == jQuery.ui.keyCode.ESCAPE) {
                    this._escapePressed(event);
                } else if (event.which === jQuery.ui.keyCode.DELETE) {
                    this._deletePressed(event);
                } else if (event.which === jQuery.ui.keyCode.UP) {
                    this._arrowKeyPressed(event, 0, -1);
                } else if (event.which === jQuery.ui.keyCode.RIGHT) {
                    this._arrowKeyPressed(event, 1, 0);
                } else if (event.which === jQuery.ui.keyCode.DOWN) {
                    this._arrowKeyPressed(event, 0, 1);
                } else if (event.which === jQuery.ui.keyCode.LEFT) {
                    this._arrowKeyPressed(event, -1, 0);
                } else if (event.which === 'A'.charCodeAt() && (event.metaKey || event.ctrlKey)) {
                    this._selectAllPressed(event);
                }
            }.bind(this));

            return this;
        },

        /**
         *  Method: _setupNodeOffsetPrintStylesheet
         *    Creates a print stylesheet which is used to compensate the node offsets on the canvas when printing.
         *    Also sets up the CSS template which is used to change the transformation every time the content changes.
         *
         *  Returns:
         *    This Editor instance for chaining.
         */
        _setupNodeOffsetPrintStylesheet: function() {
            // dynamically create a stylesheet, append it to the head and keep the reference to it
            this._nodeOffsetPrintStylesheet = jQuery('<style>')
                .attr('type',  'text/css')
                .attr('media', 'print')
                .appendTo('head');

            // this style will transform all elements on the canvas by the given 'x' and 'y' offset
            var transformCssTemplateText =
                '#' + this.config.IDs.CANVAS + ' > * {\n' +
                '   transform: translate(<%= x %>px,<%= y %>px);\n' +
                '   -ms-transform: translate(<%= x %>px,<%= y %>px); /* IE 9 */\n' +
                '   -webkit-transform: translate(<%= x %>px,<%= y %>px); /* Safari and Chrome */\n' +
                '   -o-transform: translate(<%= x %>px,<%= y %>px); /* Opera */\n' +
                '   -moz-transform: translate(<%= x %>px,<%= y %>px); /* Firefox */\n' +
                '}';
            // store this as a template so we can use it later to manipulate the offset
            this._nodeOffsetStylesheetTemplate = _.template(transformCssTemplateText);

            return this;
        },

        /**
         *  Method: _setupEventCallbacks
         *    Registers all event listeners of the editor.
         *
         *  On:
         *    <Config::Events::NODE_DRAG_STOPPED>
         *    <Config::Events::GRAPH_NODE_ADDED>
         *    <Config::Events::GRAPH_NODE_DELETED>
         *
         *  Returns:
         *    This Editor instance for chaining.
         */
        _setupEventCallbacks: function() {
            // events that trigger a re-calculation of the print offsets
            jQuery(document).on(this.config.Events.NODE_DRAG_STOPPED,  this._updatePrintOffsets.bind(this));
            jQuery(document).on(this.config.Events.GRAPH_NODE_ADDED,   this._updatePrintOffsets.bind(this));
            jQuery(document).on(this.config.Events.GRAPH_NODE_DELETED, this._updatePrintOffsets.bind(this));

            jQuery(document).ajaxStart(Progress.showProgressIndicator);
            jQuery(document).ajaxStop(Progress.hideProgressIndicator);
            jQuery(document).ajaxSuccess(Progress.flashAjaxSuccessMessage);
            jQuery(document).ajaxError(Progress.flashAjaxErrorMessage);

            return this;
        },

        /**
         *  Group: Keyboard Interaction
         */

        /**
         *  Method: _arrowKeyPressed
         *
         *    Event callback for handling presses of arrow keys. Will move the selected nodes in the given direction by
         *    and offset equal to the canvas' grid size. The movement is not done when an input field is currently in
         *    focus.
         *
         *  Parameters:
         *    {jQuery::Event} event      - the issued delete keypress event
         *    {Number}        xDirection - signum of the arrow key's x direction movement (e.g. -1 for left)
         *    {Number}        yDirection - signum of the arrow key's y direction movement (e.g.  1 for down)
         *
         *  Return:
         *    This Editor instance for chaining
         */
        _arrowKeyPressed: function(event, xDirection, yDirection) {
            if (jQuery(event.target).is('input')) return this;

            var selectedNodes = '.' + this.config.Classes.SELECTED + '.' + this.config.Classes.NODE;
            jQuery(selectedNodes).each(function(index, element) {
                var node = jQuery(element).data(this.config.Keys.NODE);
                node.moveBy({
                    x: xDirection * Canvas.gridSize,
                    y: yDirection * Canvas.gridSize
                });
            }.bind(this));

            return this;
        },

        /**
         *  Method: _deletePressed
         *
         *    Event callback for handling delete key presses. Will remove the selected nodes and edges as long as no
         *    input field is currently focused (allows e.g. character removal in properties).
         *
         *  Parameters:
         *    {jQuery::Event} event - the issued delete keypress event
         *
         *  Return:
         *    This Editor instance for chaining
         */
        _deletePressed: function(event) {
            // prevent that node is being deleted when we edit an input field
            if (jQuery(event.target).is('input')) return this;

            var selectedNodes = '.' + this.config.Classes.SELECTED + '.' + this.config.Classes.NODE;
            var selectedEdges = '.' + this.config.Classes.SELECTED + '.' + this.config.Classes.JSPLUMB_CONNECTOR;

            event.preventDefault();
            // delete selected nodes
            jQuery(selectedNodes).each(function(index, element) {
                this.graph.deleteNode(jQuery(element).data(this.config.Keys.NODE).id);
            }.bind(this));

            // delete selected edges
            jQuery(selectedEdges).each(function(index, element) {
                var edge = this.graph.getEdgeById(jQuery(element).attr(this.config.Attributes.CONNECTION_ID));
                jsPlumb.detach(edge);
                this.graph.deleteEdge(edge);
            }.bind(this));

            this.properties.hide();

            return this;
        },

        /**
         *  Method: _escapePressed
         *
         *    Event callback for handling escape key presses. Will deselect any selected nodes and edges.
         *
         *  Parameters:
         *    {jQuery::Event} event - the issued escape keypress event
         *
         *  Returns:
         *    This Editor instance for chaining
         */
        _escapePressed: function(event) {
            event.preventDefault();
            //XXX: deselect everything
            // This uses the jQuery.ui.selectable internal functions.
            // We need to trigger them manually in order to simulate a click on the canvas.
            Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStart(event);
            Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStop(event);

            return this;
        },

        /**
         * Method: _selectAllPressed
         *
         *   Event callback for handling a select all (CTRL/CMD + A) key presses. Will select all nodes and edges.
         *
         * Parameters:
         *   {jQuery::Event} event - the issued select all keypress event
         *
         * Returns:
         *   This Editor instance for chaining.
         */
        _selectAllPressed: function(event) {
            if (jQuery(event.target).is('input')) return this;

            event.preventDefault();

            //XXX: trigger selection start event manually here
            //XXX: hack to emulate a new selection process
            Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStart(event);

            var NODES           = '.' + this.config.Classes.NODE;
            var NODES_AND_EDGES = NODES + ', .' + this.config.Classes.JSPLUMB_CONNECTOR;

            jQuery(NODES_AND_EDGES).each(function(index, domElement) {
                var element = jQuery(domElement);

                element.addClass(this.config.Classes.SELECTING)
                       .addClass(this.config.Classes.SELECTED);
            }.bind(this));

            //XXX: trigger selection stop event manually here
            //XXX: nasty hack to bypass draggable and selectable incompatibility, see also canvas.js
            Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStop(null);

            return this;
        },


        /**
         *  Group: Print Offset Calculation
         */

        /**
         *  Method: _calculateContentOffsets
         *    Calculates the minimal offsets from top and left among all elements displayed on the canvas.
         *
         *  Returns:
         *    An object containing the minimal top ('top') and minimal left ('left') offset to the browser borders.
         */
        _calculateContentOffsets: function() {
            var minLeftOffset = window.Infinity;
            var minTopOffset  = window.Infinity;

            jQuery('.' + this.config.Classes.NODE + ', .' + this.config.Classes.MIRROR).each(function(index, element) {
                var offset = jQuery(element).offset();
                minLeftOffset = Math.min(minLeftOffset, offset.left);
                minTopOffset  = Math.min(minTopOffset,  offset.top);
            });

            return {
                'top':  minTopOffset,
                'left': minLeftOffset
            }
        },

        /**
         *  Method: _updatePrintOffsets
         *    Calculate the minimal offsets of elements on the canvas and updates the print stylesheet so that it will
         *    compensate these offsets while printing (using CSS transforms).
         *    This update is triggered every time a node was added, removed or moved on the canvas.
         */
        _updatePrintOffsets: function(event) {
            var minOffsets = this._calculateContentOffsets();

            if (minOffsets.top  == this._currentMinNodeOffsets.top &&
                minOffsets.left == this._currentMinNodeOffsets.left) {
                    // nothing changed
                    return;
                }

            // replace the style text with the new transformation style
            this._nodeOffsetPrintStylesheet.text(this._nodeOffsetStylesheetTemplate({
                'x': -minOffsets.left + 1, // add a tolerance pixel to avoid cut edges,
                'y': -minOffsets.top + 1
            }));
        }
    });
});
