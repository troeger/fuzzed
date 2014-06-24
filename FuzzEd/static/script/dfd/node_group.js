define(['node_group', 'property', 'class', 'canvas', 'config', 'jquery', 'd3'],
    function(NodeGroup, Property, Class, Canvas, Config) {

    /**
     * Package: Faulttree
     */

    /**
     * Class: FaulttreeNodeGroup
     *
     * Extends: <Base::NodeGroup>
     */
    return NodeGroup.extend({
        container:     undefined,

        init: function(definition, nodes, properties) {
            jQuery.extend(this, definition);

            this.nodes      = nodes;
            this.properties = jQuery.extend(true, {}, definition.properties, properties);
            this.graph      = properties.graph;
            this.id         = typeof properties.id === 'undefined' ? this.graph.createId() : properties.id;

            _.each(this.nodes, function(node) {
                node.addToNodeGroup(this);
            }.bind(this));

            delete this.properties.id;
            delete this.properties.graph;

            this._setupVisualRepresentation()
                ._redraw()
                ._setupDragging()
                ._setupMouse()
                ._setupSelection()
                ._registerEventHandlers()
                ._setupProperties();

            // call home
            jQuery(document).trigger(Config.Events.NODEGROUP_ADDED, [
                this.id,
                this.nodeIds(),
                this.toDict().properties,
                this
            ]);
        },


        /**
         * Method: _setupVisualRepresentation
         *
         * This method is used in the constructor to set up the visual representation of the node group. Initially sets
         * up this.container with css classes, its id and its data.
         *
         * Returns:
         *   This {<NodeGroup>} instance for chaining.
         */
        _setupVisualRepresentation: function() {
            this.container = jQuery("<div>")
                .attr('id', Config.Keys.NODEGROUP + this.id)
                .addClass(Config.Classes.NODEGROUP)
                .css('position', 'absolute')
                .data(Config.Keys.NODEGROUP, this);

            this.container.appendTo(Canvas.container);

            return this;
        },

        /**
         * Method: _setupDragging
         *
         * This initialization method is called in the constructor and is responsible for setting up the node group's
         * dragging functionality. The goal is to make all contained nodes move along with the node group.  The code
         * contains a lot of code <Node> uses to setup dragging as well.
         *
         * Returns:
         *   This {<NodeGroup>} instance for chaining.
         */
        _setupDragging: function() {
            if (this.readOnly) return this;

            // the css class which refers to all dependant nodes
            var dragDependant = Config.Keys.NODEGROUP + this.id + '_dragging'

            // setup nodes' dragging dependency for ui draggable via a nodegroup-specific css class
            _.each(this.nodes, function(node) {
                node.container.addClass(dragDependant);
            }.bind(this));

            var initialPosition = undefined;
            var initialNodePositions = {};

            jsPlumb.draggable(this.path(), {
                // stay in the canvas
                containment: Canvas.container,
                // become a little bit opaque when dragged
                opacity:     Config.Dragging.OPACITY,
                // show a cursor with four arrows
                cursor:      Config.Dragging.CURSOR,
                // stick to the checkered paper
                grid:        [Canvas.gridSize, Canvas.gridSize],

                // start dragging callback
                start: function(event, ui) {
                    // XXX: add dragged node to selection
                    // This uses the jQuery.ui.selectable internal functions.
                    // We need to trigger them manually because jQuery.ui.draggable doesn't propagate these events.
                    if (!this.path().hasClass(Config.Classes.SELECTED)) {
                        Canvas.container.data(Config.Keys.SELECTABLE)._mouseStart(event);
                        Canvas.container.data(Config.Keys.SELECTABLE)._mouseStop(event);
                    }

                    // save the initial positions of the node group and dependant nodes, to calculate offsets while dragging
                    initialPosition = this.path().position();
                    jQuery('.' + dragDependant).each(function(index, node) {
                        var nodeInstance = jQuery(node).data(Config.Keys.NODE);
                        // if this DOM element does not have an associated node object, do nothing
                        if (typeof nodeInstance === 'undefined') return;

                        initialNodePositions[nodeInstance.id] = nodeInstance.container.position();
                    }.bind(this));
                }.bind(this),

                drag: function(event, ui) {
                    // enlarge canvas
					Canvas.enlarge({
                        x: ui.offset.left + ui.helper.width(),
                        y: ui.offset.top  + ui.helper.height()
                    });

                    // determine by how many pixels we moved from our original position (see: start callback)
                    var xOffset = ui.position.left - initialPosition.left;
                    var yOffset = ui.position.top  - initialPosition.top;

                    // tell all dependant nodes to move as well, except this node group as the user already dragged it
                    jQuery('.' + dragDependant).not(this.container).each(function(index, node) {
                        var nodeInstance = jQuery(node).data(Config.Keys.NODE);
                        // if this DOM element does not have an associated node object, do nothing
                        if (typeof nodeInstance === 'undefined') return;

                        // move the other selectee by the dragging offset, do NOT report to the backend yet
                        nodeInstance._moveContainerToPixel({
                            'x': initialNodePositions[nodeInstance.id].left + xOffset + nodeInstance._nodeImage.xCenter,
                            'y': initialNodePositions[nodeInstance.id].top  + yOffset + nodeInstance._nodeImage.yCenter
                        });
                    }.bind(this));
                    jQuery(document).trigger(Config.Events.NODES_MOVED);
                }.bind(this),

                // stop dragging callback
                stop: function(e, ui) {
                    // redraw the node group's visual representation
                    this._redraw();

                    // calculate the final amount of pixels we moved ...
                    var xOffset = ui.position.left - initialPosition.left;
                    var yOffset = ui.position.top  - initialPosition.top;

                    jQuery('.' + dragDependant).each(function(index, node) {
                        var nodeInstance = jQuery(node).data(Config.Keys.NODE);
                        // if this DOM element does not have an associated node object, do nothing
                        if (typeof nodeInstance === 'undefined') return;

                        // ... and report to the backend this time because dragging ended
                        nodeInstance.moveToPixel({
                            'x': initialNodePositions[nodeInstance.id].left + xOffset + nodeInstance._nodeImage.xCenter,
                            'y': initialNodePositions[nodeInstance.id].top  + yOffset + nodeInstance._nodeImage.yCenter
                        });
                    }.bind(this));

                    // forget the initial position of the nodes to allow new dragging
                    initialPositions = {};
                    jQuery(document).trigger(Config.Events.NODE_DRAG_STOPPED);
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
         *   This {<NodeGroup>} instance for chaining.
         */
        _setupMouse: function() {
            if (this.readOnly) return this;
            // hovering over a node
            this.path().hover(
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
         * This initialization method is called in the constructor and sets up multi-select functionality for node groups.
         *
         * Returns:
         *   This {<NodeGroup>} instance for chaining.
         */
        _setupSelection: function() {
            if (this.readOnly) return this;

            //XXX: select a node group on click
            // This uses the jQuery.ui.selectable internal functions.
            // We need to trigger them manually because only jQuery.ui.draggable gets the mouseDown events on node groups.
            this.container.click(function(event) {
                Canvas.container.data(Config.Keys.SELECTABLE)._mouseStart(event);
                Canvas.container.data(Config.Keys.SELECTABLE)._mouseStop(event);
            }.bind(this));

            return this;
        },

        /**
         *  Method: _registerEventHandlers
         *      Add listeners to react on moves and property changes of nodes.
         *
         *  Returns:
         *      This NodeGroup instance for chaining.
         *
         */
        _registerEventHandlers: function() {
            jQuery(document).on([ Config.Events.NODES_MOVED,
                                  Config.Events.NODE_PROPERTY_CHANGED ].join(' '),  this._redraw.bind(this));

            return this;
        },

        /**
         * Method: redraw
         *      Uses d3 to calculate and redraw the NodeGroup's visual representation. Finally shrinks the container's
         *      width and height to the svg's.
         *
         * Returns:
         *      This {<NodeGroup>} instance for chaining.
         */

        _redraw: function() {
            var dom_id = Config.Keys.NODEGROUP + this.id;

            var lineFunction = d3.svg.line()
                .x(function(d) { return d[0]; })
                .y(function(d) { return d[1]; })
                //.interpolate("linear");
                .interpolate("basis-closed");

            var hull = d3.select('#'+dom_id+' svg path');
            var svg  = d3.select('#'+dom_id+' svg');

            if(hull.empty())
            {
                svg = d3.select('#'+dom_id).append('svg');

                hull = svg.append('path')
                    .style('fill','none')
                    .style('stroke-dasharray', '10,10')
                    .style('stroke-width','3px');
            }

            var outer_circle = function(c, r) {
                var count = 16;
                var step = Math.PI * 2 / count, current = 0, a = [];
                for (var i = 0; i < count; i++) {
                    var x = c.x + (r * Math.cos(current)),
                        y = c.y + (r * Math.sin(current));
                    a.push( [ x, y]);
                    current += step;
                }
                return a;
            };

            var vertices = _.map(this.nodes, function(node) {
                var center = {x: node.container.position().left + node.container.width() / 2,
                              y: node.container.position().top + node.container.height() / 2};
                return outer_circle(center, 50);
            }.bind(this));

            var _dist = function(a, b)
            {
                return Math.sqrt(Math.pow(a[0]-b[0],2)+Math.pow(a[1]-b[1],2));
            }

            vertices = _.flatten(vertices, true);
            vertices = d3.geom.hull(vertices);
            hull.attr('d', lineFunction(vertices));

            // ## WARNING: This is a pretty nasty hack for guys like me who have no clue of svg paths; feel free to do
            // ## this nicely, I'm seriously interested!

            var bbox = jQuery('#'+dom_id+' svg path')[0].getBBox();

            this.container.css('width', bbox.width);
            this.container.css('height', bbox.height);
            this.container.css('left', bbox.x);
            this.container.css('top', bbox.y);

            this.path().attr("transform", "translate(-"+bbox.x+",-"+bbox.y+")");

            // ## /hack

            return this;
        },

        /**
         * Method: remove
         *      Removes the whole visual representation from the canvas, deactivates listeners and calls home.
         *
         * Returns:
         *   {boolean} Successful deletion.
         */
        remove: function() {
            if (!this.deletable) return false;
            this.container.remove();

            // remove nodes' dragging dependency for ui draggable
            _.each(this.nodes, function(node) {
                node.container.addClass(Config.Keys.NODEGROUP + this.id + '_dragging')
            }.bind(this));

            // don't listen anymore
            jQuery(document).off([ Config.Events.NODES_MOVED,
                                   Config.Events.NODE_PROPERTY_CHANGED ].join(' '), this._redraw.bind(this));

            this._super();
        },

       removeNode: function(node) {
            this._redraw();
            this._super(node);
        },

        /**
         * Method: path
         *      Convenience method for accessing the svg-path within the container
         */

        path: function() {
            return this.container.find('svg path');
        }

    });
});
