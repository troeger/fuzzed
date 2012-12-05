define(['graph', 'rbd/node', 'json!notations/rbd.json'], function(Graph, RbdNode, RbdNotation) {

    return Graph.extend({
        getNodeClass: function() {
            return RbdNode;
        },

        getNotation: function() {
            return RbdNotation;
        }
    });
});
