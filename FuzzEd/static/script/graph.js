define(['canvas', 'class', 'config', 'edge', 'menus', 'node_group', 'faulttree/node_group', 'jquery', 'd3'],
function(Canvas, Class, Config, Edge, Menus, NodeGroup, FaulttreeNodeGroup) {
    /**
     * Package: Base
     */

    /**
     * Class: Graph
     *      This class models the _abstract_ base class for all graphs. It manages all graph elements (<Edges> and
     *      <Nodes>) and provide methods for adding and deleting them. Further it can generate <Node> classes for given
     *      kinds of nodes.
     */
    return Class.extend({
        /**
         * Group: Members
         *      {Config}  config      - An object containing graph configuration constants as found in <Config>.
         *      {Number}  id          - A server-side generated ID.
         *      {Object}  edges       - A map that stores all edges of the graph by their ID. Edges are jsPlumb
         *                              Connection objects, the ID is the _fuzzedId assigned to them.
         *      {Object}  nodes       - A map that stores all <Nodes> of the graph by their ID.
         *      {String}  name        - The name of the graph, specified by the user when creating it.
         *      {Object} _nodeClasses - A map caching all node classes already generated and storing them by their kind.
         */
        config:       undefined,
        id:           undefined,
        edges:        {},
        nodes:        {},
        nodeGroups:   {},
        name:         undefined,
        readOnly:     undefined,
        seed:         undefined,

        _nodeClasses: {},

        /**
         * Group: Initialization
         */

        /**
         * Constructor: init
         *
         * Parameters:
         *      {Object} json - The JSON representation of the graph. This is usually fetched from the backend and used
         *                      to restore the graph in the frontend.
         */
        init: function(json) {
            this.id     = json.id;
            this.name   = json.name;
            this.seed   = json.seed;
            this.config = this.getConfig();

            this._loadFromJson(json)
                ._registerEventHandlers();
        },

        /**
         * Method: _loadFromJson
         *      Extracts and restores the <Nodes> and edges from the given JSON representation of the graph.
         *
         * Parameters:
         *      {Object} json - The JSON representation of the graph, containing nodes and edges.
         *
         * Returns:
         *      This <Graph> instance for chaining.
         */
        _loadFromJson: function(json) {
            this.kind     = json.type;
            this.readOnly = json.readOnly;

            var maxX = 0;
            var maxY = 0;

            // parse the json nodes and convert them to node objects
            _.each(json.nodes, function(jsonNode) {
                this.addNode(jsonNode);
            }.bind(this));

            // connect the nodes again
            _.each(json.edges, function(jsonEdge) {
                this.addEdge(jsonEdge);
            }.bind(this));

            // create nodeGroups
            _.each(json.nodeGroups, function(jsonNodeGroup) {
                this.addNodeGroup(jsonNodeGroup);
            }.bind(this));

            return this;
        },

        /**
         * Method: _registerEventHandlers
         *      Register on <Canvas> events in order to recognize shape drops and register to jsPlumb events in order
         *      to recognize connection events. This should be done _after_ the initial graph loading from the backend
         *      to avoid the creation of duplicate nodes/edges.
         *
         * On:
         *      <Config::Events::CANVAS_SHAPE_DROPPED>
         *
         * Returns:
         *      This <Graph> instance for chaining.
         */
        _registerEventHandlers: function() {
            jsPlumb.bind('connection', function(edge) {
                this._addEdge(edge.connection);
            }.bind(this));

            jQuery(document).on(Config.Events.CANVAS_SHAPE_DROPPED, this._shapeDropped.bind(this));

            return this;
        },

        /**
         * Group: Graph manipulation
         */

        /**
         * Method: addEdge
         *      Adds a given edge to this graph by "jsPlumb.connect"ing source and target node as if it was done
         *      manually. Only use this method if an edge needs to be added programatically and not manually. Manual
         *      creation of an edge (i.e. connect-dragging nodes in the editor) is done by jsPlumbConnection event,
         *      which calls _addEdge directly.
         *
         * Parameters:
         *      {Object} jsonEdge - JSON representation of the edge to be added to the graph.
         *
         * Returns:
         *      The newly created {<Edge>} instance.
         */
        addEdge: function(jsonEdge) {
            var sourceNode = this.getNodeById(jsonEdge.source);
            var targetNode = this.getNodeById(jsonEdge.target);

            // check if source's max number of outgoing connections is already reached
            if (sourceNode.numberOfOutgoingConnections != -1) { // -1 means infinite connections possible
                if (sourceNode.outgoingEdges.length >= sourceNode.numberOfOutgoingConnections) return false;
            }

            // check if target's max number of incoming connections is already reached
            if (targetNode.numberOfIncomingConnections != -1) { // -1 means infinite connections possible
                if (targetNode.incomingEdges.length >= targetNode.numberOfIncomingConnections) return false;
            }

            var properties = jsonEdge.properties || {};
            properties.id  = jsonEdge.id;
            properties.graph = this;

            var edge = this.factory.create('Edge', this.getNotation().edges, sourceNode, targetNode, properties);
            this.edges[edge.id] = edge;

            return edge;
        },

        /**
         * Method: _addEdge
         *      Actual register of a new edge in the graph object and call home via backend.
         *
         * Parameters:
         *      {jsPlumb::Connection} jsPlumbEdge - Edge to be added to the graph object. jsPlumbEdge has to be already
         *                                          jsPlumb.connected. If you want to add an edge programmatically, use
         *                                          <Graph::addEdge> instead.
         *
         * Triggers:
         *      <Config::Events::EDGE_ADDED>
         *
         *  Returns:
         *      The newly created {<Edge>} instance.
         */
        _addEdge: function(jsPlumbEdge) {
            var edge = this.factory.create('Edge', this.getNotation().edges, jsPlumbEdge, {graph: this});
            this.edges[edge.id] = edge;

            return edge;
        },

        /**
         * Method: deleteEdge
         *      Deletes a given edge from this graph. Calls jsPlumb.detach, which calls _deleteEdge. Functionality is
         *      split into deleteEdge and _deleteEdge as in addEdge.
         *
         * Parameters:
         *      {<Edge>} edge - Edge to be deleted from the graph.
         *
         * Returns:
         *      This {<Graph>} instance for chaining.
         */
        deleteEdge: function(edge) {
            if (edge.remove()) {
                delete this.edges[edge.id];
            }

            return this;
        },

        /**
         * Method: addNode
         *      Adds a given node to this graph.
         *
         * Parameters:
         *      {Object} definition - Properties that should be merged into the new node.
         *
         * Triggers:
         *      <Config::Events::NODE_ADDED>
         *
         * Returns:
         *      The added {<Node>} instance.
         */
        addNode: function(definition) {
            definition.readOnly = this.readOnly;
            definition.graph    = this;

            var node = new (this.nodeClassFor(definition.kind))(this.factory, definition);
            this.nodes[node.id] = node;

            return node;
        },

        /**
         * Method: deleteNode
         *      Deletes the given node from the graph if present.
         *
         * Parameters:
         *      {Number} nodeId - ID of the <Node> that should be removed from this graph.
         *
         * Returns:
         *      This {<Graph>} instance for chaining.
         */
        deleteNode: function(node) {
            if (node.remove()) {
                delete this.nodes[node.id];
            }

            return this;
        },

        /**
         * Method: addNodeGroup
         *      Creates a new NodeGroup based on the given JSON representation.
         *
         *  Returns:
         *    The newly created <NodeGroup> instance if successful.
         */
        addNodeGroup: function(jsonNodeGroup) {
            // first let's check if we already have a NodeGroup with the requested nodeIds
            var jngNodeIds = jsonNodeGroup.nodeIds;

            var alreadyExisting = false;
            _.each(this.nodeGroups, function(ng) {
                // math recap: two sets are equal, when both their differences are zero length
                if (jQuery(jngNodeIds).not(ng.nodeIds()).length == 0 && jQuery(ng.nodeIds()).not(jngNodeIds).length == 0) {
                    alreadyExisting = true;
                }
            }.bind(this));

            if (alreadyExisting) return;

            var nodes = {};
            _.each(jsonNodeGroup.nodeIds, function(nodeId) {
                nodes[nodeId] = this.getNodeById(nodeId);
            }.bind(this));

            var properties = jsonNodeGroup.properties || {};
            properties.id  = jsonNodeGroup.id;
            properties.graph = this;

            var nodeGroup = this.factory.create('NodeGroup', this.getNotation().nodeGroups, nodes, properties);
            this.nodeGroups[nodeGroup.id] = nodeGroup;
        },

        /**
         * Method: deleteNodeGroup
         *      Deletes a given {<NodeGroup>} instance.
         *
         * Returns:
         *      This {<Graph>} instance for chaining.
         */
        deleteNodeGroup: function(nodeGroup) {
            if (nodeGroup.remove()) {
                delete this.nodeGroups[nodeGroup.id];
            }

            return this;
        },

        /**
         *  Method: _layoutWithAlgorithm
         *    Layouts the nodes of this graph with the given layouting algorithm.
         *
         * Returns:
         *      This {<Graph>} instance for chaining.
         */
        _layoutWithAlgorithm: function(algorithm) {
            jQuery(document).trigger(Config.Events.GRAPH_LAYOUT);
            var layoutedNodes = algorithm(this._getNodeHierarchy());

            // center the top node on the currently visible canvas (if there's enough space)
            var centerX = Math.floor((jQuery('#' + this.config.IDs.CANVAS).width() / this.config.Grid.SIZE) / 2);
            // returned coordinates can be negative, so add that offset
            var minX = _.min(layoutedNodes, function(n) { return n.x }).x;
            centerX -= Math.min(centerX + minX, 0);

            // remember the node's positions before the layout attempt
            var oldPositions = _.map(layoutedNodes, function(n) {
                var node = this.getNodeById(n.id);
                return {x: node.x, y: node.y};
            }.bind(this));

            // apply layouted positions temporarily, without saving
            _.each(layoutedNodes, function(n) {
                var node = this.getNodeById(n.id);
                // +1 because the returned coords are 0-based and we need 1-based
                node.moveToGrid({x: n.x + centerX + 1, y: n.y + 1}, true);
            }.bind(this));

            // ask the user to keep the layout
            jQuery.when(Menus.LayoutMenu.keep())
                .fail(function() {
                    _.each(layoutedNodes, function(n, index) {
                        var node = this.getNodeById(n.id);
                        node.moveToGrid(oldPositions[index], true);
                    }.bind(this));
                }.bind(this))
                .always(function() {
                    jQuery(document).trigger(Config.Events.GRAPH_LAYOUTED);
                });

            return this;
        },

        /**
         * Group: Accessors
         */

        /**
         * Method: nodeClassFor
         *      Returns the {<Node>} class for the given kind. If the class does not yet exist it is created from the
         *      notation definition. It is an error if the given node kind does not exist in the notation.
         *
         * Parameters:
         *      {String} kind - The kind of the node class to be retrieved, e.g., 'basicEvent'.
         *
         *  Returns:
         *      The {<Class>} for the given kind.
         */
        nodeClassFor: function(kind) {
            var nodeClass = this._nodeClasses[kind];

            if (typeof nodeClass !== 'undefined') return nodeClass;

            var notationDefinition = this.getNotation().nodes[kind];
            if (typeof notationDefinition === 'undefined')
                throw TypeError('no definition for kind ' + kind);
            notationDefinition.kind = kind;

            return this._newNodeClassForKind(notationDefinition);
        },

        /**
         * Abstract Method: getNotation
         *
         * Returns:
         *      The notation definition for the graph.
         */
        getNotation: function() {
            throw new SubclassResponsibility();
        },

        /**
         * Abstract Method: getNodeClass
         *
         * Returns:
         *      The abstract {<Node>} class for all <Nodes> of this graph.
         */
        getNodeClass: function() {
            throw new SubclassResponsibility();
        },

        /**
         * Method: getNodes
         *
         * Returns:
         *      An {Array[<Node>]} containing all <Nodes> of the graph.
         *
         */
        getNodes: function() {
            return _.values(this.nodes);
        },

        /**
         * Method: getEdges
         *
         * Returns:
         *      An {Array[<Edge>]} containing all <Edges> of the graph.
         *
         */
        getEdges: function() {
            return _.values(this.edges);
        },

        /**
         * Method: getNodeById
         *
         * Parameters:
         *      {Number} nodeId - ID of the <Node> that should be returned.
         *
         * Returns:
         *      The {<Node>} with the given ID.
         */
        getNodeById: function(nodeId) {
            return this.nodes[nodeId];
        },

        /**
         * Method: getEdgeById
         *
         * Parameters:
         *      {Number} edgeId - ID of the edge that should be returned.
         *
         * Returns:
         *      The {<Edge>} instance with the given ID.
         */
        getEdgeById: function(edgeId) {
            return this.edges[edgeId];
        },

        /**
         * Abstract Method: getConfig
         *
         * Returns:
         *      The graph-specific <Config> object.
         */
        getConfig: function() {
            throw new SubclassResponsibility();
        },

        /**
         * Method: createId
         *
         * Returns:
         *      A {Number} representing a next unique ID for {<Edges>} or {<Nodes>}
         */
        createId: function() {
            return ++this.seed;
        },

        /**
         * Method: _getClusterLayoutAlgorithm
         *
         * Returns:
         *      The cluster layout algorithm supported by this graph.
         *
         */
        _getClusterLayoutAlgorithm: function() {
            return d3.layout
                .cluster()
                .nodeSize([1, 2]) // leave some space for the mirror
                .separation(function(a, b) {
                    // sibling nodes are tidier
                    return a.parent == b.parent ? 2 : 3;
                });
        },

        /**
         * Method: _getTreeLayoutAlgorithm
         *
         * Returns:
         *      The tree layouting algorithm supported by this graph.
         */
        _getTreeLayoutAlgorithm: function() {
            return d3.layout.tree()
                .nodeSize([1, 2]) // leave some space for the mirror
                .separation(function(a, b) {
                    // sibling nodes are tidier
                    return a.parent == b.parent ? 2 : 3;
                });
        },

        /**
         * Method: _getNodeHierarchy
         *
         *  Returns:
         *      A dictionary representation of the node hierarchy of this graph. Each entry represents a node with its
         *      ID and a list of children.
         */
        _getNodeHierarchy: function() {
            return this.getNodeById(0)._hierarchy();
        },


        /**
         * Group: Node class generation
         */

        /**
         *  Method: _newNodeClassForKind
         *      Constructs a new <Node> class from the given JSON node definition. It considers the inheritance relation
         *      specified in the definition and constructs the base classes (if not already done) as well. If no super
         *      class is specified, the base class returned by <getNodeClass> is used. Properties defined in the
         *      definition parameter will become members of the newly created class. Created classes will be cached in
         *      the <_nodeClasses> field so that they do not need to be regenerated every time.
         *
         *  Parameters:
         *      {Object} definition - Node definition taken from the graph-specific notation file.
         *
         *  Returns:
         *      The newly created {<Node>} {<Class>}.
         */
        _newNodeClassForKind: function(definition) {
            var BaseClass = this.factory.getClassModule('Node');
            var inherits = definition.inherits;

            if (inherits) {
                BaseClass = this.nodeClassFor(inherits);
            }

            var graph    = this;
            var newClass = BaseClass.extend({
                init: function(properties) {
                    this._super(jQuery.extend(true, {}, definition, properties));
                    _.each(this.allowConnectionTo, function(value, index) {
                        if (typeof value !== 'string') return;
                        this.allowConnectionTo[index] = graph.nodeClassFor(value);
                        this.inherits = BaseClass;
                    }.bind(this));
                }
            });

            newClass.toString = function() { return definition.nodeDisplayName; };
            this._nodeClasses[definition.kind] = newClass;

            return newClass;
        },

        /**
         * Group: Event handling
         */

        /**
         * Method: _shapeDropped
         *      Callback that gets called every time a new shape (from the <ShapeMenu>) is dropped on the <Canvas>. It
         *      will create a new <Node> of the corresponding kind at the drop location.
         *
         * Parameters:
         *      {jQuery::Event} event    - The event object passed by the jQuery event handling framework.
         *      {String}        kind     - The kind associated with the dropped shape, e.g., 'basicEvent'.
         *      {Object}        position - An object containing the pixel position of the dropped shape
         *                                 ({'x': ..., 'y': ...}).
         */
        _shapeDropped: function(event, kind, position) {
            var node = jQuery.extend(Canvas.toGrid(position), {'kind': kind});
            this.addNode(node)
                .container.click(); // emulate a click in order to select the new node
        }
    });
});
