define(['graph', 'faulttree/node', 'faulttree/config', 'json!notations/faulttree.json'],
function(Graph, FaulttreeNode, FaulttreeConfig, FaulttreeNotation) {
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
            return FaulttreeConfig;
        },

        /**
         *  Method: getNodeClass
         *    See <Base::Graph::getNodeClass>.
         */
        getNodeClass: function() {
            return FaulttreeNode;
        },

        /**
         *  Method: getNotation
         *    See <Base::Graph::getNotation>.
         */
        getNotation: function() {
            return FaulttreeNotation;
        },

        // _clone's purpose is not to actually copy any properties, but to make the clone be in the same node group
        //    as the original, so they share common properties implicitly
        _clone: function(node) {
            var clone = this.addNode({
                kind: node.kind,
                x: node.x + 1,
                y: node.y + 1
            });

            // if the original node is not part of a NodeGroup yet, create a new one out of the node and the clone
            if (_.isEmpty(node.nodegroups)) {
                this.addNodeGroup({
                    nodeIds: [node.id, clone.id],
                    properties: node.toDict().properties
                });
            } else {
                // well this is a bit hacky now: in this special case we assume that the original node only has one
                //  nodegroup in its nodegroups-object, so we just get this one by using the first key of the object
                var key = Object.keys(node.nodegroups)[0];
                node.nodegroups[key].addNode(clone);
            }

            return clone;
        }
    });
});
