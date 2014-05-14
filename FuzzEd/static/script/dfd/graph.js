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
    });
});