define(['config', 'class'], function(Config, Class) {

    var Graph = Class.extend({
        init: function(kind, id) {
            this.id           = id;
            this._nodeClasses = {};
            this._nodes       = {};
            this._edges       = {};

            // load base class corresponding to graph kind and register it
            this._nodeClasses['node'] = require(kind + '-node');
            // fetch the notation json file
            this._notation = require('json!notations/' + kind);
        },

        /**
         *
         * Section: Factories
         */

        /*
         Function: newNodeOfKind
         Returns a new Node of the given kind identifier.

         Parameter:
         kind - String specifying the kind of the new Node. See Config.Node.Kinds.
         properties - [optional] A dictionary of properties that should be merged into the new node.

         Returns:
         A new Node of the given kind
         */
        newNodeOfKind: function(kind, properties) {
            return new (this.nodeClassFor(kind))(properties);
        },

        newNodeClassForKind: function(definition) {
            var BaseClass = this._nodeClasses['node'];
            var inherits = definition.inherits;

            if (inherits) {
                var BaseClass = this.nodeClassFor(inherits);
            }

            var newClass = BaseClass.extend(definition);

            jQuery.extend(true, newClass, definition);
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

            var notationDefinition = this._notation.nodes[kind];
            if (typeof notationDefinition === 'undefined')
                throw 'No definition for node of kind ' + kind;

            return this.newNodeClassForKind(notationDefinition);
        },

        /*
         Function: newNodeFromJson
         Factory method. Returns a new Node defined by the given JSON.

         Parameter:
         json - A JSON object defining the properties of the new node..
         The node's class is determined using the 'kind' property.
         Default kind is 'node'.

         Returns:
         A new Node.
         */
        newNodeFromJson: function(json) {
            var kind = json.kind || 'node';
            var nodeClass = nodeKindToClassMapping[kind];
            // the init method will merge the json attributes into the new node
            return new nodeClass(json);
        },


        /*
         Function: addEdge
         Adds a given edge to this graph.

         Parameters:
         edge - Edge to be added
         */
        addEdge: function(edge) {
            this._edges[edge.id] = edge;
        },

        /*
         Function: addNode
         Adds a given node to this graph.

         Parameters:
         node - Node to add to this graph.
         */
        addNode: function(node) {
            node.graph(this);
            this._nodes[node.id] = node;
        },

        /*
         Function: deleteEdge
         Deletes the given edges from the graph if present

         Parameters:
         edge - Edge to remove from this graph.
         */
        deleteEdge: function(edge) {
            delete this._edges[edge.id];
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
