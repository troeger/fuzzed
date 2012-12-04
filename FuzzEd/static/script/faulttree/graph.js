define(['graph', 'faulttree/node', 'json!notations/faulttree.json'], function(Graph, FaulttreeNode, FaulttreeNotation) {

    return Graph.extend({
        getNodeClass: function() {
            return FaulttreeNode;
        },

        getNotation: function() {
            return FaulttreeNotation;
        }
    });
});
