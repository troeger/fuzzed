define(['editor', 'rbd/graph', 'rbd/config'], function(Editor, RbdGraph, RbdConfig) {
    /**
     * Class: RbdEditor
     */
    return Editor.extend({
        getConfig: function() {
            return RbdConfig;
        },

        getGraphClass: function() {
            return RbdGraph;
        }
    });
});
