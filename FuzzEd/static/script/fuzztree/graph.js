define(['graph', 'fuzztree/node', 'json!notations/fuzztree.json'], function(Graph, FuzztreeNode, FuzztreeNotation) {

    return Graph.extend({
        getNodeClass: function() {
            return FuzztreeNode;
        },

        getNotation: function() {
            return FuzztreeNotation;
        }
    });
});
