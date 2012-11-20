define(['config', 'class'], function(Config, Class) {

    return Class.extend({
        id:     undefined,
        edges:  {},
        nodes:  {},
        name:   undefined,

        _nodeClasses: {},

        init: function(json) {
            this.id   = json.id;
            this.name = json.name;

            this._nodeClasses['node'] = this._nodeClass();
            this._loadFromJson(json)
                ._registerEventHandlers();
        },

        /*
         Function: addEdge
            Adds a given edge to this graph.

         Parameters:
            edge - Edge to be added
         */
        addEdge: function(edge) {
            var connection = edge.connection;
            var fuzzedId = new Date().getTime() + 1;

            connection._fuzzedID = fuzzedId;
            jQuery(document).trigger(
                Config.Events.GRAPH_EDGE_ADDED,
                fuzzedId,
                edge.source.data(Config.Keys.NODE),
                edge.target.data(Config.Keys.NODE)
            );
            this.edges[fuzzedId] = connection;

            return this;
        },

        /*
         Function: deleteEdge
            Deletes the given edges from the graph if present

         Parameters:
            edge - Edge to remove from this graph.
         */
        deleteEdge: function(edge) {
            var id = edge.connection._fuzzedID;

            Backend.deleteEdge(connection);
            jQuery(document).trigger(Config.Events.GRAPH_EDGE_DELETED, id);
            delete this._edges[id];

            return this;
        },

        /*
         Function: addNode
            Adds a given node to this graph.

         Parameters:
            kind       - String naming the kind of the node, e.g., 'basicEvent'.
            properties - Properties that should be merged into the new node.
         */
        addNode: function(kind, properties) {
            var node = new (this.nodeClassFor(kind))(this, properties);
            jQuery(document).trigger(Config.Events.GRAPH_NODE_ADDED, node.id);
            this.nodes[node.id] = node;

            return node;
        },

        /*
         Function: deleteNode
         Deletes the given node from the graph if present

         Parameters:
         node - Node to remove from this graph.
         */
        deleteNode: function(nodeId) {
            jQuery(document).trigger(Config.Events.GRAPH_NODE_DELETED, nodeId);
            delete this._nodes[nodeId];

            return this;
        },

        /*
         Function: nodeClassFor
         Returns the class for the given kind. If the class does not yet exist it is created from the notation
         definition. It is an error if the given node kind does not exist in the notation.

         Parameter:
         kind - String specifying the kind of the node class to be retrieved.

         Returns:
         The class for the given kind identifier.
         */
        nodeClassFor: function(kind) {
            var nodeClass = this._nodeClasses[kind];

            if (typeof nodeClass !== 'undefined') return nodeClass;

            var notationDefinition = this._notation().nodes[kind];
            if (typeof notationDefinition === 'undefined')
                throw 'No definition for node of kind ' + kind;

            return this._newNodeClassForKind(notationDefinition);
        },

        /* Section: Internal */

        _newNodeClassForKind: function(definition) {
            var BaseClass = this._nodeClasses['node'];
            var inherits = definition.inherits;

            if (inherits) {
                var BaseClass = this.nodeClassFor(inherits);
            }

            var newClass = BaseClass.extend({
                init: function(properties) {
                    this._super(jQuery.extend(true, definition, properties));
                }
            });

            this._nodeClasses[definition.kind] = newClass;

            return newClass;
        },

        _loadFromJson: function(json) {
            // parse the json nodes and convert them to node objects
            _.each(json.nodes, function(jsonNode) {
                this.addNode(jsonNode.kind, jsonNode);
            }.bind(this));

            // connect the nodes again
            _.each(json.edges, function(jsonEdge) {
                var edge = jsPlumb.connect({
                    source: graph.getNodeById(jsonEdge.source).container(),
                    target: graph.getNodeById(jsonEdge.target).container()
                });
                edge._fuzzedID = jsonEdge.id;
                graph.addEdge(edge);

            }.bind(this));

            return this;
        },

        _nodeClass: function() {
            throw '[ABSTRACT] Subclass responsibility';
        },

        _notation: function() {
            throw '[ABSTRACT] Subclass responsibility';
        },

        _registerEventHandlers: function() {
            jsPlumb.bind('jsPlumbConnection', this.addEdge.bind(this));
            jsPlumb.bind('jsPlumbConnectionDetached', this.deleteEdge.bind(this));
            jQuery(document).on(Config.Events.CANVAS_SHAPE_DROPPED, this._shapeDropped.bind(this));
        },

        _shapeDropped: function(kind, position) {
            var node = this.addNode(kind)
                           .moveTo(position);

            //TODO: move
            this.selection.ofNodes(node);
        }
    });
});