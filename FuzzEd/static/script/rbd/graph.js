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
        }
    });
});
