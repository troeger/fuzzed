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
            jQuery.extend(this, definition);

            this.nodes      = nodes;
            this.properties = jQuery.extend(true, {}, definition.properties, properties);
            this.graph      = properties.graph;
            this.id         = typeof properties.id === 'undefined' ? this.graph.createId() : properties.id;

            delete this.properties.id;
            delete this.properties.graph;

            this.redraw()
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
         *
         *  Blah
         *
         */
        _registerEventHandlers: function() {
            jQuery(document).on(Config.Events.NODES_MOVED,  this.redraw.bind(this));
            jQuery(document).on(Config.Events.NODE_PROPERTY_CHANGED,  this.redraw.bind(this));

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
            //TODO: -> Config
            var dom_id = 'zone'+this.id;

            if (this.container === undefined) {
                this.container = jQuery("<div>")
                    .attr('id', dom_id)
                    .addClass(Config.Classes.NODEGROUP)
                    .css('position', 'absolute')
                    .data(Config.Keys.NODEGROUP, this);
            } else {
                this.container = jQuery('#'+dom_id)
            }

            this.container.appendTo(Canvas.container);

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

        select: function() {
            this.container.find('svg path').addClass(Config.Classes.SELECTED);
        },

        remove: function() {
            if (!this.deletable) return false;

            //TODO: put selector into Config
            jQuery('#zone'+this.id).remove();

            // don't listen anymore
            jQuery(document).off(Config.Events.NODES_MOVED);

            // call home
            jQuery(document).trigger(Config.Events.NODEGROUP_DELETED, [this.id]);

            return true;
        },

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
