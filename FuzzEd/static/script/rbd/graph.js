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
         *  Method: _getLayoutAlgorithms
         *    Returns the layouting algorithms supported by this graph.
         *
         *  Returns:
         *    An array containing algorithm descriptions. Those descriptions should contain the algorithm itself
         *    (taken from d3.js), a class for the toolbar icon and a tooltip text.
         */
        _getLayoutAlgorithms: function() {
            var clusterLayout = d3.layout.cluster()
                .nodeSize([2, 2]) // leave some space for the mirror
                .separation(function(a, b) {
                    // sibling nodes are tidier
                    return a.parent == b.parent ? 1 : 2;
                });

            var treeLayout =  d3.layout.tree()
                .nodeSize([2, 2]) // leave some space for the mirror
                .separation(function(a, b) {
                    // sibling nodes are tidier
                    return a.parent == b.parent ? 1 : 2;
                });

            return [
                {
                    algorithm: clusterLayout,
                    iconClass: this.config.Classes.ICON_LAYOUT_CLUSTER,
                    tooltip:   this.config.Tooltips.LAYOUT_CLUSTER
                }, {
                    algorithm: treeLayout,
                    iconClass: this.config.Classes.ICON_LAYOUT_TREE,
                    tooltip:   this.config.Tooltips.LAYOUT_TREE
                }
            ];
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
                node.moveToGrid({x: n.y + offsetX + 1, y: n.x + 1});
            }.bind(this));

            return this;
        },
    });
});
