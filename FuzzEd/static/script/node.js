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
         *  Group: public
         *
         *  Properties:
         *    {Object}     config         - An object containing node configuration constants as found in <Config>.
         *    {DOMElement} container      - The DOM element that contains all other visual DOM elements of the node
         *                                  such as its image, mirrors, ...
         *    {int}        id             - A client-side generated id - i.e. UNIX-timestamp - to uniquely identify the
         *                                  node in the frontend. It does NOT correlate with database ids in the
         *                                  backend.
         *    {Array[Edge]} incomingEdges - An enumeration of all edges linking TO this node (this node is the target
         *                                  target of the edge).
         *    {Array[Edge]} outgoingEdges - An enumeration of all edges linking FROM this node (this node is the source
         *                                  of the edge).
         */
        config:        undefined,
        container:     undefined,
        id:            undefined,
        incomingEdges: undefined,
        outgoingEdges: undefined,

        /**
         *  Group: private
         *
         *  Properties:
         *    {bool}       _disabled         - Boolean flag indicating whether this node may be a target for a
         *                                     currently drawn edge. True disables connection and therefore fades out
         *                                     the node.
         *    {bool}       _highlighted      - Boolean flag that is true when the node needs to be highlighted on hover.
         *    {bool}       _selected         - Boolean flag that is true when the node is selected - i.e. clicked.
         *    {DOMElement} _nodeImage        - DOM element that contains the actual image/svg of the node.
         *    {DOMElement} _connectionHandle - DOM element containing the visual representation of the handle where one
         *                                     can pull out new edges.
         */
        _disabled:         false,
        _highlighted:      false,
        _selected:         false,
        _nodeImage:        undefined,
        _connectionHandle: undefined,

        /**
         * Constructor: init
         *
         * Parameters:
         *   {Object}        properties             - An object containing
         *   {Array[string]} propertiesDisplayOrder - An enumeration of property names, sorted by the order in which
         *                                            the property with the respective name shall appear in the property
         *                                            menu. May contain names of properties that the node does not have.
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

        remove: function() {
            _.each(jsPlumb.getEndpoints(this.container), function(endpoint) {
                jsPlumb.deleteEndpoint(endpoint);
            });
            this.container.remove();

            return this;
        },

        /**
         * Method: moveTo
         *     Moves the node's visual representation to the given coordinates and reports to backend.
         *
         * Parameters
         *     position - Position in form {x: ..., y:...} containing the pixel coordinates the nodes should move to.
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

        select: function() {
            // don't allow selection of disabled nodes
            if (this._disabled) return this;

            this._selected = true;
            return this._visualSelect();
        },

        deselect: function() {
            this._selected = false;

            if (this._highlighted) {
                return this._visualHighlight();
            } else {
                return this._visualReset();
            }
        },

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

        disable: function() {
            this._disabled = true;
            return this._visualDisable();
        },

        highlight: function() {
            this._highlighted = true;
            // don't highlight selected or disabled nodes (visually)
            if (this._selected || this._disabled) return this;

            return this._visualHighlight();
        },

        unhighlight: function() {
            this._highlighted = false;
            // don't highlight selected or disabled nodes (visually)
            if (this._selected || this._disabled) return this;

            return this._visualReset();
        },

        _visualSelect: function() {
            this._visualReset();

            this.container.addClass(this.config.Classes.NODE_SELECTED);
            this._nodeImage.primitives.css('stroke', this.config.Node.STROKE_SELECTED);

            return this;
        },

        _visualHighlight: function() {
            this._visualReset();

            this._nodeImage.primitives.css('stroke', this.config.Node.STROKE_HIGHLIGHTED);

            return this;
        },

        _visualDisable: function() {
            this._nodeImage.primitives.css('stroke', this.config.Node.STROKE_DISABLED);

            return this;
        },

        _visualReset: function() {
            this.container.removeClass(this.config.Classes.NODE_SELECTED);
            this._nodeImage.primitives.css('stroke', this.config.Node.STROKE_NORMAL);

            return this;
        },

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

        getConfig: function() {
            throw '[ABSTRACT] subclass responsibility';
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
