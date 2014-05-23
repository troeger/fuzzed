define(['graph', 'faulttree/node', 'faulttree/config', 'json!notations/faulttree.json'],
function(Graph, FaulttreeNode, FaulttreeConfig, FaulttreeNotation) {
    /**
     * Package: Faulttree
     */

    /**
     * Class: Graph
     *      Faulttree-specific graph.
     *
     * Extends <Base::Graph>.
     */
    return Graph.extend({
        /**
         * Group: Accessors
         */

        /**
         * Method: getConfig
         *      See <Base::Graph::getConfig>.
         */
        getConfig: function() {
            return FaulttreeConfig;
        },

        /**
         * Method: getNodeClass
         *      See <Base::Graph::getNodeClass>.
         */
        getNodeClass: function() {
            return FaulttreeNode;
        },

        /**
         * Method: getNotation
         *      See <Base::Graph::getNotation>.
         */
        getNotation: function() {
            return FaulttreeNotation;
        }
    });
});
