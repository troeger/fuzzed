define(['editor', 'rbd/graph', 'rbd/config'], function(Editor, RbdGraph, Config) {
    /**
     * Class: RbdEditor
     */
    return Editor.extend({
        _graphClass: function() {
            return RbdGraph;
        },

        _setupJsPlumb: function() {
            this._super();

            jsPlumb.importDefaults({
                Connector: [Config.JSPlumb.CONNECTOR_STYLE, {stub: Config.JSPlumb.CONNECTOR_STUB}]
            });

            return this;
        }
    });
});
