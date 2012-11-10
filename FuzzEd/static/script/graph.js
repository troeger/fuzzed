define(['config', 'class'], function(Config, Class) {

    var Graph = Class.extend({
        id:     undefined,
        edges:  {},
        nodes:  {},
        name:   undefined,

        _nodeClasses: {},

        init: function(json) {
            this.id   = json.id;
            this.name = json.name;

            this._nodeClasses['node'] = this._nodeClass();
            this._loadFromJson(json);
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
            Backend.addEdge(fuzzedId, edge.source.data(Config.Keys.NODE), edge.target.data(Config.Keys.NODE));
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
            var connection = edge.connection;

            Backend.deleteEdge(connection);
            delete this._edges[connection._fuzzedID];

            return this;
        },

        /*
         Function: addNode
         Adds a given node to this graph.

         Parameters:
         node - Node to add to this graph.
         */
        addNode: function(kind, properties) {
            var node = new (this.nodeClassFor(kind))(this, properties);
            this.nodes[node.id] = node;

            return node;
        },

        newNodeClassForKind: function(definition) {
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

            return this.newNodeClassForKind(notationDefinition);
        },

        /* Section: Internal */

        _loadFromJson: function(json) {
            // parse the json nodes and convert them to node objects
            _.each(json.nodes, function(jsonNode) {
                this.addNode(jsonNode.kind, jsonNode);
            }.bind(this));

            //TODO: put into DOM

            // connect the nodes again
            _.each(json.edges, function(jsonEdge) {
                var edge = jsPlumb.connect({
                    source: graph.getNodeById(jsonEdge.source).container(),
                    target: graph.getNodeById(jsonEdge.target).container()
                });
                edge._fuzzedID = jsonEdge.id;
                graph.addEdge(edge);

            }.bind(this));

            this._setupJsPlumbEvents().bind(this);
        },

        _nodeClass: function() {
            throw '[ABSTRACT] Subclass responsibility';
        },

        _notation: function() {
            throw '[ABSTRACT] Subclass responsibility';
        },

        _setupJsPlumbEvents: function() {
            jsPlumb.bind('jsPlumbConnection', this.addEdge.bind(this));
            jsPlumb.bind('jsPlumbConnectionDetached', this.deleteEdge.bind(this));
        },

        /*
         Function: deleteNode
         Deletes the given node from the graph if present

         Parameters:
         node - Node to remove from this graph.
         */
        deleteNode: function(node) {
            delete this._nodes[node.id]
        },

        getNodeById: function(id) {
            return this._nodes[id];
        },

        /*
         Function: getNodes
         Get all the nodes of the graph.
         */
        getNodes: function() {
            return _.values(this._nodes);
        }
    });

    return Graph;
});