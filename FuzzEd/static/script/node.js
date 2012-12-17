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
         *    {Object}     config            - An object containing node configuration constants. If not set otherwise,
         *                                     defaults to <Node::getConfig()>.
         *    {DOMElement} container         - The DOM element that contains all other visual DOM elements of the node
         *                                     such as its image, mirrors, ...
         *    {int}        id                - A client-side generated id - i.e. UNIX-timestamp - to uniquely identify
         *                                     the node in the frontend. It does NOT correlate with database ids in the
         *                                     backend. Introduced to save roundtrips and to later allow an offline mode
         *    {Array[<Edge>]} incomingEdges  - An enumeration of all edges linking TO this node (this node is the target
         *                                     target of the edge).
         *    {Array[<Edge>]} outgoingEdges  - An enumeration of all edges linking FROM this node (this node is the
         *                                     source of the edge).
         *    {bool}       _disabled         - Boolean flag indicating whether this node may be a target for a
         *                                     currently drawn edge. True disables connection and therefore fades out
         *                                     the node.
         *    {bool}       _highlighted      - Boolean flag that is true when the node needs to be highlighted on hover.
         *    {bool}       _selected         - Boolean flag that is true when the node is selected - i.e. clicked.
         *    {DOMElement} _nodeImage        - DOM element that contains the actual image/svg of the node.
         *    {DOMElement} _connectionHandle - DOM element containing the visual representation of the handle where one
         *                                     can pull out new edges.
         */
        config:        undefined,
        container:     undefined,
        id:            undefined,
        incomingEdges: undefined,
        outgoingEdges: undefined,

        _disabled:         false,
        _highlighted:      false,
        _selected:         false,
        _nodeImage:        undefined,
        _connectionHandle: undefined,

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
            this._setupVisualRepresentation();
            // some visual stuff, interaction and endpoints need to go here since they require the elements to be
            // already in the DOM.
            this._resize()
                ._moveContainerToPixel(Canvas.toPixel(this.x, this.y))
                ._setupConnectionHandle()
                ._setupEndpoints()
                ._setupDragging()
                ._setupSelection()
                ._setupMouse()
                // properties (that can be changed via menu)
                ._setupMirrors(this.propertyMirrors, propertiesDisplayOrder)
                ._setupPropertyMenuEntries(this.propertyMenuEntries, propertiesDisplayOrder);
        },

        /**
         * Method: _setupMouse
         *
         * Small helper method for setting up mouse hover highlighting (highlight while hovering, unhighlight on mouse
         * out.
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
         *   {bool} - true, if the connection is allowed; false otherwise
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
         * with other classes like <Editor> or <Graph>. Ensure that all notation specific subclasses use them very same
         * reference to the config object.
         *
         * NOTE: Wondering about the reason for this seemingly overly complex config access mechanism? Rest assured we
         * understand you. An attempt for explanation. When using JavaScript "classes" and AMD closures you run quickly
         * into scoping issues when also trying to facilitate inheritance. An Example: Imagine you would like to
         * subclass this class <Node> by another class called Derivative. In Derivative you would like to change some
         * very basic config options. These options shall already be taken into account when executing the abstract base
         * constructor. However, since you required the config already in the base class in form of an AMD closure,
         * there is no way you could possibly obtain the reference to the config in Derived without requiring it again
         * and trying to overwrite presumably constant values. Before the base class reads from the config, in a
         * asynchronous system... For this reason, we worked around it, by requiring the most specific subclass to
         * return the "most up-to-date" config, which that in turn can be easily accessed by the base class.
         *
         * Throws:
         *   Subclass Responsibility
         */
        getConfig: function() {
            throw '[ABSTRACT] Subclass Responsibility';
        },

        /**
         * Group: Visual representation
         */

        /**
         * Method: moveTo
         *   Moves the node's visual representation to the given coordinates and reports to backend.
         *
         * Parameters:
         *   Position {Object} of the form {x: ..., y:...} containing pixel coordinates.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         *
         * Triggers:
         *   <Config::Events::NODE_PROPERTY_CHANGES>
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
         * Removes the complete visual representation of this node from the canvas.
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
         * Method: _resize
         *
         * This method is a small helper for resizing the node image after being dropped onto the canvas. It will scale
         * all parts of the image from the shape menu size up to the canvas' grid size.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _resize: function() {
            // calculate the scale factor
            var marginOffset = this._nodeImage.outerWidth(true) - this._nodeImage.width();
            var scaleFactor  = (Canvas.gridSize - marginOffset) / this._nodeImage.height();

            // resize the svg and the groups
            this._nodeImage.attr('width', this._nodeImage.width()  * scaleFactor);
            this._nodeImage.attr('height', this._nodeImage.height() * scaleFactor);

            var newTransform = 'scale(' + scaleFactor + ')';
            if (this._nodeImage.groups.attr('transform')) {
                newTransform += ' ' + this._nodeImage.groups.attr('transform');
            }
            this._nodeImage.groups.attr('transform', newTransform);

            // XXX: In Webkit browsers the container div does not resize properly. This should fix it.
            this.container.width(this._nodeImage.width());

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
         *   This <Node> instance for chaining.
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
         *   This <Node> instance for chaining.
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

            return this;
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
         * @return {*}
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
         * Method: _visualSelect
         *
         * Does the dirty work for visually selecting a node. At first it reset any previously assigned style by
         * calling <Node::_visualReset()>. Then it paints all strokes of the SVG primitives of the node's image using
         * the color specified in the <Config>.
         *
         * Returns:
         *   This {<Node>} instance for chaining
         */
        _visualSelect: function() {
            this._visualReset();

            this.container.addClass(this.config.Classes.NODE_SELECTED);
            this._nodeImage.primitives.css('stroke', this.config.Node.STROKE_SELECTED);

            return this;
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

            return this;
        },



        //TODO: write comment from here on

        /**
         *  Method: _getPositionOnCanvas
         *      Returns the (pixel) position of the node (center of the node image) relative to the canvas.
         *  Returns:
         *      Object containing the 'x' and 'y' position.
         */
        _getPositionOnCanvas: function() {
            var canvasOffset = Canvas.container.offset();
            return {
                'x': this._nodeImage.offset().left - canvasOffset.left + this._nodeImage.width()  / 2,
                'y': this._nodeImage.offset().top  - canvasOffset.top  + this._nodeImage.height() / 2
            };
        },

        _moveContainerToPixel: function(position) {
            var image = this._nodeImage;
            var offsetX = image.position().left + image.outerWidth(true)  / 2;
            var offsetY = image.position().top  + image.outerHeight(true) / 2;

            this.container.css({
                left: position.x - offsetX || 0,
                top:  position.y - offsetY || 0
            });

            return this;
        },

        _moveByOffset: function(offset, done) {
            if (typeof this._initialPosition === 'undefined') {
                this._initialPosition = this.container.position();
            }
            var newPosition = {
                x: this._initialPosition.left + offset.left + this._nodeImage.outerWidth(true)  / 2,
                y: this._initialPosition.top + offset.top + this._nodeImage.outerHeight(true) / 2
            };

            if (done) {
                this._initialPosition = undefined;
                return this.moveTo(newPosition);
            }

            jsPlumb.repaintEverything();
            return this._moveContainerToPixel(newPosition);
        },

        _setupDragging: function() {
            jsPlumb.draggable(this.container, {
                containment: 'parent',
                opacity:     this.config.Dragging.OPACITY,
                cursor:      this.config.Dragging.CURSOR,
                grid:        [Canvas.gridSize, Canvas.gridSize],
                stack:       '.' + this.config.Classes.NODE + ', .' + this.config.Classes.JSPLUMB_CONNECTOR,

                // start dragging callback
                start: function(event) {
                    this._initialPosition = this.container.position();

                    //XXX: add dragged node to selection
                    // This uses the jQuery.ui.selectable internal functions.
                    // We need to trigger them manually because jQuery.ui.draggable doesn't propagate these events.
                    if (!this.container.hasClass(this.config.Classes.JQUERY_UI_SELECTED)) {
                        Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStart(event);
                        Canvas.container.data(this.config.Keys.SELECTABLE)._mouseStop(event);
                    }
                }.bind(this),

                drag: function(event, ui) {
                    // tell all selected nodes to move as well
                    var offset = {
                        left: ui.position.left - this._initialPosition.left,
                        top:  ui.position.top  - this._initialPosition.top
                    };
                    jQuery('.' + this.config.Classes.JQUERY_UI_SELECTED).not(this.container).each(function(index, node) {
                        jQuery(node).data(this.config.Keys.NODE)._moveByOffset(offset, false);
                    }.bind(this));
                }.bind(this),

                // stop dragging callback
                stop: function(event, ui) {
                    this.moveTo(this._getPositionOnCanvas());

                    var offset = {
                        left: ui.position.left - this._initialPosition.left,
                        top:  ui.position.top  - this._initialPosition.top
                    };
                    // final move is necessary to propagate the changes to the backend
                    jQuery('.' + this.config.Classes.JQUERY_UI_SELECTED).not(this.container).each(function(index, node) {
                        jQuery(node).data(this.config.Keys.NODE)._moveByOffset(offset, true);
                    }.bind(this));

                    this._initialPosition = undefined;
                }.bind(this)
            });

            return this;
        },

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

        _connectorAnchors: function() {
            return {
                'in':  [0.5, 0, 0, -1],
                'out': [0.5, 0, 0,  1]
            }
        },

        _setupEndpoints: function() {
            var anchors = this._connectorAnchors();
            var offset  = this._connectorOffset();

            this._setupIncomingEndpoint(anchors.in,  offset.in)
                ._setupOutgoingEndpoint(anchors.out, offset.out);

            return this;
        },

        _setupIncomingEndpoint: function(anchors, connectionOffset) {
            if (this.numberOfIncomingConnections == 0) return this;
            // make node target
            jsPlumb.makeTarget(this.container, {
                anchor:         anchors.concat([connectionOffset.x, connectionOffset.y]),
                maxConnections: this.numberOfIncomingConnections,
                dropOptions: {
                    accept: function(draggable) {
                        var elid = draggable.attr('elid');
                        if (typeof elid === 'undefined') return false;

                        // this is not a connection-dragging-scenario
                        var sourceNode = jQuery('.' + this.config.Classes.NODE + ':has(#' + elid + ')').data('node');
                        if (typeof sourceNode === 'undefined') return false;

                        return sourceNode.allowsConnectionsTo(this);
                    }.bind(this),
                    activeClass: this.config.Classes.NODE_DROP_ACTIVE
                }
            });

            return this;
        },

        _setupOutgoingEndpoint: function(anchors, connectionOffset) {
            if (this.numberOfOutgoingConnections == 0) return this;

            // make node source
            jsPlumb.makeSource(this._connectionHandle, {
                parent:         this.container,
                anchor:         anchors.concat([connectionOffset.x, connectionOffset.y]),
                maxConnections: this.numberOfOutgoingConnections,
                connectorStyle: this.connector,
                dragOptions: {
                    drag: function() {
                        // disable all nodes that can not be targeted
                        var nodesToDisable = jQuery('.' + this.config.Classes.NODE + ':not(.'+ this.config.Classes.NODE_DROP_ACTIVE + ')');
                        nodesToDisable.each(function(index, node){
                            jQuery(node).data(this.config.Keys.NODE).disable();
                        }.bind(this));
                    }.bind(this),
                    stop: function() {
                        // re-enable disabled nodes
                        var nodesToEnable = jQuery('.' + this.config.Classes.NODE + ':not(.'+ this.config.Classes.NODE_DROP_ACTIVE + ')');
                        nodesToEnable.each(function(index, node){
                            jQuery(node).data(this.config.Keys.NODE).enable();
                        }.bind(this));
                    }.bind(this)
                }
            });

            return this;
        },

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

        _setupConnectionHandle: function() {
            if (this.numberOfOutgoingConnections != 0) {
                this._connectionHandle = jQuery('<i class="icon-plus icon-white"></i>')
                    .addClass(this.config.Classes.NODE_HALO_CONNECT)
                    .css({
                        'top':  this._nodeImage.position().top  + this._nodeImage.outerHeight(true),
                        'left': this._nodeImage.position().left + this._nodeImage.outerWidth(true) / 2
                    })
                    .appendTo(this.container);
            }

            return this;
        },

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

        _setupVisualRepresentation: function() {
            // get the thumbnail, clone it and wrap it with a container (for labels)
            this._nodeImage = jQuery('#' + this.config.IDs.SHAPES_MENU + ' #' + this.kind)
                .clone()
                // cleanup the thumbnail's specific properties
                .removeClass('ui-draggable')
                .removeAttr('id')
                // add new classes for the actual node
                .addClass(this.config.Classes.NODE_IMAGE);

            this.container = jQuery('<div>')
                .attr('id', this.kind + this.id)
                .addClass(this.config.Classes.NODE)
                .css('position', 'absolute')
                .data(this.config.Keys.NODE, this)
                .append(this._nodeImage);

            // links to primitive shapes and groups of the SVG for later manipulation (highlighting, ...)
            this._nodeImage.primitives = this._nodeImage.find('rect, circle, path');
            this._nodeImage.groups = this._nodeImage.find('g');

            this.container.appendTo(Canvas.container);

            return this;
        }
    })
});
