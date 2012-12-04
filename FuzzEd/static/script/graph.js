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

            // store the ID in an attribute so we can retrieve it later from the DOM element
            jQuery(edge.canvas).attr(Config.Keys.CONNECTION_ID, edge._fuzzedId);

            var sourceNode = edge.source.data(Config.Keys.NODE);
            var targetNode = edge.target.data(Config.Keys.NODE);

            jQuery(document).trigger(
                Config.Events.GRAPH_EDGE_ADDED,
                [edge._fuzzedId,
                sourceNode.id,
                targetNode.id]
            );
            this.edges[edge._fuzzedId] = edge;

            sourceNode.outgoingEdges.push(edge);
            targetNode.incomingEdges.push(edge);

            return this;
        },

        /*
         Function: deleteEdge
            Deletes the given edges from the graph if present

         Parameters:
            edge - Edge to remove from this graph.
         */
        deleteEdge: function(edge) {
            var id         = edge._fuzzedId;
            var sourceNode = edge.source.data(Config.Keys.NODE);
            var targetNode = edge.target.data(Config.Keys.NODE);

            sourceNode.outgoingEdges = _.without(sourceNode.outgoingEdges, edge);
            targetNode.incomingEdges = _.without(targetNode.incomingEdges, edge);

            jQuery(document).trigger(Config.Events.GRAPH_EDGE_DELETED, id);
            delete this.edges[id];

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
            var node = this.nodes[nodeId];
            if (node.deletable === false) return this;

            _.each(_.union(node.incomingEdges, node.outgoingEdges), function(edge) {
                this.deleteEdge(edge);
            }.bind(this));

            jQuery(document).trigger(Config.Events.GRAPH_NODE_DELETED, nodeId);

            node.remove();
            delete this.nodes[nodeId];

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

        getEdgeById: function(edgeId) {
            return this.edges[edgeId];
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

            jQuery(document).on(Config.Events.CANVAS_SHAPE_DROPPED,   this._shapeDropped.bind(this));

            jQuery(document).on(Config.Events.CANVAS_EDGE_SELECTED,   this._edgeSelected.bind(this));
            jQuery(document).on(Config.Events.CANVAS_EDGE_UNSELECTED, this._edgeUnselected.bind(this));
        },

        _shapeDropped: function(event, kind, position) {
            var node = this.addNode(kind, Canvas.toGrid(position));

            //TODO: select the node
        },

        _edgeSelected: function(event, edgeId) {
            var edge = this.getEdgeById(edgeId);
            //XXX: Normally we could use jsPlumb's 'Connection Type' mechanism which allows the definition of
            //     different styles and toggeling between them. Unfortunately this causes the connector to get
            //     completely redrawn (replace DOM element) which prevents us from associating it with the connection
            //     object (via DOM attribute). So we need to toggle the styles manually for the moment.
            edge.setPaintStyle({
                strokeStyle: Config.JSPlumb.STROKE_COLOR_SELECTED,
                lineWidth:   Config.JSPlumb.STROKE_WIDTH
            });
            edge.setHoverPaintStyle({
                strokeStyle: Config.JSPlumb.STROKE_COLOR_SELECTED,
                lineWidth:   Config.JSPlumb.STROKE_WIDTH
            });
        },

        _edgeUnselected: function(event, edgeId) {
            var edge = this.getEdgeById(edgeId);
            edge.setPaintStyle({
                strokeStyle: Config.JSPlumb.STROKE_COLOR,
                lineWidth:   Config.JSPlumb.STROKE_WIDTH
            });
            edge.setHoverPaintStyle({
                strokeStyle: Config.JSPlumb.STROKE_COLOR_HIGHLIGHTED,
                lineWidth:   Config.JSPlumb.STROKE_WIDTH
            });
        }
    });
});