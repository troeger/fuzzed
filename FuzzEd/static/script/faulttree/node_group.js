define(['node_group'], function(NodeGroup) {

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
            console.log("hallo");
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
        }
    });
});
