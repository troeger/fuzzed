define(['property', 'class', 'canvas', 'config', 'jquery', 'd3'],
function(Property, Class, Canvas, Config) {
    /**
     *  Class: NodeGroup
     *
     *  Blah
     *
     */
    return Class.extend({
        /**
         *  Group: Members
         *
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
         *
         */
        init: function(definition, nodes, properties) {
            this.nodes      = nodes;
            this.properties = jQuery.extend(true, {}, definition, properties);
            this.graph      = properties.graph;
            this.id         = typeof properties.id === 'undefined' ? this.graph.createId() : properties.id;

            delete this.properties.id;
            delete this.properties.graph;

            this.redraw()
                ._registerEventHandlers()
                ._setupSelection()
                ._setupProperties();

            // call home
            jQuery(document).trigger(Config.Events.NODEGROUP_ADDED, [this.id, this.nodeIds()]);
        },

        /**
         *  Method: _registerEventHandlers
         *
         *  Blah
         *
         */
        _registerEventHandlers: function() {
            jQuery(document).on(Config.Events.NODES_MOVED,  this.redraw.bind(this));

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
         * Method: _setupProperties
         *
         * Returns:
         *   This {<NodeGroup>} instance for chaining.
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

        nodeIds: function() {
            return _.map(this.nodes, function(node) { return node.id });
        },

        redraw: function() {
            var lineFunction = d3.svg.line()
                .x(function(d) { return d[0]; })
                .y(function(d) { return d[1]; })
                //.interpolate("linear");
                .interpolate("basis-closed");

            var dom_id = 'zone'+this.id;
            var hull = d3.select('#'+dom_id);

            if(hull.empty())
            {
                svg = d3.select(Canvas.container.selector)
                    .append("svg")
                    .style('position', 'absolute');

                hull = svg.append('path')
                    .attr('id', dom_id)
                    .style('fill','none')
                    .style('stroke-dasharray', '10,10')
                    .style('stroke-width','2px');
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

            this.container = jQuery('#'+dom_id).addClass(Config.Classes.NODEGROUP)
                                               .data(Config.Keys.NODEGROUP, this);

            return this;
        },

        remove: function() {
            //TODO: put selector into Config
            jQuery('#zone'+this.id).parent().remove();
            jQuery('#zone'+this.id).remove();

            // don't listen anymore
            jQuery(document).off(Config.Events.NODES_MOVED);

            // call home
            jQuery(document).trigger(Config.Events.NODEGROUP_DELETED, [this.id]);

            return true;
        }
    });
});
