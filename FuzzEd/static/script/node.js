define(['properties', 'mirror', 'canvas', 'class', 'jsplumb', 'jquery.svg'],
function(Properties, Mirror, Canvas, Class) {
    /**
     *  Class: {Abstract} Node
     *
     *  This class models the abstract base class for all nodes. It provides basic functionality for CRUD operations,
     *  setting up visual representation, dragging, selection, <Mirrors>, <Properties> and defines basic connection
     *  rules. Other classes, like e.g. <Editor> and <Graph>, rely on the interface provided by this class. It is
     *  therefore strongly recommended to inherit from <Node> and to add custom behaviour. Any non abstract subclass
     *  MUST implement <Node::getConfig()>.
     *
     */
    return Class.extend({
        /**
         *  Group: Members
         *
         *  Properties:
         *    {Object}     config              - An object containing node configuration constants. If not set otherwise,
         *                                       defaults to <Node::getConfig()>.
         *    {DOMElement} container           - The DOM element that contains all other visual DOM elements of the node
         *                                       such as its image, mirrors, ...
         *    {int}        id                  - A client-side generated id - i.e. UNIX-timestamp - to uniquely identify
         *                                       the node in the frontend. It does NOT correlate with database ids in the
         *                                       backend. Introduced to save round-trips and to later allow for an
         *                                       offline mode.
         *    {Array[<Edge>]} incomingEdges    - An enumeration of all edges linking TO this node (this node is the target
         *                                       target of the edge).
         *    {Array[<Edge>]} outgoingEdges    - An enumeration of all edges linking FROM this node (this node is the
         *                                       source of the edge).
         *    {bool}       _disabled           - Boolean flag indicating whether this node may be a target for a
         *                                       currently drawn edge. True disables connection and therefore fades out
         *                                       the node.
         *    {bool}       _highlighted        - Boolean flag that is true when the node needs to be highlighted on hover.
         *    {bool}       _selected           - Boolean flag that is true when the node is selected - i.e. clicked.
         *    {DOMElement} _nodeImage          - DOM element that contains the actual image/svg of the node.
         *    {DOMElement} _nodeImageContainer - A wrapper for the node image which is necessary to get position
         *                                       calculation working in Firefox.
         *    {DOMElement} _connectionHandle   - DOM element containing the visual representation of the handle where one
         *                                       can pull out new edges.
         */
        config:        undefined,
        container:     undefined,
        id:            undefined,
        incomingEdges: undefined,
        outgoingEdges: undefined,

        _disabled:           false,
        _highlighted:        false,
        _selected:           false,
        _nodeImage:          undefined,
        _nodeImageContainer: undefined,
        _connectionHandle:   undefined,

        /**
         * Group: Initialization
         */

        /**
         * Constructor: init
         *
         * The constructor of the abstract node class. It will merge the state of the properties, assign a client-side
         * id, setup the visual representation and enable interaction via mouse and keyboard. Calling the constructor
         * as-is, will result in an exception.
         *
         * Parameters:
         *   {Object}     properties             - An object containing default values for the node's properties. E.g.:
         *                                         {x: 1, y: 20, name: 'foo'}. The values will be merged into the node
         *                                         recursively, creating deep copies of complex structures like arrays
         *                                         or other objects. Mainly required for restoring the state of a node
         *                                         when loading a graph from the backend.
         *   {Array[str]} propertiesDisplayOrder - An enumeration of property names, sorted by the order in which the
         *                                         property with the respective name shall appear in the property menu.
         *                                         May contain names of properties that the node does not have.
         *
         * Returns:
         *   This {<Node>} instance.
         */
        init: function(properties, propertiesDisplayOrder) {
            // merge all presets of the configuration and data from the backend into this object
            jQuery.extend(true, this, properties);

            // logic
            if (typeof this.id === 'undefined') {
                // make sure the 0 is not reassigned; it's reserved for the top event
                this.id = new Date().getTime() + 1;
            }
            this.config = this.getConfig();

            this.incomingEdges = [];
            this.outgoingEdges = [];

            // visuals
            jsPlumb.extend(this.connector, jsPlumb.Defaults.PaintStyle);

            this._setupVisualRepresentation()
                // Additional visual operations - cannot go to _setupVisualRepresentation since they require the
                // container to be already in the DOM/
                ._setupNodeImage()
                ._moveContainerToPixel(Canvas.toPixel(this.x, this.y))
                ._setupConnectionHandle()
                ._setupEndpoints()
                // Interaction
                ._setupDragging()
                ._setupMouse()
                ._setupSelection()
                // Property displays
                ._setupMirrors(this.propertyMirrors, propertiesDisplayOrder)
                ._setupPropertyMenuEntries(this.propertyMenuEntries, propertiesDisplayOrder);
        },

        /**
         * Method: _setupVisualRepresentation
         *
         * This method is used in the constructor to set up the visual representation of the node from its kind string.
         * First, the node's image is created by cloning the corresponding thumbnail from the shape menu and formatting
         * it. Then, it is appended to a freshly created div element becoming the node's <Node::container> element.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _setupVisualRepresentation: function() {
            // get the thumbnail, clone it and wrap it with a container (for labels)
            this._nodeImage = jQuery('#' + this.config.IDs.SHAPES_MENU + ' #' + this.kind)
                .clone()
                // cleanup the thumbnail's specific properties
                .removeClass('ui-draggable')
                .removeAttr('id')
                // add new classes for the actual node
                .addClass(this.config.Classes.NODE_IMAGE);

            this._nodeImageContainer = jQuery('<div>')
                .append(this._nodeImage);

            this.container = jQuery('<div>')
                .attr('id', this.kind + this.id)
                .addClass(this.config.Classes.NODE)
                .css('position', 'absolute')
                .data(this.config.Keys.NODE, this)
                .append(this._nodeImageContainer);

            this.container.appendTo(Canvas.container);

            return this;
        },

        /**
         * Method: _setupNodeImage
         *
         * Helper method used in the constructor to setup the actual image of the node. First off it scales the cloned
         * thumbnail of the node from the shape menu up to the grid size (requires a number SVG of transformations on
         * all groups) and sets the according image margins to snap to the grid. After that the <Node::_nodeImage>
         * member is enriched with additional convenience values (primitives, groups, xCenter, yCenter) to allow faster
         * processing in other methods.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _setupNodeImage: function() {
            // links to primitive shapes and groups of the SVG for later manipulation (highlighting, ...)
            this._nodeImage.primitives = this._nodeImage.find('rect, circle, path');
            this._nodeImage.groups     = this._nodeImage.find('g');

            // calculate the scale factor
            var marginOffset = this._nodeImage.outerWidth(true) - this._nodeImage.width();
            var scaleFactor  = (Canvas.gridSize - marginOffset) / this._nodeImage.height();

            // resize the svg and the groups
            this._nodeImage.attr('width',  this._nodeImage.width()  * scaleFactor);
            this._nodeImage.attr('height', this._nodeImage.height() * scaleFactor);

            var newTransform = 'scale(' + scaleFactor + ')';
            if (this._nodeImage.groups.attr('transform')) {
                newTransform += ' ' + this._nodeImage.groups.attr('transform');
            }
            this._nodeImage.groups.attr('transform', newTransform);

            // XXX: In Webkit browsers the container div does not resize properly. This should fix it.
            this.container.width(this._nodeImage.width());

            // cache center of the image
            // XXX: We need to use the node image's container's position because Firefox fails otherwise
            this._nodeImage.xCenter = this._nodeImageContainer.position().left + this._nodeImage.outerWidth(true)  / 2;
            this._nodeImage.yCenter = this._nodeImageContainer.position().top  + this._nodeImage.outerHeight(true) / 2;

            return this;
        },

        /**
         * Method: _setupConnectionHandle
         *
         * This initialization method is called in the constructor to setup the connection handles of the node. These
         * are the small plus icons where one can drag edges out of. In the default implementation connectors are
         * located at the bottom of the image centered.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _setupConnectionHandle: function() {
            if (this.numberOfOutgoingConnections != 0) {
                this._connectionHandle = jQuery('<i class="icon-plus icon-white"></i>')
                    .addClass(this.config.Classes.NODE_HALO_CONNECT + ' ' + this.config.Classes.NO_PRINT)
                    .css({
                        'top':  this._nodeImage.yCenter + this._nodeImage.outerHeight(true) / 2,
                        'left': this._nodeImage.xCenter
                    })
                    .appendTo(this.container);
            }

            return this;
        },

        /**
         * Method: _setupEndpoints
         *
         * This initialization method does the setup work for endpoints. Endpoints are virtual entities that function as
         * source as well as target of edges dragged from/to them. They define how many edges and coming from which
         * node type may be connected to this node. This method serves as a dispatcher to the sub-methods
         * <Node::_setupIncomingEndpoint> and <Node::_setupOutoingEndpoint>.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _setupEndpoints: function() {
            var anchors = this._connectorAnchors();
            var offset  = this._connectorOffset();

            this._setupIncomingEndpoint(anchors.in,  offset.in)
                ._setupOutgoingEndpoint(anchors.out, offset.out);

            return this;
        },

        /**
         * Method: _setupIncomingEndpoint
         *
         * This method sets up the endpoint for incoming connections - i.e. the target - for a node. Therefore it uses
         * the jsPlumb makeTarget function on the node's container. Nodes that disallow incoming connection do NOT have
         * any endpoint target.
         *
         * Parameters:
         *   {Array[int]} anchors          - jsPlumb four tuple anchor definition as return by <Node::connectorAnchors>.
         *   {Object}     connectionOffset - Precise pixel offset of the endpoint in relation to the relative anchor
         *                                   position of the anchor parameter. See also <Node::connectorOffset>
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _setupIncomingEndpoint: function(anchors, connectionOffset) {
            if (this.numberOfIncomingConnections === 0) return this;

            jsPlumb.makeTarget(this.container, {
                // position of the anchor
                anchor:         anchors.concat([connectionOffset.x, connectionOffset.y]),
                maxConnections: this.numberOfIncomingConnections,
                dropOptions: {
                    // Define which node can connect to the target...
                    accept: function(draggable) {
                        var elid = draggable.attr('elid');
                        // ...DOM elements without elid (generated by jsPlumb) are disallowed...
                        if (typeof elid === 'undefined') return false;

                        // ...as well as nodes without a node object representing it.
                        var sourceNode = jQuery('.' + this.config.Classes.NODE + ':has(#' + elid + ')').data('node');
                        if (typeof sourceNode === 'undefined') return false;

                        // Ask the source node if it can connect to us.
                        return sourceNode.allowsConnectionsTo(this);
                    }.bind(this),
                    activeClass: this.config.Classes.NODE_DROP_ACTIVE
                }
            });

            return this;
        },

        /**
         * Method: _setupOutgoingEndpoint
         *
         * This initialization method sets up the endpoint for outgoing connections - i.e. the source - for edges of
         * this node. The source is in contrary of a target not the whole node, but only the connection handle of the
         * node (see: <Node::_setupConnectionHandle>). The functionality is provided by the jsPlumb makeSource call.
         * Nodes that do no allow for outgoing connections do NOT have any source endpoint. In this method you will
         * also find the callbacks that are responsible for fading out target nodes that do not allow connection from
         * this node.
         *
         * Parameters:
         *   {Array[int]} anchors          - jsPlumb four tuple anchor definition as return by <Node::connectorAnchors>.
         *   {Object}     connectionOffset - Precise pixel offset of the endpoint in relation to the relative anchor
         *                                   position of the anchor parameter. See also <Node::connectorOffset>
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _setupOutgoingEndpoint: function(anchors, connectionOffset) {
            if (this.numberOfOutgoingConnections == 0) return this;

            // small flag for the drag callback, explanation below
            var highlight     = true;
            var inactiveNodes = '.' + this.config.Classes.NODE + ':not(.'+ this.config.Classes.NODE_DROP_ACTIVE + ')';

            jsPlumb.makeSource(this._connectionHandle, {
                parent:         this.container,
                anchor:         anchors.concat([connectionOffset.x, connectionOffset.y]),
                maxConnections: this.numberOfOutgoingConnections,
                connectorStyle: this.connector,
                dragOptions: {
                    cursor: this.config.Dragging.CURSOR_EDGE,
                    // XXX: have to use drag callback here instead of start
                    // The activeClass assigned in <Node::_setupIncomingEndpoint> is unfortunately assigned only AFTER
                    // the execution of the start callback by jsPlumb.
                    drag: function() {
                        // using the highlight flag here to simulate only-once-behaviour (no re-computation of node set)
                        if (!highlight) return;
                        // disable all nodes that can not be targeted
                        jQuery(inactiveNodes).each(function(index, node){
                            jQuery(node).data(this.config.Keys.NODE).disable();
                        }.bind(this));
                        highlight = false;
                    }.bind(this),
                    stop: function() {
                        // re-enable disabled nodes
                        jQuery(inactiveNodes).each(function(index, node){
                            jQuery(node).data(this.config.Keys.NODE).enable();
                        }.bind(this));
                        // release the flag, to allow fading out nodes again
                        highlight = true;
                    }.bind(this)
                }
            });

            return this;
        },

        /**
         * Method: _setupDragging
         *
         * This initialization method is called in the constructor and is responsible for setting up the node's dragging
         * functionality. A user is not able to position nodes freely but can only let nodes snap to grid, simulating
         * checkered graph paper. The functionality below is multi select aware, meaning a user can drag multiple node
         * at once.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _setupDragging: function() {
            var initialPositions = {};

            // using jsPlumb draggable and not jQueryUI to allow that edges move together with nodes
            jsPlumb.draggable(this.container, {
                // stay in the canvas
                containment: 'parent',
                // become a little bit opaque when dragged
                opacity:     this.config.Dragging.OPACITY,
                // show a cursor with four arrows
                cursor:      this.config.Dragging.CURSOR,
                // stick to the checkered paper
                grid:        [Canvas.gridSize, Canvas.gridSize],
                // when dragged a node is send to front, overlaying other nodes and edges
                stack:       '.' + this.config.Classes.NODE + ', .' + this.config.Classes.JSPLUMB_CONNECTOR,

                // start dragging callback
                start: function(event) {
                    // XXX: add dragged node to selection
                    // This uses the jQuery.ui.selectable internal functions.
                    // We need to trigger them manually because jQuery.ui.draggable doesn't propagate these events.
                    if (!this.container.hasClass(this.config.Classes.JQUERY_UI_SELECTED)) {
                        Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStart(event);
                        Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStop(event);
                    }

                    // capture the original positions of all (multi) selected nodes and save them
                    jQuery('.' + this.config.Classes.JQUERY_UI_SELECTED).each(function(index, node) {
                        var nodeInstance = jQuery(node).data(this.config.Keys.NODE);
                        initialPositions[nodeInstance.id] = nodeInstance.container.position();
                    }.bind(this));
                }.bind(this),

                drag: function(event, ui) {
                    // determine by how many pixels we moved from our original position (see: start callback)
                    var xOffset = ui.position.left - initialPositions[this.id].left;
                    var yOffset = ui.position.top  - initialPositions[this.id].top;

                    // tell all selected nodes to move as well, except this node; the user already dragged it
                    jQuery('.' + this.config.Classes.JQUERY_UI_SELECTED).not(this.container).each(function(index, node) {
                        var nodeInstance = jQuery(node).data(this.config.Keys.NODE);

                        // move the other selectee by the dragging offset, do NOT report to the backend yet
                        nodeInstance._moveContainerToPixel({
                            'x': initialPositions[nodeInstance.id].left + xOffset + nodeInstance._nodeImage.xCenter,
                            'y': initialPositions[nodeInstance.id].top  + yOffset + nodeInstance._nodeImage.yCenter
                        });

                        // ask jsPlumb to repaint the selectee in order to redraw its connections
                        jsPlumb.repaint(nodeInstance.container);
                    }.bind(this));
                }.bind(this),

                // stop dragging callback
                stop: function(event, ui) {
                    // ... calculate the final amount of pixels we moved...
                    var xOffset = ui.position.left - initialPositions[this.id].left;
                    var yOffset = ui.position.top  - initialPositions[this.id].top;

                    jQuery('.' + this.config.Classes.JQUERY_UI_SELECTED).each(function(index, node) {
                        var nodeInstance = jQuery(node).data(this.config.Keys.NODE);

                        // ... and report to the backend this time because dragging ended
                        nodeInstance.moveTo({
                            'x': initialPositions[nodeInstance.id].left + xOffset + nodeInstance._nodeImage.xCenter,
                            'y': initialPositions[nodeInstance.id].top  + yOffset + nodeInstance._nodeImage.yCenter
                        });
                    }.bind(this));

                    // forget the initial position of the nodes to allow new dragging
                    initialPositions = {};

                    jQuery(document).trigger(this.config.Events.NODE_DRAG_STOPPED);
                }.bind(this)
            });

            return this;
        },

        /**
         * Method: _setupMouse
         *
         * Small helper method used in the constructor for setting up mouse hover highlighting (highlight on hover,
         * unhighlight on mouse out).
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _setupMouse: function() {
            // hovering over a node
            this.container.hover(
                // mouse in
                this.highlight.bind(this),
                // mouse out
                this.unhighlight.bind(this)
            );

            return this;
        },

        /**
         * Method: _setupSelection
         *
         * This initialization method is called in the constructor and sets up multi-select functionality for nodes.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _setupSelection: function() {
            //XXX: select a node on click
            // This uses the jQuery.ui.selectable internal functions.
            // We need to trigger them manually because only jQuery.ui.draggable gets the mouseDown events on nodes.
            this.container.click(function(event) {
                Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStart(event);
                Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStop(event);
            }.bind(this));

            return this;
        },

        /**
         * Method: _setupMirrors
         *
         * This helper method is called in the constructor and creates <Mirrors> for the node. Mirrors are create if
         * and only if they appear in the propertyDisplayOrder collection.
         *
         * Parameters:
         *   {Object}     propertyMirrors      - The mirror definition objects as found in notations file
         *                                       (e.g. notations/faulttree.json)
         *   {Array[str]} propertyDisplayOrder - An array of property name string in the order descending order of their
         *                                       appearance as mirrors.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _setupMirrors: function(propertyMirrors, propertiesDisplayOrder) {
            this.propertyMirrors = {};
            if (typeof propertyMirrors === 'undefined') return this;

            _.each(propertiesDisplayOrder, function(property) {
                var mirrorDefinition = propertyMirrors[property];

                if (typeof mirrorDefinition === 'undefined' || mirrorDefinition === null) return;
                this.propertyMirrors[property] = new Mirror(this.container, mirrorDefinition);
            }.bind(this));

            return this;
        },

        /**
         * Method: _setuPropertyMenuEntries
         *
         * Parameters:
         *   {Object}     propertyMenuEntries    - An object containing
         *   {Array[str]} propertiesDisplayOrder - bar.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _setupPropertyMenuEntries: function(propertyMenuEntries, propertiesDisplayOrder) {
            this.propertyMenuEntries = {};
            if (typeof propertyMenuEntries === 'undefined') return this.propertyMenuEntries;

            _.each(propertiesDisplayOrder, function(property) {
                var menuEntry = propertyMenuEntries[property];
                if (typeof menuEntry === 'undefined' || menuEntry === null) return;

                var mirror = this.propertyMirrors[property];

                menuEntry.property = property;
                this.propertyMenuEntries[property] = Properties.newFrom(this, mirror, menuEntry);
            }.bind(this));

            return this;
        },

        /**
         * Group: Configuration
         */

        /**
         * Method: _connectorAnchors
         *
         * This method returns the position of the anchors for the connectors. The format is taken from jsPlumb and is
         * defined as a four-tuple: [x, y, edge_x, edge_y]. The values for x and y define the relative offset of the
         * connector from the left upper corner of the container. Edge_x and edgy_y determine the direction connected
         * edges point from the connector.
         *
         * Returns:
         *   {Object} with 'in' and 'out' keys containing jsPlumb four-tuple connector definitions.
         */
        _connectorAnchors: function() {
            return {
                'in':  [0.5, 0, 0, -1],
                'out': [0.5, 0, 0,  1]
            }
        },

        /**
         * Method: _connectorOffset
         *
         * This method returns an object with additional precise pixel offsets for the connectors as defined in
         * <Node::_connectorAnchors>.
         *
         * Returns:
         *   {Object} with 'in' and 'out' keys containing {Objects} with pixel offsets of the connectors.
         */
        _connectorOffset: function() {
            var topOffset = this._nodeImage.offset().top - this.container.offset().top;
            var bottomOffset = topOffset + this._nodeImage.height() + this.connector.offset.bottom;

            return {
                'in': {
                    'x': 0,
                    'y': topOffset
                },
                'out': {
                    'x': 0,
                    'y': bottomOffset
                }
            }
        },

        /**
         * Group: Logic
         */

        /**
         * Method: allowsConnectionTo
         *
         * This method checks if it is allowed to draw an object between this node (source) and the other node passed
         * as parameter (target). Connections are allowed if and only if, the node does not connect to itself, the
         * outgoing connections of this node, respectively the incoming connections of the other node are not exceeded
         * and the notation file allows a connection between these two nodes.
         *
         * Parameters:
         *   {<Node>} otherNode - the node instance to connect to
         *
         * Returns:
         *   {true} if the connection is allowed, {false} otherwise
         */
        allowsConnectionsTo: function(otherNode) {
            // no connections to same node
            if (this == otherNode) return false;

            // otherNode must be in the 'allowConnectionTo' list defined in the notations
            var allowed = _.any(this.allowConnectionTo, function(nodeClass) {
                return otherNode instanceof nodeClass;
            });
            if (!allowed) return false;

            // there is already a connection between these nodes
            var connections = jsPlumb.getConnections({
                //TODO: the selector should suffice, but due to a bug in jsPlumb we need the IDs here
                //TODO: maybe that is fixed in a newer version of jsPlumb
                source: this.container.attr('id'),
                target: otherNode.container.attr('id')
            });
            if (connections.length != 0) return false;

            // no connection if endpoint is full
            var endpoints = jsPlumb.getEndpoints(otherNode.container);
            if (endpoints) {
                //TODO: find a better way to determine endpoint
                var targetEndpoint = _.find(endpoints, function(endpoint){
                    return endpoint.isTarget || endpoint._makeTargetCreator
                });
                if (targetEndpoint && targetEndpoint.isFull()) return false;
            }

            return true;
        },

        /**
         * Method: getConfig
         *
         * This method is abstract. All non abstract subclasses MUST override this method. It is an error to call this
         * function otherwise. The expected return value of this function is an Object containing at least all key-value
         * pairs as defined in <Config> (return it when in doubt). This Object is used for the initialization of node
         * instances and contains static values such as e.g. colors, pixel values, CSS class names, ... that are shared
         * with other classes like <Editor> or <Graph>. Ensure that all notation specific subclasses use the very same
         * reference to a config object.
         *
         * NOTE: Wondering about the reason for this seemingly overly complex config access mechanism? Rest assured we
         * understand you. An attempt for explanation. When using JavaScript "classes" and AMD closures you run quickly
         * into scoping issues when also trying to facilitate inheritance. An Example: Imagine you would like to
         * subclass this class <Node> by another class called Derivative. In Derivative you would like to change some
         * very basic config options. These options shall already be taken into account when executing the abstract base
         * constructor. However, since you required the config already in the base class in form of an AMD closure,
         * there is no way you could possibly obtain the reference to the config in Derived without requiring it again
         * and trying to overwrite presumably constant values. An all that, before the base class can even possibly
         * reads from the config, due to asynchronous AMD requests... For this reason, we use this work-around. By
         * requiring the most specific subclass to return the "most up-to-date" config, which that in turn can be easily
         * accessed by the base class.
         *
         * Throws:
         *   [ABSTRACT] Subclass Responsibility
         */
        getConfig: function() {
            throw '[ABSTRACT] Subclass Responsibility';
        },

        /**
         * Group: DOM Manipulation
         */

        /**
         * Method: moveTo
         *   Moves the node's visual representation to the given coordinates and reports to backend. The center of the
         *   node's image is the anchor point for the translation.
         *
         * Parameters:
         *   {Object} position      - Object in the form of {x: ..., y: ...} containing the pixel coordinates to move
         *                            the node to.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         *
         * Triggers:
         *   <Config::Events::NODE_PROPERTY_CHANGED>
         */
        moveTo: function(position) {
            var gridPos = Canvas.toGrid(position);
            this.x = gridPos.x;
            this.y = gridPos.y;

            this._moveContainerToPixel(position);
            // call home
            jQuery(document).trigger(this.config.Events.NODE_PROPERTY_CHANGED, [this.id, {'x': this.x, 'y': this.y}]);

            return this;
        },

        /**
         * Method: remove
         *
         * Removes the whole visual representation including endpoints from the canvas.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        remove: function() {
            _.each(jsPlumb.getEndpoints(this.container), function(endpoint) {
                jsPlumb.deleteEndpoint(endpoint);
            });
            this.container.remove();

            return this;
        },

        /**
         * Method: _moveContainerToPixel
         *
         * Moves the node's <Node::container> to the pixel position specified in the position parameter. Does not take
         * <Canvas> offset or the grid into account. The node's image center is the anchor point for the translation.
         *
         * Parameters:
         *   {Object} position - Object of the form {x: ..., y: ...}, where x and y point to integer pixel values where
         *                       the node's container shall be moved to
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _moveContainerToPixel: function(position) {
            this.container.css({
                left: position.x - this._nodeImage.xCenter,
                top:  position.y - this._nodeImage.yCenter
            });

            return this;
        },

        /**
         * Group: Highlighting
         */

        /**
         * Method: disable
         *
         * Disables the node visually (fade out) to make it appear to be not interactive for the user. Sets the node's
         * <Node::_disabled> flag to true.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        disable: function() {
            this._disabled = true;
            return this._visualDisable();
        },

        /**
         * Method: enable
         *
         * This method node re-enables the node visually and makes appear interactive to the user. Should usually be
         * called subsequently to <Node::disabled()>. Modifies the node's <Node::_disabled> flag to false. The method
         * takes other visual states like highlighted and selected into account.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        enable: function() {
            this._disabled = false;

            if (this._selected) {
                return this._visualSelect();
            } else if (this._highlighted) {
                return this._visualHighlight();
            } else {
                return this._visualReset();
            }
        },

        /**
         * Method: select
         *
         * Marks the node as selected - meaning: it will set the <Node::_selected> member to true and change the node's
         * visual appearance (<Node::_visualSelect()>). A node can only be selected if it is not already disabled.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        select: function() {
            // don't allow selection of disabled nodes
            if (this._disabled) return this;

            this._selected = true;
            return this._visualSelect();
        },

        /**
         * Method: deselect
         *
         * This method deselects the node - meaning: sets the <Node::_selected> flag to false and reset it visual
         * appearance as long is it not also selected.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        deselect: function() {
            this._selected = false;

            if (this._highlighted) {
                return this._visualHighlight();
            } else {
                return this._visualReset();
            }
        },

        /**
         * Method: highlight
         *
         * This method highlights the node visually as long as the node is not already disabled or selected. It is for
         * instance called when the user hovers over a node. Modifies the node's <Node::_highlighted> flag to true.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        highlight: function() {
            this._highlighted = true;
            // don't highlight selected or disabled nodes (visually)
            if (this._selected || this._disabled) return this;

            return this._visualHighlight();
        },

        /**
         * Method: unhighlight
         *
         * Unhighlights the node' visual appearance. The method is for instance calls when the user leaves a hovered
         * node. Modifies the node's <Node::_highlighted> flag to false. Unhighlighting is only possible if the node is
         * not also selected or disabled.
         *
         * P.S.: The weird word unhighlighting is an adoption of the jQueryUI dev team speak, all credits to them :)!
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        unhighlight: function() {
            this._highlighted = false;
            // don't highlight selected or disabled nodes (visually)
            if (this._selected || this._disabled) return this;

            return this._visualReset();
        },

        /**
         * Method: _visualDisable
         *
         * Does the dirty work for visually disabling a node - changes the stroke of all SVG primitives (e.g. path,
         * circle, ...) to the color specified in the <Config>.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _visualDisable: function() {
            this._nodeImage.primitives.css('stroke', this.config.Node.STROKE_DISABLED);
            this._nodeImage.css('opacity', this.config.Dragging.OPACITY);

            return this;
        },

        /**
         * Method: _visualHighlight
         *
         * Does the dirty work for visually changing the appearance of a highlighted node. Removes at first all already
         * applied styles by calling <Node::_visualReset()> and then changes the stroke color of all SVG primitives of
         * the node's image to the color specified in the <Config>.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _visualHighlight: function() {
            this._visualReset();
            this._nodeImage.primitives.css('stroke', this.config.Node.STROKE_HIGHLIGHTED);

            return this;
        },

        /**
         * Small helper method to reset all applied visual changes of the _visual*** method group. Therefore, removes
         * added CSS classes and sets the node's stroke to its initial color.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _visualReset: function() {
            this.container.removeClass(this.config.Classes.NODE_SELECTED);
            this._nodeImage.primitives.css('stroke', this.config.Node.STROKE_NORMAL);
            this._nodeImage.css('opacity', 1);

            return this;
        },

        /**
         * Method: _visualSelect
         *
         * Does the dirty work for visually selecting a node. At first it reset any previously assigned style by
         * calling <Node::_visualReset()>. Then it paints all strokes of the SVG primitives of the node's image using
         * the color specified in the <Config>.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _visualSelect: function() {
            this._visualReset();

            this.container.addClass(this.config.Classes.NODE_SELECTED);
            this._nodeImage.primitives.css('stroke', this.config.Node.STROKE_SELECTED);

            return this;
        }
    });
});
