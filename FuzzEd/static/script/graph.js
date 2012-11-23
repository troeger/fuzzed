define(['canvas', 'config', 'class'], function(Canvas, Config, Class) {

    return Class.extend({
        id:     undefined,
        edges:  {},
        nodes:  {},
        name:   undefined,

        _nodeClasses: {},

        init: function(json) {
            this.id   = json.id;
            this.name = json.name;

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
            if (typeof edge._fuzzedId === 'undefined') {
                edge._fuzzedId = new Date().getTime() + 1;
            }

            jQuery(document).trigger(
                Config.Events.GRAPH_EDGE_ADDED,
                [edge._fuzzedId,
                edge.source.data(Config.Keys.NODE).id,
                edge.target.data(Config.Keys.NODE).id]
            );
            this.edges[edge._fuzzedId] = edge;

            return this;
        },

        /*
         Function: deleteEdge
            Deletes the given edges from the graph if present

         Parameters:
            edge - Edge to remove from this graph.
         */
        deleteEdge: function(edge) {
            var id = edge.connection._fuzzedId;

            jQuery(document).trigger(Config.Events.GRAPH_EDGE_DELETED, id);
            delete this._edges[id];

            return this;
        },

        /*
         Function: addNode
            Adds a given node to this graph.

         Parameters:
            kind       - String naming the kind of the node, e.g., 'basicEvent'.
            properties - [optional] Properties that should be merged into the new node.
         */
        addNode: function(kind, properties, success) {
            var node = new (this.nodeClassFor(kind))(properties, this.getNotation().propertiesDisplayOrder);
            jQuery(document).trigger(Config.Events.GRAPH_NODE_ADDED, [node.id, kind, node.x, node.y]);
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

            this._nodes[nodeId].remove();
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

            var notationDefinition = this.getNotation().nodes[kind];
            if (typeof notationDefinition === 'undefined')
                throw 'No definition for node of kind ' + kind;

            notationDefinition.kind = kind;

            return this._newNodeClassForKind(notationDefinition);
        },

        getNotation: function() {
            throw '[ABSTRACT] Subclass responsibility';
        },

        getNodeClass: function() {
            throw '[ABSTRACT] Subclass responsibility';
        },

        getNodes: function() {
            return _.values(this._nodes);
        },

        getNodeById: function(nodeId) {
            return this.nodes[nodeId];
        },

        /* Section: Internal */

        _newNodeClassForKind: function(definition) {
            var BaseClass = this.getNodeClass();
            var inherits = definition.inherits;

            if (inherits) {
                var BaseClass = this.nodeClassFor(inherits);
            }

            var newClass = BaseClass.extend({
                init: function(properties, propertiesDisplayOrder) {
                    this._super(jQuery.extend(true, {}, definition, properties), propertiesDisplayOrder);
                }
            });

            this._nodeClasses[definition.kind] = newClass;

            // replace the node kind strings in the allowConnection field with actual classes
            // this allows for instanceof checks later
            _.each(definition.allowConnectionTo, function(kind, index) {
                definition.allowConnectionTo[index] = this.nodeClassFor(kind);
            }.bind(this));

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
                    source: this.getNodeById(jsonEdge.source).container,
                    target: this.getNodeById(jsonEdge.target).container
                });
                edge._fuzzedId = jsonEdge.id;
                this.addEdge(edge);

            }.bind(this));

            return this;
        },

        _registerEventHandlers: function() {
            jsPlumb.bind('jsPlumbConnection', function(edge) {
                this.addEdge(edge.connection);
            }.bind(this));
            jsPlumb.bind('jsPlumbConnectionDetached', function(edge) {
                this.deleteEdge(edge.connection);
            }.bind(this));
            jQuery(document).on(Config.Events.CANVAS_SHAPE_DROPPED, this._shapeDropped.bind(this));
        },

        _shapeDropped: function(event, kind, position) {
            var node = this.addNode(kind, Canvas.toGrid(position));

            //TODO: select the node
        }
    });
});