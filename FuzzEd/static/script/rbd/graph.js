define(['graph', 'rbd/node', 'rbd/config', 'json!notations/rbd.json'],
function(Graph, RbdNode, RbdConfig, RbdNotation) {
    /**
     *  Package: RBD
     */

    /**
     *  Class: Graph
     *    RBD-specific graph. Extends <Base::Graph>.
     */
    return Graph.extend({
        /**
         *  Group: Accessors
         */

        /**
         *  Method: getConfig
         *    See <Base::Graph::getConfig>.
         */
        getConfig: function() {
            return RbdConfig;
        },

        /**
         *  Method: getNodeClass
         *    See <Base::Graph::getNodeClass>.
         */
        getNodeClass: function() {
            return RbdNode;
        },

        /**
         *  Method: getNotation
         *    See <Base::Graph::getNotation>.
         */
        getNotation: function() {
            return RbdNotation;
        },

        /**
         *  Method: _getClusterLayoutAlgorithm
         *    Returns the cluster layouting algorithm supported by this graph.
         */
        _getClusterLayoutAlgorithm: function() {
            var clusterLayout = d3.layout.cluster()
                .nodeSize([2, 2]) // leave some space for the mirror
                .separation(function(a, b) {
                    // sibling nodes are tidier
                    return a.parent == b.parent ? 1 : 2;
                });

            return clusterLayout;
        },


        /**
         *  Method: _getTreeLayoutAlgorithm
         *    Returns the tree cluster layouting algorithm supported by this graph.
         */
        _getTreeLayoutAlgorithm: function() {
            var treeLayout =  d3.layout.tree()
                .nodeSize([2, 2]) // leave some space for the mirror
                .separation(function(a, b) {
                    // sibling nodes are tidier
                    return a.parent == b.parent ? 1 : 2;
                });

            return treeLayout;
        },


        /**
         *  Group: Graph manipulation
         */

        /**
         *  Method: _layoutWithAlgorithm
         *    Layouts the nodes of this graph with the given layouting algorithm.
         *    We overwrite here because RBDs are layouted horizontally (change x and y).
         *
         *  Returns:
         *    This <Graph> instance for chaining.
         */
        _layoutWithAlgorithm: function(algorithm) {
            var layoutedNodes = algorithm(this._getNodeHierarchy());

            var maxY = _.max(layoutedNodes, function(n) {return n.y}).y;
            // try to center the graph on the canvas (if there's enough space)
            var centerX = Math.floor((jQuery('#' + this.config.IDs.CANVAS).width() / this.config.Grid.SIZE) / 2);
            var offsetX = Math.max(centerX - (maxY / 2), 0);

            // apply positions
            _.each(layoutedNodes, function(n) {
                var node = this.getNodeById(n.id);
                // +1 because the returned coords are 0-based and we need 1-based
                //TODO: layouting RBDs can't be animated for the moment because they are no real trees which means
                //      that the animated will be triggered multiple times on some nodes which causes strange effects
                node.moveToGrid({x: n.y + offsetX + 1, y: n.x + 1}, false);
            }.bind(this));

            return this;
        },
    });
});
