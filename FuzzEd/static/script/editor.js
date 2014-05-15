define(['class', 'menus', 'canvas', 'backend', 'alerts', 'progress_indicator', 'jquery-classlist', 'jsplumb'],
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
        layout:                        undefined,

        _backend:                      undefined,
        _currentMinNodeOffsets:        {'top': 0, 'left': 0},
        _nodeOffsetPrintStylesheet:    undefined,
        _nodeOffsetStylesheetTemplate: undefined,

        _clipboard:                    '',

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
            this._backend = Backend.establish(graphId);

            // remember certain UI elements
            this._progressIndicator = jQuery('#' + this.config.IDs.PROGRESS_INDICATOR);
            this._progressMessage = jQuery('#' + this.config.IDs.PROGRESS_MESSAGE);

            // run a few sub initializer
            this._setupJsPlumb()
                ._setupNodeOffsetPrintStylesheet()
                ._setupEventCallbacks()
                ._setupMenuActions()
                ._setupDropDownBlur();

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
            this.properties = Menus.PropertiesMenu;
            this.shapes     = Menus.ShapeMenu;
            this.layout     = Menus.LayoutMenu;
            this._backend.activate();
            this.properties.displayOrder(this.graph.getNotation().propertiesDisplayOrder);

            if (readOnly) {
                Alerts.showInfoAlert('Remember:', 'this diagram is read-only');
                this.shapes.disable();
                this.properties.disable();
                Canvas.disableInteraction();
            }

            // enable user interaction
            this._setupMouse()
                ._setupKeyBindings(readOnly);

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
         * Method: _setupDropDownBlur
         *
         * Register an event handler that takes care of closing and blurring all currently open drop down menu items
         * from the toolbar.
         *
         * Returns:
         *   This {<Editor>} instance for chaining.
         */
        _setupDropDownBlur: function () {
            jQuery('#' + this.config.IDs.CANVAS).mousedown(function(event) {
                // close open bootstrap dropdown
                jQuery('.dropdown.open')
                    .removeClass('open')
                    .find('a')
                    .blur();
            });
            
            return this;
        },

        /**
         *  Method: _setupMenuActions
         *
         *  Registers the event handlers for graph type - independent menu entries that trigger JS calls
         *
         *  Returns:
         *    This {<Node>} instance for chaining.
         */
        _setupMenuActions: function() {
            jQuery('#' + this.config.IDs.ACTION_GRID_TOGGLE).click(function() {
                Canvas.toggleGrid();
            }.bind(this));

            jQuery('#' + this.config.IDs.ACTION_CUT).click(function() {
                this._cutSelection();
            }.bind(this));

            jQuery('#' + this.config.IDs.ACTION_COPY).click(function() {
                this._copySelection();
            }.bind(this));

            jQuery('#' + this.config.IDs.ACTION_PASTE).click(function() {
                this._paste();
            }.bind(this));

            jQuery('#' + this.config.IDs.ACTION_DELETE).click(function() {
                this._deleteSelection();
            }.bind(this));

            jQuery('#' + this.config.IDs.ACTION_SELECTALL).click(function(event) {
                this._selectAll(event);
            }.bind(this));

            jQuery('#' + this.config.IDs.ACTION_LAYOUT_CLUSTER).click(function() {
                this.graph._layoutWithAlgorithm(this.graph._getClusterLayoutAlgorithm());
            }.bind(this));

            jQuery('#' + this.config.IDs.ACTION_LAYOUT_TREE).click(function() {
                this.graph._layoutWithAlgorithm(this.graph._getTreeLayoutAlgorithm());
            }.bind(this));

            // set the shortcut hints from 'Ctrl+' to '⌘' when on Mac
            if (navigator.platform == 'MacIntel' || navigator.platform == 'MacPPC') {
                jQuery('#' + this.config.IDs.ACTION_CUT + ' span').text('⌘X');
                jQuery('#' + this.config.IDs.ACTION_COPY + ' span').text('⌘C');
                jQuery('#' + this.config.IDs.ACTION_PASTE + ' span').text('⌘P');
                jQuery('#' + this.config.IDs.ACTION_SELECTALL + ' span').text('⌘A');
            }

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
                    lineWidth:   this.config.JSPlumb.STROKE_WIDTH,
                    outlineColor:this.config.JSPlumb.OUTLINE_COLOR,
                    outlineWidth:this.config.JSPlumb.OUTLINE_WIDTH
                },
                HoverPaintStyle: {
                    strokeStyle: this.config.JSPlumb.STROKE_COLOR_HIGHLIGHTED
                },
                HoverClass:      this.config.Classes.HIGHLIGHTED,
                Connector:       [this.config.JSPlumb.CONNECTOR_STYLE, this.config.JSPlumb.CONNECTOR_OPTIONS],
                ConnectionsDetachable: false,
                ConnectionOverlays: this.config.JSPlumb.CONNECTION_OVERLAYS
            });

            jsPlumb.connectorClass = this.config.Classes.JSPLUMB_CONNECTOR;

            return this;
        },

        /**
         *  Method: _setupMouse
         *    Sets up callbacks that fire when the user interacts with the editor using his mouse. So far this is only
         *    concerns resizing the window.
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _setupMouse: function() {
            jQuery(window).resize(function() {
                var content = jQuery('#' + this.config.IDs.CONTENT);

                Canvas.enlarge({
                    x: content.width(),
                    y: content.height()
                }, true);
            }.bind(this));

            return this;
        },

        /**
         *  Method: _setupKeyBindings
         *    Setup the global key bindings
         *
         *  Keys:
         *    ESCAPE             - Clear selection.
         *    DELETE             - Delete all selected elements (nodes/edges).
         *    UP/RIGHT/DOWN/LEFT - Move the node in the according direction
         *    CTRL/CMD + A       - Select all nodes and edges
         *
         *  Returns:
         *    This editor instance for chaining.
         */
        _setupKeyBindings: function(readOnly) {
            if (readOnly) return this;

            jQuery(document).keydown(function(event) {
                if (event.which == jQuery.ui.keyCode.ESCAPE) {
                    this._escapePressed(event);
                } else if (event.which === jQuery.ui.keyCode.DELETE || event.which === jQuery.ui.keyCode.BACKSPACE) {
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
                } else if (event.which === 'C'.charCodeAt() && (event.metaKey || event.ctrlKey)) {
                    this._copyPressed(event);
                } else if (event.which === 'V'.charCodeAt() && (event.metaKey || event.ctrlKey)) {
                    this._pastePressed(event);
                } else if (event.which === 'X'.charCodeAt() && (event.metaKey || event.ctrlKey)) {
                    this._cutPressed(event);
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
         *    <Config::Events::NODE_ADDED>
         *    <Config::Events::NODE_DELETED>
         *
         *  Returns:
         *    This Editor instance for chaining.
         */
        _setupEventCallbacks: function() {
            // events that trigger a re-calculation of the print offsets
            jQuery(document).on(this.config.Events.NODE_DRAG_STOPPED,  this._updatePrintOffsets.bind(this));
            jQuery(document).on(this.config.Events.NODE_ADDED,         this._updatePrintOffsets.bind(this));
            jQuery(document).on(this.config.Events.NODE_DELETED,       this._updatePrintOffsets.bind(this));

            // show status of global AJAX events in navbar
            jQuery(document).ajaxSend(Progress.showAjaxProgress);
            jQuery(document).ajaxSuccess(Progress.flashAjaxSuccessMessage);
            jQuery(document).ajaxError(Progress.flashAjaxErrorMessage);

            return this;
        },

        /**
         *  Group: Graph Editing
         */

        /**
         *  Method: _deleteSelection
         *
         *    Will remove the selected nodes and edges.
         *
         *  Returns:
         *    This Editor instance for chaining
         */
        _deleteSelection: function() {
            var selectedNodes =      '.' + this.config.Classes.SELECTED + '.' + this.config.Classes.NODE;
            var selectedEdges =      '.' + this.config.Classes.SELECTED + '.' + this.config.Classes.JSPLUMB_CONNECTOR;

            // delete selected nodes
            jQuery(selectedNodes).each(function(index, element) {
                var node = jQuery(element).data(this.config.Keys.NODE);
                this.graph.deleteNode(node);
            }.bind(this));

            // delete selected edges
            jQuery(selectedEdges).each(function(index, element) {
                var edge = jQuery(element).data(this.config.Keys.EDGE);
                this.graph.deleteEdge(edge);
            }.bind(this));

            // delete selected node groups (NASTY!!!)
            var allNodeGroups = '.' + this.config.Classes.NODEGROUP;

            jQuery(allNodeGroups).each(function(index, element) {
                var nodeGroup = jQuery(element).data(this.config.Keys.NODEGROUP);
                if (nodeGroup.container.find("svg path").hasClass(this.config.Classes.SELECTED)) {
                    this.graph.deleteNodeGroup(nodeGroup);
                }
            }.bind(this));

            this.properties.hide();
        },

        /**
         * Method: _selectAll
         *
         *   Will select all nodes and edges.
         *
         * Parameters:
         *   {jQuery::Event} event - the issued select all keypress event
         *
         * Returns:
         *   This Editor instance for chaining.
         */

        _selectAll: function(event) {

            //XXX: trigger selection start event manually here
            //XXX: hack to emulate a new selection process
            Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStart(event);

            jQuery('.'+this.config.Classes.SELECTEE)
                .addClass(this.config.Classes.SELECTING)
                .addClass(this.config.Classes.SELECTED);

            //XXX: trigger selection stop event manually here
            //XXX: nasty hack to bypass draggable and selectable incompatibility, see also canvas.js
            Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStop(null);
        },

        /**
         * Method: _deselectAll
         *
         *   Deselects all the nodes and edges in the current graph.
         *
         * Parameters:
         *   {jQuery::Event} event - (optional) the issued select all keypress event
         *
         * Returns:
         *   This Editor instance for chaining.
         */
        _deselectAll: function(event) {
            if (typeof event === 'undefined') {
                event = window.event;
            }

            //XXX: Since a deselect-click only works without metaKey or ctrlKey pressed,
            // we need to deactivate them manually.
            var hackEvent = jQuery.extend({}, event, {
                metaKey: false,
                ctrlKey: false
            });

            //XXX: deselect everything
            // This uses the jQuery.ui.selectable internal functions.
            // We need to trigger them manually in order to simulate a click on the canvas.
            Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStart(hackEvent);
            Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStop(hackEvent);

            return this;
        },

        /**
         * Method: _copySelection
         *
         *   Will copy selected nodes by serializing and saving them to html5 Local Storage or the _clipboard var using
         *   _updateClipboard().
         *
         * Returns:
         *   This Editor instance for chaining.
         */
        _copySelection: function() {
            var selectedNodes = '.' + this.config.Classes.SELECTED + '.' + this.config.Classes.NODE;
            var selectedEdges = '.' + this.config.Classes.SELECTED + '.' + this.config.Classes.JSPLUMB_CONNECTOR;

            // put nodes as dicts into nodes
            var nodes = [];
            jQuery(selectedNodes).each(function(index, element) {
                var node = this.graph.getNodeById(jQuery(element).data(this.config.Keys.NODE).id);
                if (node.copyable) {
                    nodes.push(node.toDict());
                }
            }.bind(this));

            var edges = [];
            jQuery(selectedEdges).each(function(index, element) {
                var edge = jQuery(element).data(this.config.Keys.EDGE);
                if (edge.copyable) {
                    edges.push(edge.toDict());
                }
            }.bind(this));

            var nodegroups = [];
            // find selected node groups (NASTY!!!)
            var allNodeGroups = '.' + this.config.Classes.NODEGROUP;

            jQuery(allNodeGroups).each(function(index, element) {
                var nodeGroup = jQuery(element).data(this.config.Keys.NODEGROUP);
                // since the selectable element is an svg path, we need to look for that nested element and check its
                //   state of selection via the CSS class .selected
                if (nodeGroup.container.find("svg path").hasClass(this.config.Classes.SELECTED)) {
                    nodegroups.push(nodeGroup.toDict());
                }
            }.bind(this));

            var clipboard = {
                'pasteCount': 0,
                'nodes':      nodes,
                'edges':      edges,
                'nodeGroups': nodegroups
            };

            // forbid copyings without any node
            if (nodes.length > 0) {
                this._updateClipboard(clipboard);
            }
        },

        /**
         * Method: _paste
         *
         *   Will paste previously copied nodes from html5 Local Storage or the _clipboard var by using _getClipboard().
         *
         * Returns:
         *   This Editor instance for chaining.
         */
        _paste: function() {
            // deselect the original nodes and edges
            this._deselectAll();

            // fetch clipboard from local storage or variable and increase pasteCount
            var clipboard = this._getClipboard();
            var pasteCount = ++clipboard.pasteCount;
            this._updateClipboard(clipboard);

            var nodes       = clipboard.nodes;
            var edges       = clipboard.edges;
            var nodeGroups  = clipboard.nodeGroups;
            var ids         = {}; // stores to every old id the newly generated id to connect the nodes again
            var boundingBox = this._boundingBoxForNodes(nodes); // used along with pasteCount to place the copy nicely

            _.each(nodes, function(jsonNode) {
                var pasteId  = this.graph.createId();
                ids[jsonNode.id] = pasteId;
                jsonNode.id = pasteId;
                jsonNode.x += pasteCount * (boundingBox.width + 1);
                jsonNode.y += pasteCount * (boundingBox.height + 1);

                var node = this.graph.addNode(jsonNode);
                if (node) node.select();
            }.bind(this));

            _.each(edges, function(jsonEdge) {
                jsonEdge.id = undefined;
                jsonEdge.source = ids[jsonEdge.sourceNodeId] || jsonEdge.sourceNodeId;
                jsonEdge.target = ids[jsonEdge.targetNodeId] || jsonEdge.targetNodeId;

                var edge = this.graph.addEdge(jsonEdge);
                if (edge) edge.select();
            }.bind(this));

            _.each(nodeGroups, function(jsonNodeGroup) {
                // remove the original nodeGroup's identity
                jsonNodeGroup.id = undefined;
                // map old ids to new ids
                jsonNodeGroup.nodeIds = _.map(jsonNodeGroup.nodeIds, function(nodeId) {
                    return ids[nodeId] || nodeId;
                });

                var nodeGroup = this.graph.addNodeGroup(jsonNodeGroup);
                if (nodeGroup) nodeGroup.select();
            }.bind(this));

            //XXX: trigger selection stop event manually here
            //XXX: nasty hack to bypass draggable and selectable incompatibility, see also canvas.js
            Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStop(null);
        },

        /**
         * Method: _cutSelection
         *
         *   Will delete and copy selected nodes by using _updateClipboard().
         *
         * Returns:
         *   This Editor instance for chaining.
         */
        _cutSelection: function() {
            this._copySelection();
            this._deleteSelection();

            // set the just copied clipboard's pasteCount to -1, so that it will paste right in place of the original.
            var clipboard = this._getClipboard();
            --clipboard['pasteCount'];
            this._updateClipboard(clipboard);
        },

        /**
         * Method: _boundingBoxForNodes
         *
         *   Returns the (smallest) bounding box for the given nodes by accessing their x and y coordinates and finding
         *   mins and maxes. Used by _paste() to place the copy nicely.
         *
         * Returns:
         *   A dictionary containing 'width' and 'height' of the calculated bounding box.
         */

        _boundingBoxForNodes: function(nodes) {
            var topMostNode     = { 'y': Number.MAX_VALUE };
            var leftMostNode    = { 'x': Number.MAX_VALUE };
            var bottomMostNode  = { 'y': 0 };
            var rightMostNode   = { 'x': 0 };

            _.each(nodes, function(node) {
                if (node.y < topMostNode.y)    { topMostNode    = node }
                if (node.x < leftMostNode.x)   { leftMostNode   = node; }
                if (node.y > bottomMostNode.y) { bottomMostNode = node; }
                if (node.x > rightMostNode.x)  { rightMostNode  = node; }
            }.bind(this));

            return {
                'width':  rightMostNode.x - leftMostNode.x,
                'height': bottomMostNode.y - topMostNode.y
            }
        },


        /**
         *  Group: Clipboard Handling
         */

        /**
         * Method: _updateClipboard
         *
         *   Saves the given clipboardDict either to html5 Local Storage or at least to the Graph's _clipboard var as
         *   JSON string.
         *
         * Parameters:
         *   {JSON} clipboardDict - JSON dict to be stored
         *
         * Returns:
         *   This Editor instance for chaining.
         */
        _updateClipboard: function(clipboardDict) {
            var clipboardString = JSON.stringify(clipboardDict);
            if (typeof window.Storage !== 'undefined') {
                localStorage['clipboard_' + this.graph.kind] = clipboardString;
            } else { // fallback
                this._clipboard = clipboardString;
            }

            return this;
        },

        /**
         * Method: _getClipboard
         *
         *   Returns the current clipboard either from html5 Local Storage or from the Graph's _clipboard var as JSON.
         *
         * Returns:
         *   The clipboard contents as JSON object.
         */
        _getClipboard: function() {
            if (typeof window.Storage !== 'undefined' && localStorage['clipboard_' + this.graph.kind] !== 'undefined') {
                return JSON.parse(localStorage['clipboard_' + this.graph.kind]);
            } else {
                return JSON.parse(this._clipboard);
            }
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
            if (jQuery(event.target).is('input, textarea')) return this;

            var selectedNodes = '.' + this.config.Classes.SELECTED + '.' + this.config.Classes.NODE;
            jQuery(selectedNodes).each(function(index, element) {
                var node = jQuery(element).data(this.config.Keys.NODE);
                node.moveBy({
                    x: xDirection * Canvas.gridSize,
                    y: yDirection * Canvas.gridSize
                });
            }.bind(this));

            jQuery(document).trigger(this.config.Events.NODES_MOVED);

            return this;
        },

        /**
         *  Method: _deletePressed
         *
         *    Event callback for handling delete key presses. Will remove the selected nodes and edges by calling
         *    _deleteSelection as long as no input field is currently focused (allows e.g. character removal in
         *    properties).
         *
         *  Parameters:
         *    {jQuery::Event} event - the issued delete keypress event
         *
         *  Return:
         *    This Editor instance for chaining
         */
        _deletePressed: function(event) {
            // prevent that node is being deleted when we edit an input field
            if (jQuery(event.target).is('input, textarea')) return this;
            event.preventDefault();
            this._deleteSelection();
            return this;
        },

        /**
         *  Method: _escapePressed
         *
         *    Event callback for handling escape key presses. Will deselect any selected nodes and edges by calling
         *    _deselectAll().
         *
         *  Parameters:
         *    {jQuery::Event} event - the issued escape keypress event
         *
         *  Returns:
         *    This Editor instance for chaining
         */
        _escapePressed: function(event) {
            event.preventDefault();
            this._deselectAll(event);
            return this;
        },

        /**
         * Method: _selectAllPressed
         *
         *   Event callback for handling a select all (CTRL/CMD + A) key presses. Will select all nodes and edges by
         *   calling _selectAll().
         *
         * Parameters:
         *   {jQuery::Event} event - the issued select all keypress event
         *
         * Returns:
         *   This Editor instance for chaining.
         */
        _selectAllPressed: function(event) {
            if (jQuery(event.target).is('input, textarea')) return this;
            event.preventDefault();
            this._selectAll(event);
            return this;
        },

        /**
         * Method: _copyPressed
         *
         *   Event callback for handling a copy (CTRL/CMD + C) key press. Will copy selected nodes by serializing and
         *   saving them to html5 Local Storage or the _clipboard var by calling _copySelection().
         *
         * Parameters:
         *   {jQuery::Event} event - the issued select all keypress event
         *
         * Returns:
         *   This Editor instance for chaining.
         */
        _copyPressed: function(event) {
            if (jQuery(event.target).is('input, textarea')) return this;
            event.preventDefault();
            this._copySelection();
            return this;
        },

        /**
         * Method: _pastePressed
         *
         *   Event callback for handling a paste (CTRL/CMD + V) key press. Will paste previously copied nodes from
         *   html5 Local Storage or the _clipboard var by calling _paste().
         *
         * Parameters:
         *   {jQuery::Event} event - the issued select all keypress event
         *
         * Returns:
         *   This Editor instance for chaining.
         */
        _pastePressed: function(event) {
            if (jQuery(event.target).is('input, textarea')) return this;
            event.preventDefault();
            this._paste();
            return this;
        },

        /**
         * Method: _cutPressed
         *
         *   Event callback for handling a cut (CTRL/CMD + X) key press. Will delete and copy selected nodes by calling
         *   _cutSelection().
         *
         * Parameters:
         *   {jQuery::Event} event - the issued select all keypress event
         *
         * Returns:
         *   This Editor instance for chaining.
         */
        _cutPressed: function(event) {
            if (jQuery(event.target).is('input, textarea')) return this;
            event.preventDefault();
            this._cutSelection();
            return this;
        },

        /**
         *  Group: Progress Indication
         */

        /**
         *  Method _showProgressIndicator
         *    Display the progress indicator.
         *
         *  Returns:
         *    This Editor instance for chaining.
         */
        _showProgressIndicator: function() {
            // show indicator only if it takes longer then 500 ms
            this._progressIndicatorTimeout = setTimeout(function() {
                jQuery('#' + this.config.IDs.PROGRESS_INDICATOR).show();
            }.bind(this), 500);

            return this;
        },

        /**
         *  Method _hideProgressIndicator
         *    Hides the progress indicator.
         *
         *  Returns:
         *    This Editor instance for chaining.
         */
        _hideProgressIndicator: function() {
            // prevent indicator from showing before 500 ms are passed
            clearTimeout(this._progressIndicatorTimeout);
            jQuery('#' + this.config.IDs.PROGRESS_INDICATOR).hide();

            return this;
        },

        /**
         *  Method: _flashSaveIndicator
         *    Flash the save indicator to show that the current graph is saved in the backend.
         *
         *  Returns:
         *    This Editor instance for chaining.
         */
        _flashSaveIndicator: function() {
            var indicator = jQuery('#' + this.config.IDs.SAVE_INDICATOR);
            // only flash if not already visible
            if (indicator.is(':hidden')) {
                indicator.fadeIn(200).delay(600).fadeOut(200);
            }

            return this;
        },

        /**
         *  Method _flashErrorIndicator
         *    Flash the error indicator to show that the current graph has not been saved to the backend.
         *
         *  Returns:
         *    This Editor instance for chaining.
         */
        _flashErrorIndicator: function() {
            var indicator = jQuery('#' + this.config.IDs.ERROR_INDICATOR);
            // only flash if not already visible
            if (indicator.is(':hidden')) {
                indicator.fadeIn(200).delay(5000).fadeOut(200);
            }

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
