define(['factory', 'property', 'mirror', 'canvas', 'class', 'config', 'jquery', 'jsplumb'],
function(Factory, Property, Mirror, Canvas, Class, Config) {
    /**
     * Package: Base
     */

    /**
     * Abstract Class: Node
     *      This class models the abstract base class for all nodes. It provides basic functionality for CRUD
     *      operations, setting up visual representation, dragging, selection, <Mirrors>, <Properties> and defines basic
     *      connection rules. Other classes, like e.g. <Editor> and <Graph>, rely on the interface provided by this
     *      class. It is therefore strongly recommended to inherit from <Node> and to add custom behaviour.
     *
     */
    return Class.extend({
        /**
         * Group: Members
         *      {DOMElement}    container           - The DOM element that contains all other visual DOM elements of the node
         *                                            such as its image, mirrors, ...
         *      {<Graph>}       graph               - The Graph this node belongs to.
         *      {Number}        id                  - A client-side generated id to uniquely identify the node in the
         *                                            frontend. It does NOT correlate with database ids in the backend.
         *                                            Introduced to save round-trips and to later allow for an offline
         *                                            mode.
         *      {Array[<Edge>]} incomingEdges       - An enumeration of all edges linking TO this node (this node is the
         *                                            target of the edge).
         *      {Array[<Edge>]} outgoingEdges       - An enumeration of all edges linking FROM this node (this node is
         *                                            the source of the edge).
         *      {DOMElement} _nodeImage             - DOM element that contains the actual image/svg of the node.
         *      {DOMElement} _badge                 - DOM element that contains the badge that can be used to display
         *                                            additional information on a node.
         *      {DOMElement} _nodeImageContainer    - A wrapper for the node image which is necessary to get position
         *                                            calculation working in Firefox.
         *      {DOMElement} _connectionHandle      - DOM element containing the visual representation of the handle
         *                                            where one can pull out new edges.
         */
        container:           undefined,
        graph:               undefined,
        id:                  undefined,
        nodegroups:          undefined,
        incomingEdges:       undefined,
        outgoingEdges:       undefined,

        _nodeImage:          undefined,
        _badge:              undefined,
        _nodeImageContainer: undefined,
        _connectionHandle:   undefined,

        /**
         * Group: Initialization
         */

        /**
         * Constructor: init
         *      The constructor of the abstract node class. It will merge the state of the definition, assign a
         *      client-side id, setup the visual representation and enable interaction via mouse and keyboard. Calling
         *      the constructor as-is, will result in an exception.
         *
         * Parameters:
         *      {Object}     definition                - An object containing default values for the node's definition.
         *                                               E.g.: {x: 1, y: 20, name: 'foo'}. The values will be merged
         *                                               into the node recursively, creating deep copies of complex
         *                                               structures like arrays or other objects. Mainly required for
         *                                               restoring the state of a node when loading a graph from the
         *                                               backend.
         *      {Array[String]} propertiesDisplayOrder - An enumeration of property names, sorted by the order in which
         *                                               the property with the respective name shall appear in the
         *                                               property menu. May contain names of properties that the node
         *                                               does not have.
         */
        init: function(definition) {
            // merge all presets of the configuration and data from the backend into this object
            jQuery.extend(true, this, definition);

            this.nodegroups    = {};
            this.incomingEdges = [];
            this.outgoingEdges = [];

            if (typeof this.id === 'undefined') this.id = this.graph.createId();

            // visuals
            jsPlumb.extend(this.connector, jsPlumb.Defaults.PaintStyle);
            this._setupVisualRepresentation()
                // Additional visual operations - cannot go to _setupVisualRepresentation since they require the
                // container to be already in the DOM/
                ._setupNodeImage()
                ._moveContainerToPixel(Canvas.toPixel(this.x, this.y))
                ._setupConnectionHandle()
                ._setupEndpoints()
				.__setupZIndex()
                // Interaction
                ._setupDragging()
                ._setupMouse()
                ._setupSelection()
                ._setupProperties()
				._setupEditable()
				._setupResizable()
                // Events
                ._registerEventHandlers();

            // call home
            jQuery(document).trigger(Factory.getModule('Config').Events.NODE_ADDED, [
                this.id,
                this.kind,
                this.x,
                this.y,
                this.toDict().properties
            ]);
        },

        /**
         * Method: _setupVisualRepresentation
         *      This method is used in the constructor to set up the visual representation of the node from its kind
         *      string. First, the node's image is created by cloning the corresponding thumbnail from the shape menu
         *      and formatting it. Then, it is appended to a freshly created div element becoming the node's
         *      <Node::container> element.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        _setupVisualRepresentation: function() {
            // get the thumbnail, clone it and wrap it with a container (for labels)
            this._nodeImage = jQuery('#' + Factory.getModule('Config').IDs.SHAPES_MENU + ' #' + this.kind)
                .clone()
                // cleanup the thumbnail's specific properties
                .removeClass('ui-draggable')
                .removeAttr('id')
                // add new classes for the actual node
                .addClass(Factory.getModule('Config').Classes.NODE_IMAGE);
				
            this._badge = jQuery('<span class="badge"></span>')
                .hide();

            this._nodeImageContainer = jQuery('<div>')
                .append(this._nodeImage)
                .append(this._badge);

            this.container = jQuery('<div>')
                .attr('id', this.kind + this.id)
                .addClass(Factory.getModule('Config').Classes.NODE)
                .css('position', 'absolute')
                .data(Factory.getModule('Config').Keys.NODE, this)
                .append(this._nodeImageContainer);
			
            this.container.appendTo(Canvas.container);

            return this;
        },
		
        /**
         * Method: __setupZIndex
         *      This method implements special treatment of z-Index for sticky notes. Sticky notes are normally
         *      displayed behind all other nodes, as well as node connections with a z-Index value of "-1". If a sticky
         *      note gets selected it will be brought in front of all other nodes/connections with a z-Index value of
         *      "101". If a sticky note gets unselected it will be brought in the background again.
		 *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
		__setupZIndex: function(){
			if (this.kind != 'stickyNote') return this;

			jQuery(this.container).css('z-index', '-1');

			jQuery(document).on(Factory.getModule('Config').Events.NODE_SELECTED, function(event, ui) {
				// bring only the sticky note in front that is selected
				if (jQuery(this.container).hasClass('ui-selected'))
					jQuery(this.container).css('z-index', '101');
            }.bind(this));
			
			jQuery(document).on(Factory.getModule('Config').Events.NODE_UNSELECTED, function() {
				jQuery(this.container).css('z-index', '-1')
            }.bind(this));

			return this;
		},

        /**
         * Method: _setupNodeImage
         *      Helper method used in the constructor to setup the actual image of the node. First off it scales the
         *      cloned thumbnail of the node from the shape menu up to the grid size (requires a number SVG of
         *      transformations on all groups) and sets the according image margins to snap to the grid. After that the
         *      <Node::_nodeImage> member is enriched with additional convenience values (primitives, groups, xCenter,
         *      yCenter) to allow faster processing in other methods.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        _setupNodeImage: function() {
            // calculate the scale factor
            var marginOffset = this._nodeImage.outerWidth(true) - this._nodeImage.width();
            var scaleFactor  = (Canvas.gridSize - marginOffset) / this._nodeImage.height();

            // resize the svg and the groups
            this._nodeImage.attr('width',  this._nodeImage.width()  * scaleFactor);
            this._nodeImage.attr('height', this._nodeImage.height() * scaleFactor);

            var newTransform = 'scale(' + scaleFactor + ')';
            var groups = this._nodeImage.find('g');

            if (groups.attr('transform')) newTransform += ' ' + groups.attr('transform');
            groups.attr('transform', newTransform);

            // XXX: In Webkit browsers the container div does not resize properly. This should fix it.
            this.container.width(this._nodeImage.width());
            this.container.height(this._nodeImage.height());

            // cache center of the image
            // XXX: We need to use the node image's container's position because Firefox fails otherwise
            this._nodeImage.xCenter = this._nodeImageContainer.position().left + this._nodeImage.outerWidth(true)  / 2;
            this._nodeImage.yCenter = this._nodeImageContainer.position().top  + this._nodeImage.outerHeight(true) / 2;

            return this;
        },

        /**
         * Method: _setupConnectionHandle
         *      This initialization method is called in the constructor to setup the connection handles of the node.
         *      These are the small plus icons where one can drag edges out of. In the default implementation connectors
         *      are located at the bottom of the image centered.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        _setupConnectionHandle: function() {
            if (this.numberOfOutgoingConnections != 0) {
                this._connectionHandle = jQuery('<i class="fa fa-plus"></i>')
                    .addClass(Factory.getModule('Config').Classes.NODE_HALO_CONNECT + ' ' + Factory.getModule('Config').Classes.NO_PRINT)
                    .css({
                        'top':  this._nodeImage.yCenter + this._nodeImage.outerHeight(true) / 2,
                        'left': this._nodeImage.xCenter
                    })
                    .appendTo(this.container);

                if (this.readOnly) this._connectionHandle.hide();
            }

            return this;
        },

        /**
         * Method: _setupEndpoints
         *      This initialization method does the setup work for endpoints. Endpoints are virtual entities that
         *      function as source as well as target of edges dragged from/to them. They define how many edges and
         *      coming from which node type may be connected to this node. This method serves as a dispatcher to the
         *      sub-methods <Node::_setupIncomingEndpoint> and <Node::_setupOutgoingEndpoint>.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
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
         *      This method sets up the endpoint for incoming connections - i.e. the target - for a node. Therefore it
         *      uses the jsPlumb makeTarget function on the node's container. Nodes that disallow incoming connection do
         *      NOT have any endpoint target.
         *
         * Parameters:
         *      {Array[Number]} anchors          - jsPlumb tuple anchor definition as returned by <connectorAnchors>.
         *      {Object}        connectionOffset - Precise pixel offset of the endpoint in relation to the relative
         *                                         anchor position of the anchor parameter. See also <connectorOffset>.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
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
                        var sourceNode = jQuery('.' + Factory.getModule('Config').Classes.NODE + ':has(#' + elid + ')').data('node');
                        if (typeof sourceNode === 'undefined') return false;

                        // Ask the source node if it can connect to us.
                        return sourceNode.allowsConnectionsTo(this);
                    }.bind(this),
                    activeClass: Factory.getModule('Config').Classes.NODE_DROP_ACTIVE
                }
            });

            return this;
        },

        /**
         * Method: _setupOutgoingEndpoint
         *      This initialization method sets up the endpoint for outgoing connections - i.e. the source - for edges
         *      of this node. The source is in contrary of a target not the whole node, but only the connection handle
         *      of the node (see: <Node::_setupConnectionHandle>). The functionality is provided by the jsPlumb
         *      makeSource call. Nodes that do no allow for outgoing connections do NOT have any source endpoint. In
         *      this method you will also find the callbacks that are responsible for fading out target nodes that do
         *      not allow connection from this node.
         *
         * Parameters:
         *      {Array[Number]} anchors          - jsPlumb tuple anchor definition as returned by <connectorAnchors>.
         *      {Object}        connectionOffset - Precise pixel offset of the endpoint in relation to the relative
         *                                         anchor position of the anchor parameter. See also <connectorOffset>.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        _setupOutgoingEndpoint: function(anchors, connectionOffset) {
            if (this.numberOfOutgoingConnections == 0) return this;

            // small flag for the drag callback, explanation below
            var highlight     = true;
            var inactiveNodes = '.' + Factory.getModule('Config').Classes.NODE + ':not(.'+ Factory.getModule('Config').Classes.NODE_DROP_ACTIVE + ')';

            jsPlumb.makeSource(this._connectionHandle, {
                parent:         this.container,
                anchor:         anchors.concat([connectionOffset.x, connectionOffset.y]),
                maxConnections: this.numberOfOutgoingConnections,
                connectorStyle: this.connector,
                dragOptions: {
                    cursor: Factory.getModule('Config').Dragging.CURSOR_EDGE,
                    // XXX: have to use drag callback here instead of start
                    // The activeClass assigned in <Node::_setupIncomingEndpoint> is unfortunately assigned only AFTER
                    // the execution of the start callback by jsPlumb.
                    drag: function() {
                        // using the highlight flag here to simulate only-once-behaviour (no re-computation of node set)
                        if (!highlight) return;
                        // disable all nodes that can not be targeted
                        jQuery(inactiveNodes).each(function(index, node){
                            jQuery(node).data(Factory.getModule('Config').Keys.NODE).disable();
                        }.bind(this));
                        highlight = false;
                    }.bind(this),
                    stop: function() {
                        // re-enable disabled nodes
                        jQuery(inactiveNodes).each(function(index, node){
                            jQuery(node).data(Factory.getModule('Config').Keys.NODE).enable();
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
         *      This initialization method is called in the constructor and is responsible for setting up the node's
         *      dragging functionality. A user is not able to position nodes freely but can only let nodes snap to grid,
         *      simulating checkered graph paper. The functionality below is multi select aware, meaning a user can drag
         *      multiple node at once.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        _setupDragging: function() {
            if (this.readOnly) return this;

            var initialPositions = {};
            // using jsPlumb draggable and not jQueryUI to allow that edges move together with nodes
            jsPlumb.draggable(this.container, {
                // stay in the canvas
                containment: Canvas.container,
                // become a little bit opaque when dragged
                opacity:     Factory.getModule('Config').Dragging.OPACITY,
                // show a cursor with four arrows
                cursor:      Factory.getModule('Config').Dragging.CURSOR,
                // stick to the checkered paper
                grid:        [Canvas.gridSize, Canvas.gridSize],
                // when dragged a node is send to front, overlaying other nodes and edges
                stack:       '.' + Factory.getModule('Config').Classes.NODE + ', .' + Factory.getModule('Config').Classes.JSPLUMB_CONNECTOR,

                // start dragging callback
                start: function(event) {
                    // XXX: add dragged node to selection
                    // This uses the jQuery.ui.selectable internal functions.
                    // We need to trigger them manually because jQuery.ui.draggable doesn't propagate these events.
                    if (!this.container.hasClass(Factory.getModule('Config').Classes.SELECTED)) {
                        Canvas.container.data(Factory.getModule('Config').Keys.SELECTABLE)._mouseStart(event);
                        Canvas.container.data(Factory.getModule('Config').Keys.SELECTABLE)._mouseStop(event);
                    }

                    // capture the original positions of all (multi) selected nodes and save them
                    jQuery('.' + Factory.getModule('Config').Classes.SELECTED).each(function(index, node) {
                        var nodeInstance = jQuery(node).data(Factory.getModule('Config').Keys.NODE);
                        // if this DOM element does not have an associated node object, do nothing
                        if (typeof nodeInstance === 'undefined') return;

                        initialPositions[nodeInstance.id] = nodeInstance.container.position();
                    }.bind(this));
                }.bind(this),

                drag: function(event, ui) {
                    // enlarge canvas
					Canvas.enlarge({
                        x: ui.offset.left + ui.helper.width(),
                        y: ui.offset.top  + ui.helper.height()
                    });

                    // determine by how many pixels we moved from our original position (see: start callback)
                    var xOffset = ui.position.left - initialPositions[this.id].left;
                    var yOffset = ui.position.top  - initialPositions[this.id].top;

                    // tell all selected nodes to move as well, except this node; the user already dragged it
                    jQuery('.' + Factory.getModule('Config').Classes.SELECTED).not(this.container).each(function(index, node) {
                        var nodeInstance = jQuery(node).data(Factory.getModule('Config').Keys.NODE);
                        // if this DOM element does not have an associated node object, do nothing
                        if (typeof nodeInstance === 'undefined') return;

                        // move the other selectee by the dragging offset, do NOT report to the backend yet
                        nodeInstance._moveContainerToPixel({
                            'x': initialPositions[nodeInstance.id].left + xOffset + nodeInstance._nodeImage.xCenter,
                            'y': initialPositions[nodeInstance.id].top  + yOffset + nodeInstance._nodeImage.yCenter
                        });
                    }.bind(this));
                    jQuery(document).trigger(Factory.getModule('Config').Events.NODES_MOVED);
                }.bind(this),

                // stop dragging callback
                stop: function(event, ui) {
                    // ... calculate the final amount of pixels we moved...
                    var xOffset = ui.position.left - initialPositions[this.id].left;
                    var yOffset = ui.position.top  - initialPositions[this.id].top;

                    jQuery('.' + Factory.getModule('Config').Classes.SELECTED).each(function(index, node) {
                        var nodeInstance = jQuery(node).data(Factory.getModule('Config').Keys.NODE);
                        // if this DOM element does not have an associated node object, do nothing
                        if (typeof nodeInstance === 'undefined') return;

                        // ... and report to the backend this time because dragging ended
                        nodeInstance.moveToPixel({
                            'x': initialPositions[nodeInstance.id].left + xOffset + nodeInstance._nodeImage.xCenter,
                            'y': initialPositions[nodeInstance.id].top  + yOffset + nodeInstance._nodeImage.yCenter
                        });
                    }.bind(this));

                    // forget the initial position of the nodes to allow new dragging
                    initialPositions = {};
                    jQuery(document).trigger(Factory.getModule('Config').Events.NODE_DRAG_STOPPED);
                }.bind(this)
            });

            return this;
        },

        /**
         * Method: _setupMouse
         *      Small helper method used in the constructor for setting up mouse hover highlighting (highlight on hover,
         *      unhighlight on mouse out).
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        _setupMouse: function() {
            if (this.readOnly) return this;
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
         *      This method sets up multi-select functionality for nodes.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        _setupSelection: function() {
            if (this.readOnly) return this;

            //XXX: select a node on click
            // This uses the jQuery.ui.selectable internal functions.
            // We need to trigger them manually because only jQuery.ui.draggable gets the mouseDown events on nodes.
            this.container.click(function(event) {
                Canvas.container.data(Factory.getModule('Config').Keys.SELECTABLE)._mouseStart(event);
                Canvas.container.data(Factory.getModule('Config').Keys.SELECTABLE)._mouseStop(event);
            }.bind(this));

            return this;
        },

        /**
         * Method: _setupProperties
         *      Creates the node's properties instances sorted by the passed display order. If a property passed in the
         *      display order is not present in the node it is skipped silently. When a property in the node's
         *      definition is set to null the property is not created and eventually removed if inherited from its
         *      parent.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        _setupProperties: function() {
            _.each(Factory.getNotation().propertiesDisplayOrder, function(propertyName) {
                var property = this.properties[propertyName];

                if (typeof property === 'undefined') {
                    return;
                } else if (property === null) {
                    delete this.properties[propertyName];
                    return;
                }

                property.name = propertyName;
                this.properties[propertyName] = Factory.getModule('Property').from(this, [ this ], property);
            }.bind(this));

            return this;
        },
		
		/**
		 * Method: _setupResizable
         *      This initialization method is called in the constructor and is responsible for setting up the resizing
         *      of a node. Until now the resizing functionality is intended only for use in resizing sticky notes on the
         *      canvas.
		 *
         * Returns:
         *      This {<Node>} instance for chaining.
		 */
		_setupResizable: function() {
			if (!this.resizable) return this;
			// adapt size of container div to inner resizable div
			this.container.width('auto').height('auto');
			
			var properties = this.properties;
			var _nodeImage = this._nodeImage;
			
			var height = properties.height.value;
			var width  = properties.width.value;
		
			var resizable = this.container.find('.' + Factory.getModule('Config').Classes.RESIZABLE).resizable();
			// setup resizable with width/height values stored in the backend
			jQuery(resizable).height(height).width(width);
			
			// if resizable gets resized update width/height attribute		
			jQuery(resizable).on('resizestop',function() {
				var newWidth = jQuery(this).width();
				var newHeight= jQuery(this).height();
			
				properties.width.setValue(newWidth);
				properties.height.setValue(newHeight);
				// update central point after resizing
	            _nodeImage.xCenter = jQuery(this).outerWidth() / 2;
	            _nodeImage.yCenter = jQuery(this).outerHeight() / 2;
			});
			
			jQuery(resizable).on('resize',function(event, ui) {
                // enlarge canvas if resizable is resized out of the canvas
				Canvas.enlarge({
                    x: ui.helper.offset().left + ui.helper.width(),
                    y: ui.helper.offset().top  + ui.helper.height()
                });
				
				// scroll canvas if resizable is resized out of the visible part of the canvas
				var scrollable    = jQuery('body');
				var screenWidth   = jQuery(window).width();
				var screenHeight  = jQuery(window).height();
				var rightScrolled = scrollable.scrollLeft();
				var downScrolled  = scrollable.scrollTop();
				var scrollOffset  = Factory.getModule('Config').Resizable.SCROLL_OFFSET;
				
				// resize to the right	-> scroll right			
				if (event.clientX > screenWidth - scrollOffset)
					scrollable.scrollLeft(rightScrolled + Canvas.gridSize);
				// resize to the left	-> scroll left
				if (event.clientX <= scrollOffset)
					scrollable.scrollLeft(rightScrolled - Canvas.gridSize);
				
				// resize downwards -> scroll downwards
				if (event.clientY > screenHeight - scrollOffset)
					scrollable.scrollTop(downScrolled + Canvas.gridSize);
				// resize upwards  -> scroll upwards
				if (event.clientY <= scrollOffset)
					scrollable.scrollTop(downScrolled - Canvas.gridSize);
			}.bind(this));
			
			return this;
		},
		
		/**
		 * Method: _setupEditable
         *      This initialization method is called in the constructor and is responsible for setting up the editing
         *      of a node. Until now the editing functionality is intended only for editing sticky notes on the canvas.
		 *      If the sticky note is clicked ,the html paragraph inside the sticky note will be hidden and the
         *      textarea will be displayed.
		 *
         * Returns:
         *      This {<Node>} instance for chaining.
		 */
		_setupEditable: function() {
			if (!this.editable) return this;
			
			var container = this.container
			var editable  = container.find('.'+ Factory.getModule('Config').Classes.EDITABLE);
			var textarea  = editable.find('textarea');				
			var paragraph = editable.find('p');
						
			editable.on('dblclick', function(event) {
				paragraph.toggle(false);
				textarea.toggle(true).focus();
			});
			
			jQuery(document).on(Factory.getModule('Config').Events.NODE_UNSELECTED, function(event) {
				textarea.blur();
			});
				
			return this;
		}, 

        /**
         *  Group: Event Handling
         */

        /**
         *  Method: _registerEventHandlers
         *      Register a listener for edge add and delete events so that we can check the edge count and hide the
         *      connection handle in case we are 'full'.
         *
         *  Returns:
         *      This {<Node>} instance for chaining.
         */
        _registerEventHandlers: function() {
            jQuery(document).on(Factory.getModule('Config').Events.EDGE_ADDED,   this._checkEdgeCapacity.bind(this));
            jQuery(document).on(Factory.getModule('Config').Events.EDGE_DELETED, this._checkEdgeCapacity.bind(this));

            jQuery(document).on(Factory.getModule('Config').Events.NODE_SELECTED, function(event, ui) {
                if (jQuery(ui.selected).data('node') == this) {
                    this.select();
                }
            }.bind(this));

            jQuery(document).on(Factory.getModule('Config').Events.NODE_UNSELECTED, function(event, ui) {
                if (jQuery(ui.unselected).data('node') == this) {
                    this.deselect();
                }
            }.bind(this));

            return this;
        },

        /**
         *  Method: _checkEdgeCapacity
         *      Check if we reached the max. number of outgoing edges allowed and hide the connection handle
         *      in this case.
         *
         *  Returns:
         *      This {<Node>} instance for chaining.
         */
        _checkEdgeCapacity: function() {
            // no need to hide the connection handle if there is none or if we allow infinite connections
            if (typeof this._connectionHandle === 'undefined' || this.numberOfOutgoingConnections == -1) return;

            if (this.outgoingEdges.length >= this.numberOfOutgoingConnections) {
                // full
                this._connectionHandle.hide();
            } else {
                this._connectionHandle.show();
            }

            return this;
        },

        /**
         * Group: Configuration
         */

        /**
         * Method: _connectorAnchors
         *      This method returns the position of the anchors for the connectors. The format is taken from jsPlumb and
         *      is defined as a four-tuple: [x, y, edge_x, edge_y]. The values for x and y define the relative offset of
         *      the connector from the left upper corner of the container. Edge_x and edgy_y determine the direction of
         *      connected edges pointing from or to the connector.
         *
         * Returns:
         *      {Object} with 'in' and 'out' keys containing jsPlumb four-tuple connector definitions.
         */
        _connectorAnchors: function() {
            return {
                'in':  [0.5, 0, 0, -1],
                'out': [0.5, 0, 0,  1]
            }
        },

        /**
         * Method: _connectorOffset
         *      This method returns an object with additional precise pixel offsets for the connectors as defined in
         *      <Node::_connectorAnchors>.
         *
         * Returns:
         *      {Object} with 'in' and 'out' keys containing {Objects} with pixel offsets of the connectors.
         */
        _connectorOffset: function() {
            // XXX: We need to use the offset of the image container because FF has difficulties to calculate the
            //      offsets of inline SVG elements directly.
            var topOffset    = this._nodeImageContainer.offset().top - this.container.offset().top;
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
         *      This method checks if it is allowed to draw an object between this node (source) and the other node
         *      passed as parameter (target). Connections are allowed if and only if, the node does not connect to
         *      itself, the outgoing connections of this node, respectively the incoming connections of the other node
         *      are not exceeded and the notation file allows a connection between these two nodes.
         *
         * Parameters:
         *      {<Node>} otherNode - the node instance to connect to
         *
         * Returns:
         *      A {Boolean} that is true if the connection is allowed or false otherwise
         */
        allowsConnectionsTo: function(otherNode) {
            // no connections to same node
            if (this === otherNode) return false;

            // otherNode must be in the 'allowConnectionTo' list defined in the notations
            var allowed = _.any(this.allowConnectionTo, function(nodeClass) { return otherNode instanceof nodeClass; });
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

        //TODO: documentation
        addToNodeGroup: function(nodegroup) {
            this.nodegroups[nodegroup.id] = nodegroup;
        },

        removeFromNodeGroup: function(nodegroup) {
            delete this.nodegroups[nodegroup.id];
        },

        // the internal variant of removeFromNodeGroup also notifies the nodegroup of the removal
        _removeFromNodeGroup: function(nodegroup) {
            nodegroup.removeNode(this);

            this.removeFromNodeGroup(nodegroup);
        },

        /**
         * Method: setChildProperties
         *      This method will evaluate and set the properties of the passed child according to the value specified
         *      in the childProperties key of the notation file.
         *
         * Parameters:
         *      {<Node>} other - the child of the current node.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        setChildProperties: function(otherNode) {
            _.each(this.childProperties, function(childValues, propertyName) {
                var property = otherNode.properties[propertyName];
                if (typeof property === 'undefined' || property === null) return;

                _.each(childValues, function(value, key) {
                    if (key === 'hidden') {
                        property.setHidden(value);
                    } else if (key === 'value') {
                        property.setValue(value);
                    }
                });
            });

            return this;
        },

        /**
         * Method: restoreChildProperties
         *      This method will reset the children properties previously enforced this node.
         *
         * Parameters:
         *     {<Node>} other - the child of the current node.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        restoreChildProperties: function(otherNode) {
            _.each(this.childProperties, function(childValue, propertyName) {
                var property = otherNode.properties[propertyName];
                if (typeof property === 'undefined' || property === null) return;

                _.each(childValue, function(value, key) {
                    if (key === 'hidden') {
                        property.setHidden(!value);
                    }
                });
            });

            return this;
        },

        /**
         * Group: Accessors
         */

        /**
         * Method: getChildren
         *
         * Returns:
         *      All direct children as {Array[{<Node}>]} of this node.
         */
        getChildren: function() {
            var children = [];
            _.each(this.outgoingEdges, function(edge) {
                children.push(edge.target);
            }.bind(this));
            return children;
        },

         /**
         * Method: toDict
         *
         * Returns:
         *      A key-value {Object} representing of this node.
         */
        toDict: function() {
            var properties = _.map(this.properties, function(prop) { return prop.toDict() });

            return {
                properties: _.reduce(properties, function(memo, prop) {
                    return _.extend(memo, prop);
                }, {}),
                id:       this.id,
                kind:     this.kind,
                x:        this.x,
                y:        this.y,
                outgoing: this.outgoing,
                incoming: this.incoming
            };
        },

        /**
         *  Method: _hierarchy
         *          Recursively computes a dictionary representation of this node's hierarchy. NOTE: This works
         *          currently only with trees. Circular structures, like arbitrary graphs, will produce infinite loops.
         *
         *  Returns:
         *      A dictionary representation of this node's hierarchy. Each entry represents a node with its ID and a
         *      list of children.
         */
        _hierarchy: function() {
            var result = {id: this.id};

            var children = this.getChildren();
            if (children.length != 0) {
                result.children = _.map(children, function(node) {return node._hierarchy();});
            }

            return result;
        },

        /**
         * Group: DOM Manipulation
         */

        /**
         * Method: moveBy
         *      Moves the node's visual representation by the given offset and reports to backend. The center of the
         *      node's image is the anchor point for the translation.
         *
         * Parameters:
         *   {  Object} offset - Object of the form of {x: ..., y: ...} containing the pixel offset to move the node by.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        moveBy: function(offset) {
            var position = this.container.position();

            return this.moveToPixel({
                x: position.left + this._nodeImage.xCenter + offset.x,
                y: position.top  + this._nodeImage.yCenter + offset.y
            });
        },

        /**
         * Method: moveToPixel
         *      Moves the node's visual representation to the given coordinates and reports to backend. The center of
         *      the node's image is the anchor point for the translation.
         *
         * Parameters:
         *      {Object} position  - Object in the form of {x: ..., y: ...} containing the pixel coordinates to move the
         *                           node to.
         *      {Boolean} animated - [optional] If true, the node repositioning is animated.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        moveToPixel: function(position, animated) {
            var gridPos = Canvas.toGrid(position);
            this.x = Math.max(gridPos.x, 0);
            this.y = Math.max(gridPos.y, 0);

            this._moveContainerToPixel(position, animated);
            // call home
            jQuery(document).trigger(Factory.getModule('Config').Events.NODE_PROPERTY_CHANGED, [this.id, {'x': this.x, 'y': this.y}]);

            return this;
        },

        /**
         * Method: moveToGrid
         *      Moves the node's visual representation to the given grid coordinates and reports to backend.
         *
         * Parameters:
         *      {Object} position  - Object in the form of {x: ..., y: ...} containing the grid coordinates to move the
         *                           node to.
         *      {Boolean} animated - [optional] If true, the node repositioning is animated.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        moveToGrid: function(gridPos, animated) {
            this.x = Math.floor(Math.max(gridPos.x, 1));
            this.y = Math.floor(Math.max(gridPos.y, 1));

            var pixelPos = Canvas.toPixel(this.x, this.y);
            this._moveContainerToPixel(pixelPos, animated);

            // call home
            jQuery(document).trigger(Factory.getModule('Config').Events.NODE_PROPERTY_CHANGED, [this.id, {'x': this.x, 'y': this.y}]);

            return this;
        },

        /**
         * Method: remove
         *      Removes the whole visual representation including endpoints from the canvas.
         *
         * Returns:
         *      A {Boolean} indicating successful node deletion.
         */
        remove: function() {
            if (!this.deletable) return false;

            // Remove all incoming and outgoing edges
            _.each(_.union(this.incomingEdges, this.outgoingEdges), function(edge) {
                this.graph.deleteEdge(edge);
            }.bind(this));

            // Tell jsPlumb to remove node endpoints
            _.each(jsPlumb.getEndpoints(this.container), function(endpoint) {
                jsPlumb.deleteEndpoint(endpoint);
            });

            // Remove us from all NodeGroups we are part of
            _.each(this.nodegroups, function(nodegroup) {
                this._removeFromNodeGroup(nodegroup);
            }.bind(this));

            // Call home
            jQuery(document).trigger(Factory.getModule('Config').Events.NODE_DELETED, this.id);
            this.container.remove();

            return true;
        },

        /**
         * Method: _moveContainerToPixel
         *      Moves the node's <Node::container> to the pixel position specified in the position parameter. Does not
         *      take <Canvas> offset or the grid into account. The node's image center is the anchor point for the
         *      translation.
         *
         * Parameters:
         *      {Object}  position - Object of the form {x: ..., y: ...}, where x and y point to integer pixel values
         *                           where the node's container shall be moved to.
         *      {Boolean} animated - [optional] If true, the node repositioning is animated.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        _moveContainerToPixel: function(position, animated) {
            var halfGrid = Canvas.gridSize / 2;
            var x        = Math.max(position.x - this._nodeImage.xCenter, halfGrid);
            var y        = Math.max(position.y - this._nodeImage.yCenter, halfGrid);

            if (animated) {
                jsPlumb.animate(this.container.attr('id'), {
                    left: x,
                    top:  y
                }, {
                    duration: 200,
                    queue:    false,
                    done:     function() { Canvas.enlarge(position); }
                });
            } else {
                this.container.css({
                    left: x,
                    top:  y
                });
                Canvas.enlarge(position);
                // ask jsPlumb to repaint the selectee in order to redraw its connections
                jsPlumb.repaint(this.container);
            }

            return this;
        },

        /**
         * Group: Highlighting
         */

        /**
         * Method: disable
         *      Disables the node visually (fade out) to make it appear to be not interactive for the user.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        disable: function() {
            this.container.addClass(Factory.getModule('Config').Classes.DISABLED);

            return this;
        },

        /**
         * Method: enable
         *      This method node re-enables the node visually and makes appear interactive to the user.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        enable: function() {
            this.container.removeClass(Factory.getModule('Config').Classes.DISABLED);

            return this;
        },

        /**
         * Method: select
         *      Marks the node as selected by adding the corresponding CSS class.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        select: function() {
            this.container.addClass(Factory.getModule('Config').Classes.SELECTED);

            return this;
        },

        /**
         * Method: deselect
         *      This method deselects the node by removing the corresponding CSS class to it.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        deselect: function() {
            this.container.removeClass(Factory.getModule('Config').Classes.SELECTED);

            return this;
        },

        /**
         * Method: highlight
         *      This method highlights the node visually as long as the node is not already disabled or selected. It is
         *      for instance called when the user hovers over a node.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        highlight: function() {
            this.container.addClass(Factory.getModule('Config').Classes.HIGHLIGHTED);

            return this;
        },

        /**
         * Method: unhighlight
         *      Unhighlights the node' visual appearance. The method is for instance calls when the user leaves a
         *      hovered node. P.S.: The weird word unhighlighting is an adoption of the jQueryUI dev team speak, all
         *      credits to them :)!
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        unhighlight: function() {
            this.container.removeClass(Factory.getModule('Config').Classes.HIGHLIGHTED);

            return this;
        },

        /**
         * Method: showBadge
         *      Display a badge on the node.
         *
         * Parameters:
         *      {String} text  - The text that should be displayed in the badge.
         *      {String} style - [optional] The style (color) of the badge.
         *                       See http://twitter.github.io/bootstrap/components.html#labels-badges.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        showBadge: function(text, style) {
            this._badge
                .text(text)
                .addClass('badge')
                .show();
            if (typeof style !== 'undefined')
                this._badge.addClass('badge-' + style);

            return this;
        },

        /**
         * Method: hideBadge
         *      Hides the badge displayed on the node.
         *
         * Returns:
         *      This {<Node>} instance for chaining.
         */
        hideBadge: function() {
            this._badge
                .text('')
                .removeClass()
                .hide();

            return this;
        }
    });
});
