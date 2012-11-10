define(['config', 'node', 'backend', 'class', 'underscore'], function(Config, Nodes, Backend, Class) {

    /**
     * Class: Selection
     */
    var Selection = Class.extend({

        _nodes: [],         // node objects; not DOM elements
        _connections: [],   // jsPlumb Connection objects
        _editor: undefined, // being retrieved in the constructor

        init: function() {
            this._editor = jQuery('#' + Config.IDs.CANVAS).data(Config.Keys.EDITOR);
        },

        /* Section: API */

        /**
         * Method: clear
         *     Clear the selection, leaving the nodes on the canvas.
         */
        clear: function() {
            _.each(this._nodes, function(node) {
                node.deselect();
            });

            // reset connection and endpoint styles
            _.each(this._connections, function(connection) {
                connection.setPaintStyle({
                    strokeStyle: Config.JSPlumb.STROKE
                });
                connection.setHoverPaintStyle({
                    strokeStyle: Config.JSPlumb.STROKE_HIGHLIGHTED
                });

                _.each(connection.endpoints, function(endpoint) {
                    endpoint.setPaintStyle({
                        fillStyle: Config.JSPlumb.ENDPOINT_FILL
                    });
                })
            });

            this._empty();
            this._editor.properties.hide();

            return this;
        },

        contains: function(element) {
            return _.indexOf(this._nodes, element) >= 0 
                || _.indexOf(this._connections, element) >= 0;
        },

        /**
         * Method: ofNodes
         *     Make a new selection of the given node(s).
         *
         * Parameters:
         *     nodes - Nodes to be selected.
         */
        ofNodes: function(nodes) {
            this.clear();

            if (_.isArray(nodes)) {
                this._nodes = nodes;
            } else {
                this._nodes.push(nodes);
            }

            _.each(this._nodes, function(node) {
                node.select();
            });
            this._editor.properties.show(nodes);

            return this;
        },

        /**
         * Method: ofConnections
         *     Make a new selection of the given connection(s).
         *
         * Parameters:
         *     connections - Connections to be selected.
         */
        ofConnections: function(connections) {
            this.clear();

            if (_.isArray(connections)) {
                this._connections = connections;
            } else {
                this._connections.push(connections);
            }

            // mark connections and their endpoints as selected
            _.each(this._connections, function(connection) {
                connection.setPaintStyle({
                    strokeStyle: Config.JSPlumb.STROKE_SELECTED
                });
                connection.setHoverPaintStyle({
                    strokeStyle: Config.JSPlumb.STROKE_SELECTED
                });

                _.each(connection.endpoints, function(endpoint) {
                    endpoint.setPaintStyle({
                        fillStyle: Config.JSPlumb.STROKE_SELECTED
                    });
                })
            });

            return this;
        },

        /**
         * Method: remove
         *     Remove the current contained nodes from the canvas and clear the selection.
         */
        remove: function() {
            var containsTop = false;

            _.each(this._nodes, function(node) {
                //TODO: let node decide whether it can be removed
                if (!(node instanceof Nodes.TopEvent)) {
                    Backend.deleteNode(node);
                    node.graph().deleteNode(node);
                    node.remove();

                } else {
                    containsTop = true;
                }
            }.bind(this));

            _.each(this._connections, function(connection) {
                jsPlumb.detach(connection);
            });

            if (!containsTop) {
                this._empty();
                this._editor.properties.hide();
            }

            return this;
        },

        /* Section: Internal */

        _empty: function() {
            this._nodes = [];
            this._connections = [];
            return this;
        }
    });

    return Selection;
});