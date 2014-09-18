define(['factory', 'graph', 'faulttree/node', 'faulttree/config', 'json!notations/faulttree.json'],
function(Factory, Graph, FaulttreeNode, FaulttreeConfig, FaulttreeNotation) {
    /**
     * Package: Faulttree
     */

    /**
     * Class: Graph
     *      Faulttree-specific graph.
     *
     * Extends <Base::Graph>.
     */
    return Graph.extend({
        /**
         * Group: Accessors
         */

        // _mirror's purpose is not to actually copy any properties, but to make the mirrored node be in the same node
        //     group as the original, so they share common properties implicitly
        _mirror: function(node) {
            var mirroredNode = this.addNode({
                kind: node.kind,
                x: node.x + 1,
                y: node.y + 1
            });

            // if the original node is not part of a NodeGroup yet, create a new one out of the node and the mirrored node
            if (_.isEmpty(node.nodegroups)) {
                this.addNodeGroup({
                    nodeIds: [node.id, mirroredNode.id],
                    properties: node.toDict().properties
                });
            } else {
                // well this is a bit hacky now: in this special case we assume that the original node only has one
                //  nodegroup in its nodegroups-object, so we just get this one by using the first key of the object
                var key = Object.keys(node.nodegroups)[0];
                node.nodegroups[key].addNode(mirroredNode);
            }

            return mirroredNode;
        }
    });
});
