define(['node_group', 'config'], function(NodeGroup, Config) {

    /**
     * Package: Faulttree
     */

    /**
     * Class: FaulttreeNodeGroup
     *
     * Extends: <Base::NodeGroup>
     */
    return NodeGroup.extend({
        _setupVisualRepresentation: function() {
            return this;
        },
        redraw: function() {
            return this;
        },
        _setupDragging: function() {
            return this;
        },
        _setupMouse: function() {
            return this;
        },
        _setupSelection: function() {
            return this;
        },
        remove: function() {
            if (!this.deletable) return false;

            // unaffect all currently affected nodes (you know, the purple ones)
            _.each(this.nodes, function(node) {
                node.unaffect();
            }.bind(this));

            // don't listen anymore
            jQuery(document).off([ Config.Events.NODES_MOVED,
                                   Config.Events.NODE_PROPERTY_CHANGED ].join(' '), this.redraw.bind(this));

            // call home
            jQuery(document).trigger(Config.Events.NODEGROUP_DELETED, [this.id, this.nodeIds()]);

            return true;
        },
    });
});
