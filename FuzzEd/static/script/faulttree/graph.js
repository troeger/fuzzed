define(['graph', 'faulttree/node', 'faulttree/config', 'json!notations/faulttree.json'],
function(Graph, FaulttreeNode, FaulttreeConfig, FaulttreeNotation) {

    return Graph.extend({
        getConfig: function() {
            return FaulttreeConfig;
        },

        getNodeClass: function() {
            return FaulttreeNode;
        },

        getNotation: function() {
            return FaulttreeNotation;
        }
    });
});
