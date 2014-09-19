define(['factory', 'graph', 'rbd/node', 'json!notations/rbd.json'],
function(Factory, Graph, RbdNode, RbdNotation) {
    /**
     * Package: RBD
     */

    /**
     * Class: Graph
     *      RBD-specific graph.
     *
     * Extends <Base::Graph>.
     */
    return Graph.extend({

        /**
         *  Method: _getClusterLayoutAlgorithm
         *
         *  Returns:
         *      The cluster layout algorithm supported by this graph.
         */
        _getClusterLayoutAlgorithm: function() {
            return d3.layout.cluster()
                .nodeSize([2, 2]) // leave some space for the mirror
                .separation(function(a, b) {
                    // sibling nodes are tidier
                    return a.parent == b.parent ? 1 : 2;
                });
        },


        /**
         * Method: _getTreeLayoutAlgorithm
         *
         * Returns:
         *      The tree cluster layout algorithm supported by this graph.
         */
        _getTreeLayoutAlgorithm: function() {
            return d3.layout.tree()
                .nodeSize([2, 2]) // leave some space for the mirror
                .separation(function(a, b) {
                    // sibling nodes are tidier
                    return a.parent == b.parent ? 1 : 2;
                });
        },


        /**
         * Group: Graph manipulation
         */

        /**
         * Method: _layoutWithAlgorithm
         *      Layouts the nodes of this graph with the given layout algorithm. We overwrite here because RBDs are
         *      layout horizontally (change x and y).
         *
         *  Returns:
         *      This {<RBDGraph>} instance for chaining.
         */
        _layoutWithAlgorithm: function(algorithm) {
            var layoutedNodes = algorithm(this._getNodeHierarchy());
            var maxY          = _.max(layoutedNodes, function(n) {return n.y}).y;

            // try to center the graph on the canvas (if there's enough space)
            var centerX = Math.floor((jQuery('#' + Factory.getModule('Config').IDs.CANVAS).width() / Factory.getModule('Config').Grid.SIZE) / 2);
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
        }
    });
});
