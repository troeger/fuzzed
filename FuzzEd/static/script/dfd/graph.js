define(['factory', 'graph', 'dfd/node', 'dfd/config', 'json!notations/dfd.json', 'underscore', 'd3'],
function(Factory, Graph, DfdNode, DfdConfig, DfdNotation) {
    /**
     * Package: DFD
     */

    /**
     * Class: Graph
     *      DFD-specific graph subclass. Mainly adds node group functionality
     *
     *  Extends <Base::Graph>.
     */
    return Graph.extend({
        getConfig: function() {
            return DfdConfig;
        },

        getNodeClass: function() {
            return DfdNode;
        },

        getNotation: function() {
            return DfdNotation;
        },
        _getNodeHierarchy: function() {
            return this.getNodeById(0)._hierarchy();
        },

        _getClusterLayoutAlgorithm: function() {
            return function() {
                var nodes = _.map(this.nodes, function(node, i) {
                    return {
                        x:        node.x,
                        y:        node.y,
                        px:       node.x,
                        py:       node.y,
                        index:    i,
                        node_obj: node, 
                        id:       node.id,
                        fixed:    false
                    };
                }.bind(this));

                var id_map = _.map(nodes, function(n) {
                    return n.node_obj.id;
                }.bind(this));

                var links = _.map(this.edges, function(edge) {
                    return {
                        source: id_map.indexOf(edge.source.id),
                        target: id_map.indexOf(edge.target.id)
                    }
                }.bind(this));

                var forceLayout = d3.layout.force();

                var tick = function() {
                    _.each(nodes, function(node) {
                        var gridX    = Math.round(node.x);
                        var gridY    = Math.round(node.y);
                        var distance = Math.min(1.0, forceLayout.alpha() * 10);

                        node.x = distance * node.x + (1 - distance) * gridX;
                        node.y = distance * node.y + (1 - distance) * gridY;
                    }.bind(this));
                }.bind(this);

                forceLayout = forceLayout
                    .nodes(nodes)
                    .links(links)
                    .on('tick', tick)
                    .charge(-0.5)
                    .linkDistance(4)
                    .linkStrength(0.6)
                    .size([20, 10]);

                for (var k=0; k<10; ++k) {
                    var n = 1000;

                    forceLayout.start();
                    for (var i = 0; i < n; ++i) {
                       forceLayout.tick();
                    }
                    forceLayout.stop();
                }

                return forceLayout.nodes();
            }.bind(this);
        },

        /**
         * Method: _getTreeLayoutAlgorithm
         *
         * Returns:
         *      The tree cluster layout algorithm supported by this graph.
         */
        _getTreeLayoutAlgorithm: function() {
            throw new Error("Tree Layout not supported.");
        },

        /**
         *  Method: _layoutWithAlgorithm
         *      Layouts the nodes of this graph with the given layouting algorithm. We override here because RBDs are
         *      layout horizontally (change x and y).
         *
         *  Returns:
         *      This {<Graph>} instance for chaining.
         */
        _layoutWithAlgorithm: function(algorithm) {
            // move to the upper border
            var layoutedNodes = algorithm();
            var minY          = _.min(layoutedNodes, function(node) { return node.y }).y;
            var offsetY       = 1 - minY;
            // center horizontally
            var centerX       = Math.floor((jQuery('#' + this.config.IDs.CANVAS).width() / this.config.Grid.SIZE) / 2);
            var minX          = _.min(layoutedNodes, function(node) { return node.x }).x;
            var maxX          = _.max(layoutedNodes, function(node) { return node.x }).x;
            var offsetX       = centerX - (minX + maxX) / 2;

            // apply positions
            _.each(layoutedNodes, function(n) {
                var node = this.getNodeById(n.id);

                node.moveToGrid({
                    x: n.x+offsetX,
                    y: n.y+offsetY
                }, false);
            }.bind(this));

            return this;
        }
    });
});