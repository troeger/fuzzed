define(['faulttree/graph', 'fuzztree/node', 'fuzztree/config', 'json!notations/fuzztree.json'],
function(FaulttreeGraph, FuzztreeNode, FuzztreeConfig, FuzztreeNotation) {
    /**
     * Package: Fuzztree
     */

    /**
     * Class: Graph
     *      Fuzztree-specific graph.
     *
     * Extends: <Base::Graph>.
     */
    return FaulttreeGraph.extend({
        /**
         *  Group: Accessors
         */

        /**
         *  Method: getConfig
         *    See <Base::Graph::getConfig>.
         */
        getConfig: function() {
            return FuzztreeConfig;
        },

        getNodeClass: function() {
            return FuzztreeNode;
        },

        getNotation: function() {
            return FuzztreeNotation;
        }
    });
});
