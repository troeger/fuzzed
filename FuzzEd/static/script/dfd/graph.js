define(['graph', 'dfd/node', 'dfd/config', 'json!notations/dfd.json'],
function(Graph, DfdNode, DfdConfig, DfdNotation) {
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
         *  Group: Accessors
         */

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
        }
    });
});