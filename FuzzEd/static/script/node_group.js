define(['property', 'class', 'canvas', 'config', 'jquery', 'd3'],
function(Property, Class, Canvas, Config) {
    /**
     *  Class: NodeGroup
     *
     *  This class models a generic group of nodes, further specified in the respective notations file.
     *
     */
    return Class.extend({
        /**
         *  Group: Members
         *
         *  Properties:
         *    {DOMElement}     container       - A jQuery object referring to the node group's html representation.
         *    {<Graph>}        graph           - The Graph this node group belongs to.
         *    {int}            id              - A client-side generated id to uniquely identify the node group in the
         *                                       frontend. It does NOT correlate with database ids in the backend.
         *                                       Introduced to save round-trips and to later allow for an offline mode.
         *    {Array[<Node>]}  nodes           - Enumeration of all nodes this node group belongs to
         *    {Object}         properties      - A dictionary of the node group's properties
         *
         */
        container:     undefined,
        graph:         undefined,
        id:            undefined,
        nodes:         undefined,
        properties:    undefined,

        /**
         * Group: Initialization
         */

        /**
         * Constructor: init
         *
         * A node group's constructor. Merges the given definition and individual properties. Assigns the node group a
         * unique frontend id.
         *
         * Parameters:
         *   {Object}       definition         - An object containing default values for the node's definition.
         *   {Array[<Node>] nodes              - A list of nodes the node group is supposed to connect.
         *   {Object}       properties         - Initial properties to be carried into the NodeGroup object
         *
         */
        init: function(definition, nodes, properties) {
            jQuery.extend(this, definition);

            this.nodes      = nodes;
            this.properties = jQuery.extend(true, {}, definition.properties, properties);
            this.graph      = properties.graph;
            this.id         = typeof properties.id === 'undefined' ? this.graph.createId() : properties.id;

            delete this.properties.id;
            delete this.properties.graph;

            this._setupVisualRepresentation()
                .redraw()
                ._registerEventHandlers()
                ._setupProperties();

            // call home
            jQuery(document).trigger(Config.Events.NODEGROUP_ADDED, [
                this.id,
                this.nodeIds(),
                this.toDict().properties
            ]);
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
                                  Config.Events.NODE_PROPERTY_CHANGED ].join(' '),  this.redraw.bind(this));

            return this;
        },

        /**
         * Method: _setupVisualRepresentation
         *
         * This method is used in the constructor to set up the visual representation of the node group. Initially sets
         * up this.container with css classes, its id and its data.
         *
         * Returns:
         *   This {<Node>} instance for chaining.
         */
        _setupVisualRepresentation: function() {
            this.container = jQuery("<div>")
                .attr('id', Config.Keys.NODEGROUP + this.id)
                .addClass(Config.Classes.NODEGROUP)
                .css('position', 'absolute')
                .data(Config.Keys.NODEGROUP, this);


            // setup nodes' dragging dependency for ui draggable, so the nodes move along with the node group
            _.each(this.nodes, function(node) {
                node.container.addClass(Config.Keys.NODEGROUP + this.id + '_dragging')
            }.bind(this));

            // setup dragging
            var cssClass = Config.Keys.NODEGROUP + this.id + '_dragging'

            var getAll = function(t) {
                return $('.nodegroup' + t.helper.attr('class').match(/nodegroup([0-9]+)_dragging/)[1]).not(t);
            };

            jsPlumb.draggable(this.container, {
                revert: true,
                revertDuration: 10,
                // grouped items animate separately, so leave this number low
                containment: Canvas.container,
                start: function(event) {
                    this.select();
                },
                stop: function(e, ui) {
                    getAll(ui).css({
                        'top': ui.helper.css('top'),
                        'left': 0
                    });
                },
                drag: function(e, ui) {
                    getAll(ui).css({
                        'top': ui.helper.css('top'),
                        'left': ui.helper.css('left')
                    });
                }
            });

            this.container.appendTo(Canvas.container);

            return this;
        },

        /**
         * Method: _setupProperties
         *      Converts the informal properties stored in <properties> into Property objects ordered by this graph's
         *      propertiesDisplayOrder (see <Graph::getNotation()> or the respective notations json-file).
         *
         *      ! Exact code duplication in <Node::_setupProperties()>  and <Edge::_setupPropertes()>
         *
         * Returns:
         *      This {<NodeGroup>} instance for chaining.
         */
        _setupProperties: function() {
            _.each(this.graph.getNotation().propertiesDisplayOrder, function(propertyName) {
                var property = this.properties[propertyName];

                if (typeof property === 'undefined') {
                    return;
                } else if (property === null) {
                    delete this.properties[propertyName];
                    return;
                }

                property.name = propertyName;
                this.properties[propertyName] = Property.from(this, property);
            }.bind(this));

            return this;
        },

        /**
         * Method: nodeIds
         *      Returns an array of all nodes' ids, the NodeGroup holds. Used for lightweight node identification.
         *
         */

        nodeIds: function() {
            return _.map(this.nodes, function(node) { return node.id });
        },

        /**
         * Method: redraw
         *      Uses d3 to calculate and redraw the NodeGroup's visual representation. Finally shrinks the container's
         *      width and height to the svg's.
         *
         * Returns:
         *      This {<NodeGroup>} instance for chaining.
         */

        redraw: function() {
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

            this.container.find('svg path').attr("transform", "translate(-"+bbox.x+",-"+bbox.y+")");

            // ## /hack

            return this;
        },

        /**
         * Method: select
         *   Marks the node group as selected by adding the corresponding CSS class.
         *
         * Returns:
         *   This {<NodeGroup>} instance for chaining.
         */
        select: function() {
            this.container.find('svg path').addClass(Config.Classes.SELECTED);

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
                                   Config.Events.NODE_PROPERTY_CHANGED ].join(' '));

            // call home
            jQuery(document).trigger(Config.Events.NODEGROUP_DELETED, [this.id]);

            return true;
        },

        /**
         * Method: toDict
         *
         * Returns:
         *   A dict representation of the node group avoiding any circular structures.
         */
        toDict: function() {
            var properties = _.map(this.properties, function(prop) { return prop.toDict() });

            return {
                id:           this.id,
                nodeIds:     this.nodeIds(),
                properties:   _.reduce(properties, function(memo, prop) {
                                    return _.extend(memo, prop);
                              })
            }
        }
    });
});
