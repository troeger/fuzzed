define(['graph', 'rbd/node', 'rbd/config', 'json!notations/rbd.json'],
function(Graph, RbdNode, RbdConfig, RbdNotation) {

    return Graph.extend({
        getConfig: function() {
            return RbdConfig;
        },

        getNodeClass: function() {
            return RbdNode;
        },

        getNotation: function() {
            return RbdNotation;
        }
    });
});
