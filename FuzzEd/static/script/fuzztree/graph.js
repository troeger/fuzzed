define(['graph', 'fuzztree/node', 'fuzztree/config', 'json!notations/fuzztree.json'],
function(Graph, FuzztreeNode, FuzztreeConfig, FuzztreeNotation) {
    /**
     * Package: Fuzztree
     */

    /**
     * Class: Graph
     *      Fuzztree-specific graph.
     *
     * Extends: <Base::Graph>.
     */
    return Graph.extend({
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
