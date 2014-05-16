define(['graph', 'dfd/node', 'dfd/config', 'json!notations/dfd.json', 'canvas', 'underscore', 'd3'],
function(Graph, DfdNode, DfdConfig, DfdNotation, Canvas) {
    /**
     *  Package: Faulttree
     */

    /**
     *  Class: Graph
     *
     *  Faulttree-specific graph.
     *
     *  Extends <Base::Graph>.
     */
    return Graph.extend({
        /**
         *  Group: Members
         *
         *  Properties:
         *    {Object}  zones       - A map that stores all communication zones of the graph by their ID.
         */
        //zones:        {},

        /**
         *  Method: getConfig
         *    See <Base::Graph::getConfig>.
         */
        getConfig: function() {
            return DfdConfig;
        },

        /**
         *  Method: getNodeClass
         *    See <Base::Graph::getNodeClass>.
         */
        getNodeClass: function() {
            return DfdNode;
        },

        /**
         *  Method: getNotation
         *    See <Base::Graph::getNotation>.
         */
        getNotation: function() {
            return DfdNotation;
        },

        /**
         *  Method: _getNodeHierarchy
         *    Returns a dictionary representation of the node hierarchy of this graph.
         *
         *  Returns:
         *    A dictionary representation of the node hierarchy of this graph. Each entry represents a node with
         *    its ID and a list of children.
         */
        _getNodeHierarchy: function() {
            return this.getNodeById(0)._hierarchy();
        },

        /**
         *  Method: _getClusterLayoutAlgorithm
         *    Returns the cluster layouting algorithm supported by this graph.
         */
        _getClusterLayoutAlgorithm: function() {

            return function(nodes){
                var nodes = _.map(this.nodes, function(node, i) {
                    return {
                        x: node.x, 
                        y: node.y, 
                        px: node.x,
                        py: node.y,
                        index: i, 
                        node_obj: node, 
                        id: node.id,
                        fixed: false,
                    };
                }.bind(this));

                var id_map = _.map(nodes, function(n){
                    return n.node_obj.id;
                }.bind(this));

                var links = _.map(this.edges, function(edge) {
                    return {
                        source: id_map.indexOf(edge.source.id),
                        target: id_map.indexOf(edge.target.id),
                    }
                }.bind(this));

                var forceLayout = d3.layout.force();

                var tick = function(e) {
                    _.each(nodes, function(n) {
                        var gridx = Math.round(n.x);
                        var gridy = Math.round(n.y);
                        var a = Math.min(1.0, forceLayout.alpha() * 10);
                        n.x = a*n.x + (1-a)*gridx;
                        n.y = a*n.y + (1-a)*gridy;
                    }.bind(this));
                }.bind(this);

                forceLayout = forceLayout
                    .nodes(nodes)
                    .links(links)
                    .on("tick", tick)
                    .charge(-0.5)
                    .linkDistance(4)
                    .linkStrength(0.6)
                    .size([20, 10]);

                for(var k=0; k<10; k++)
                {
                    forceLayout.start();
                    var n = 1000;
                    for (var i = 0; i < n; ++i) 
                       forceLayout.tick();
                    forceLayout.stop();
                }

                return forceLayout.nodes();
            }.bind(this);
        },

        /**
         *  Method: _getTreeLayoutAlgorithm
         *    Returns the tree cluster layouting algorithm supported by this graph.
         */
        _getTreeLayoutAlgorithm: function() {
            throw new Error("Tree Layout not supported.");
        },

        /**
         *  Method: _layoutWithAlgorithm
         *    Layouts the nodes of this graph with the given layouting algorithm.
         *    We overwrite here because RBDs are layouted horizontally (change x and y).
         *
         *  Returns:
         *    This <Graph> instance for chaining.
         */
        _layoutWithAlgorithm: function(algorithm) {
            var layoutedNodes = algorithm();

            // move to the upper border
            var minY = _.min(layoutedNodes, function(n) {return n.y}).y;
            var offsetY = 1 - minY;

            // center horizontally
            var centerX = Math.floor((jQuery('#' + this.config.IDs.CANVAS).width() / this.config.Grid.SIZE) / 2);
            
            var minX = _.min(layoutedNodes, function(n) {return n.x}).x;
            var maxX = _.max(layoutedNodes, function(n) {return n.x}).x;

            var offsetX = centerX - (minX+maxX)/2;

            // apply positions
            _.each(layoutedNodes, function(n) {
                var node = this.getNodeById(n.id);
                node.moveToGrid({x: n.x+offsetX, y: n.y+offsetY}, false);
            }.bind(this));

            return this;
        }

        /*
        _registerEventHandlers: function() {
            this._initialize_zones();

            jQuery(document).on(this.config.Events.NODES_MOVED,   this._redraw_communication_zones.bind(this));
            jQuery(document).on(this.config.Events.NODE_DELETED,  this._delete_node_from_zones.bind(this));
            //jQuery(document).on(this.config.Events.NODE_ADDED,    this._add_node_to_zones.bind(this));

            return this._super()
        },

        _initialize_zones: function() {
            _.each(this.nodes, function(node){
                this._add_node_to_zones(undefined, node.id);
            }, this);
        },

        _add_node_to_zones: function(event, nodeId) {
            var node = this.getNodeById(nodeId);
            var zone_ids = JSON.parse(node.properties['zones'].value);
                _.each(zone_ids, function(zone_id){
                    if(this.zones[zone_id] === undefined)
                        this.zones[zone_id] = [node.id];
                    else
                        this.zones[zone_id].push(node.id);
                }, this);
            this._redraw_communication_zones();
        },

        _delete_node_from_zones: function(event, nodeId) {

            for(var zoneId in this.zones){
                this.zones[zoneId] = _.without(this.zones[zoneId], nodeId);
                if(this.zones[zoneId].length < 2){
                    this.delete_communication_zone(_.map(this.zones[zoneId], this.getNodeById.bind(this)));
                }
            }
            this._redraw_communication_zones();

        },


        create_communication_zone: function(nodes) {
            var zoneId = this.createId();
            this.zones[zoneId] = _.map(nodes, function(node){return node.id;});

            _.each(nodes, function(node){
                var node_zones = JSON.parse(node.properties['zones'].value);
                node_zones.push(zoneId);
                node.properties['zones'].setValue(JSON.stringify(node_zones));
            });

            this._redraw_communication_zones();
        },

        delete_communication_zone: function(nodes) {
            nodes = _.map(nodes, function(node){return node.id;}).sort();
            var zones_ids = _.keys(this.zones).sort().reverse();
            zoneId = _.find(zones_ids, function(zoneId){
                return _.isEqual(this.zones[zoneId].sort(), nodes);
            }.bind(this));

            if(zoneId === undefined)
                return;
            zoneId = parseInt(zoneId);

            _.each(this.zones[zoneId], function(nodeId){
                var node = this.getNodeById(nodeId);
                var node_zones = JSON.parse(node.properties['zones'].value);
                node_zones = _.without(node_zones, zoneId);
                node.properties['zones'].setValue(JSON.stringify(node_zones));
            }, this);

            delete this.zones[zoneId];
            jQuery('#zone'+zoneId).remove();

        },

        _redraw_communication_zones: function() {

            var lineFunction = d3.svg.line()
                .x(function(d) { return d[0]; })
                .y(function(d) { return d[1]; })
                //.interpolate("linear");
                .interpolate("basis-closed");

            for(var zoneId in this.zones)
            {
                var dom_id = 'zone'+zoneId;
                var hull = d3.select('#'+dom_id);
               
                if(hull.empty())
                {
                    svg = d3.select(Canvas.container.selector)
                        .append("svg")
                        .style('position', 'absolute');

                    hull = svg.append('path')
                        .attr('id', dom_id)
                        .style('fill','none')
                        .style('stroke','steelblue')
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

                var vertices = _.map(this.zones[zoneId], function(nodeId) {
                    var node = this.getNodeById(nodeId);
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

            }
        }*/
    });
});