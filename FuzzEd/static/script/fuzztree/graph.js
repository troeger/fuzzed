define(['graph', 'fuzztree/node', 'fuzztree/config', 'json!notations/fuzztree.json'],
function(Graph, FuzztreeNode, FuzztreeConfig, FuzztreeNotation) {

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
