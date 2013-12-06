define(['canvas', 'class', 'jquery', 'd3'], function(Canvas, Class) {
    /**
     *  Package: Base
     */

    /**
     *  Class: Graph
     *
     *  This class models the _abstract_ base class for all graphs. It manages all graph elements (Edges and <Nodes>)
     *  and provide methods for adding and deleting them. Further it can generate <Node> classes
     *  for given kinds of nodes.
     */
    return Class.extend({
        /**
         *  Group: Members
         *
         *  Properties:
         *    {Config}  config      - An object containing graph configuration constants as found in <Config>.
         *    {int}     id          - A server-side generated ID.
         *    {Object}  edges       - A map that stores all edges of the graph by their ID. Edges are jsPlumb Connection
         *                            objects, the ID is the _fuzzedId assigned to them.
         *    {Object}  nodes       - A map that stores all <Nodes> of the graph by their ID.
         *    {str}     name        - The name of the graph, specified by the user when creating it.
         *    {Object} _nodeClasses - A map caching all node classes already generated and storing them by their kind.
         */
        config:       undefined,
        id:           undefined,
        edges:        {},
        nodes:        {},
        name:         undefined,
        readOnly:     undefined,

        _nodeClasses: {},

        /**
         *  Group: Initialization
         */

        /**
         *  Constructor: init
         *
         *  Parameters:
         *    {JSON} json - The JSON representation of the graph. This is usually fetched from the backend and used
         *                  to restore the graph in the frontend.
         */
        init: function(json) {
            this.id     = json.id;
            this.name   = json.name;
            this.config = this.getConfig();

            this._loadFromJson(json)
                ._registerEventHandlers()
                ._setupAutoLayout();
        },

        /**
         *  Method: _loadFromJson
         *    Extracts and restores the <Nodes> and edges from the given JSON representation of the graph.
         *
         *  Parameters:
         *    {JSON} json - The JSON representation of the graph, containing nodes and edges.
         *
         *  Returns:
         *    This <Graph> instance for chaining.
         */
        _loadFromJson: function(json) {
            this.readOnly = json.readOnly;

            var maxX = 0;
            var maxY = 0;

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

        /**
         *  Method: _registerEventHandlers
         *    Register on <Canvas> events in order to recognize shape drops and register to
         *    jsPlumb events in order to recognize connection events.
         *    This should be done _after_ the initial graph loading from the backend to avoid the creation
         *    of duplicate nodes/edges.
         *
         *  On:
         *    <Config::Events::CANVAS_SHAPE_DROPPED>
         *
         *  Returns:
         *    This <Graph> instance for chaining.
         */
        _registerEventHandlers: function() {
            jsPlumb.bind('jsPlumbConnection', function(edge) {
                this.addEdge(edge.connection);
            }.bind(this));

            jsPlumb.bind('jsPlumbConnectionDetached', function(edge) {
                this.deleteEdge(edge.connection);
            }.bind(this));

            jQuery(document).on(this.config.Events.CANVAS_SHAPE_DROPPED,   this._shapeDropped.bind(this));

            return this;
        },

        /**
         *  Method: _setupAutoLayout
         *    Sets up the toolbar entries for the layouting functions supported by this graph.
         *
         *  Returns:
         *    This <Graph> instance for chaining.
         */
        _setupAutoLayout: function() {
            var toolsContainer = jQuery('#' + this.config.IDs.NAVBAR_TOOLS);
            _.each(this._getLayoutAlgorithms(), function(algorithm) {
                jQuery('<a><i class="' + algorithm.iconClass + '"></i></a>')
                    .attr('title', algorithm.tooltip)
                    .on('click', function(){
                        this._layoutWithAlgorithm(algorithm.algorithm);
                    }.bind(this))
                    .appendTo(toolsContainer);
            }.bind(this));

            return this;
        },


        /**
         *  Group: Graph manipulation
         */

        /**
         *  Method: addEdge
         *    Adds a given edge to this graph. It will also assign a unique _fuzzedId to it and store it by this
         *    ID in the <edges> member.
         *
         *  Parameters:
         *    {jsPlumb::Connection} edge - Edge to be added to the graph.
         *
         *  Triggers:
         *    <Config::Events::GRAPH_EDGE_ADDED>
         *
         *  Returns:
         *    This <Graph> instance for chaining.
         */
        addEdge: function(edge) {
            if (typeof edge._fuzzedId === 'undefined') {
                edge._fuzzedId = new Date().getTime() + 1;
            }

            // store the ID in an attribute so we can retrieve it later from the DOM element
            jQuery(edge.canvas).attr(this.config.Attributes.CONNECTION_ID, edge._fuzzedId);

            var sourceNode = edge.source.data(this.config.Keys.NODE);
            var targetNode = edge.target.data(this.config.Keys.NODE);

            sourceNode.setChildProperties(targetNode);

            this.edges[edge._fuzzedId] = edge;

            sourceNode.outgoingEdges.push(edge);
            targetNode.incomingEdges.push(edge);

            jQuery(document).trigger(
                this.config.Events.GRAPH_EDGE_ADDED,
                [edge._fuzzedId,
                sourceNode.id,
                targetNode.id]
            );

            return this;
        },

        /**
         *  Method: deleteEdge
         *    Deletes the given edges from the graph if present.
         *
         *  Parameters:
         *    {jsPlumb::Connection} edge - Edge to be removed from this graph.
         *
         *  Triggers:
         *    <Config::Events::GRAPH_EDGE_DELETED>
         *
         *  Returns:
         *    This <Graph> instance for chaining.
         */
        deleteEdge: function(edge) {
            var id         = edge._fuzzedId;
            var sourceNode = edge.source.data(this.config.Keys.NODE);
            var targetNode = edge.target.data(this.config.Keys.NODE);

            sourceNode.restoreChildProperties(targetNode);

            sourceNode.outgoingEdges = _.without(sourceNode.outgoingEdges, edge);
            targetNode.incomingEdges = _.without(targetNode.incomingEdges, edge);

            jQuery(document).trigger(this.config.Events.GRAPH_EDGE_DELETED, id);
            delete this.edges[id];

            return this;
        },

        /**
         *  Method: addNode
         *    Adds a given node to this graph.
         *
         *  Parameters:
         *    {str}    kind       - The kind of the node, e.g., 'basicEvent'.
         *    {Object} properties - [optional] Properties that should be merged into the new node.
         *
         *  Triggers:
         *    <Config::Events::GRAPH_NODE_ADDED>
         *
         *  Returns:
         *    This <Graph> instance for chaining.
         */
        addNode: function(kind, properties) {
            properties.readOnly = this.readOnly;
            properties.graph    = this;

            var node = new (this.nodeClassFor(kind))(properties, this.getNotation().propertiesDisplayOrder);
            jQuery(document).trigger(this.config.Events.GRAPH_NODE_ADDED, [node.id, kind, node.x, node.y]);
            this.nodes[node.id] = node;

            return node;
        },

        /**
         *  Method: deleteNode
         *    Deletes the given node from the graph if present.
         *
         *  Parameters:
         *    {int} nodeId - ID of the <Node> that should be removed from this graph.
         *
         *  Triggers:
         *    <Config::Events::GRAPH_NODE_DELETED>
         *
         *  Returns:
         *    This <Graph> instance for chaining.
         */
        deleteNode: function(nodeId) {
            var node = this.nodes[nodeId];
            if (node.deletable === false) return this;

            _.each(_.union(node.incomingEdges, node.outgoingEdges), function(edge) {
                this.deleteEdge(edge);
            }.bind(this));

            node.remove();
            delete this.nodes[nodeId];

            jQuery(document).trigger(this.config.Events.GRAPH_NODE_DELETED, nodeId);

            return this;
        },

        /**
         *  Method: _layoutWithAlgorithm
         *    Layouts the nodes of this graph with the given layouting algorithm.
         *
         *  Returns:
         *    This <Graph> instance for chaining.
         */
        _layoutWithAlgorithm: function(algorithm) {
            var layoutedNodes = algorithm(this._getNodeHierarchy());
            var minX = _.min(layoutedNodes, function(n) {return n.x}).x;
            // apply positions
            _.each(layoutedNodes, function(n) {
                var node = this.getNodeById(n.id);
                node.moveToGrid({x: n.x - minX + 1, y: n.y + 1});
            }.bind(this));

            return this;
        },

        /**
         *  Group: Accessors
         */

        /**
         *  Method: nodeClassFor
         *    Returns the <Node> class for the given kind. If the class does not yet exist it is created from the
         *    notation definition. It is an error if the given node kind does not exist in the notation.
         *
         *  Parameters:
         *    {str} kind - The kind of the node class to be retrieved, e.g., 'basicEvent'.
         *
         *  Returns:
         *    The class for the given kind.
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
         *  Method: getNotation
         *    _Abstract_ method that returns the Notation object for the specific graph. Subclasses need to overwrite
         *    this method.
         *
         *  Returns:
         *    The Notation for the graph.
         */
        getNotation: function() {
            throw new SubclassResponsibility();
        },

        /**
         *  Method: getNodeClass
         *    _Abstract_ method that returns the class of the abstract base node that should be used by <Node>
         *    subclasses generated by this graph. Subclasses need to overwrite this method.
         *
         *  Returns:
         *    The abstract <Node> class for all <Nodes> of this graph.
         */
        getNodeClass: function() {
            throw new SubclassResponsibility();
        },

        /**
         *  Method: getNodes
         *
         *  Returns:
         *    An Array containing all <Nodes> of the graph.
         *
         */
        getNodes: function() {
            return _.values(this.nodes);
        },

        /**
         *  Method: getEdges
         *
         *  Returns:
         *    An Array containing all <Edges> of the graph.
         *
         */
        getEdges: function() {
            return _.values(this.edges);
        },

        /**
         *  Method: getNodeById
         *
         *  Parameters:
         *    {int} nodeId - ID of the <Node> that should be returned.
         *
         *  Returns:
         *    The <Node> with the given ID.
         */
        getNodeById: function(nodeId) {
            return this.nodes[nodeId];
        },

        /**
         *  Method: getEdgeById
         *
         *  Parameters:
         *    {int} edgeId - ID of the edge that should be returned.
         *
         *  Returns:
         *    The edge (<jsPlumb::Connection> object) with the given ID.
         */
        getEdgeById: function(edgeId) {
            return this.edges[edgeId];
        },

        /**
         *  Method: getConfig
         *    _Abstract_ method that returns the graph-specific <Config> object.
         *    Subclasses need to overwrite this method.
         *
         *  Returns:
         *    The graph-specific <Config> object.
         *
         *  See also:
         *    <Node::getConfig>
         */
        getConfig: function() {
            throw new SubclassResponsibility();
        },

        /**
         *  Method: _getLayoutAlgorithms
         *    Returns the layouting algorithms supported by this graph.
         *    This is the default implementation. Subclasses may override this behavior.
         *
         *  Returns:
         *    An array containing algorithm descriptions. Those descriptions should contain the algorithm itself
         *    (taken from d3.js), a class for the toolbar icon and a tooltip text.
         */
        _getLayoutAlgorithms: function() {
            var clusterLayout = d3.layout.cluster()
                .nodeSize([1, 2]) // leave some space for the mirror
                .separation(function(a, b) {
                    // sibling nodes are tidier
                    return a.parent == b.parent ? 2 : 3;
                });

            var treeLayout =  d3.layout.tree()
                .nodeSize([1, 2]) // leave some space for the mirror
                .separation(function(a, b) {
                    // sibling nodes are tidier
                    return a.parent == b.parent ? 2 : 3;
                });



            return [
                {
                    algorithm: clusterLayout,
                    iconClass: this.config.Classes.ICON_LAYOUT_CLUSTER,
                    tooltip:   this.config.Tooltips.LAYOUT_CLUSTER
                }, {
                    algorithm: treeLayout,
                    iconClass: this.config.Classes.ICON_LAYOUT_TREE,
                    tooltip:   this.config.Tooltips.LAYOUT_TREE
                }
            ];
        },

        /**
         *  Method: _getNodeHierarchy
         *    Returns a dictionary representation of the node hierarchy of this graph.
         *
         *  Returns:
         *    A dictionary representation of the node hierarchy of this graph. Each entry represents a node with
         *    its ID and a list of children.
         */
        _getNodeHierarchy: function() {
            return this.getNodeById(0)._hierarchy();
        },


        /**
         *  Group: Node class generation
         */

        /**
         *  Method: _newNodeClassForKind
         *    Constructs a new <Node> class from the given JSON node definition. It considers the inheritance relation
         *    specified in the definition and constructs the base classes (if not already done) as well. If no
         *    super class is specified, the base class returned by <getNodeClass> is used. Properties defined in the
         *    definition parameter will become members of the newly created class. Created classes will be cached
         *    in the <_nodeClasses> field so that they do not need to be regenerated every time.
         *
         *  Parameters:
         *    {JSON} definition - Node definition taken from the graph-specific notation file.
         *
         *  Returns:
         *    The newly created <Node> subclass.
         */
        _newNodeClassForKind: function(definition) {
            var BaseClass = this.getNodeClass();
            var inherits = definition.inherits;

            if (inherits) {
                BaseClass = this.nodeClassFor(inherits);
            }

            var graph    = this;
            var newClass = BaseClass.extend({
                init: function(properties, propertiesDisplayOrder) {
                    this._super(jQuery.extend(true, {}, definition, properties), propertiesDisplayOrder);
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
         *  Group: Event handling
         */

        /**
         *  Method: _shapeDropped
         *    Callback that gets called every time a new shape (from the <ShapeMenu>) is dropped on the <Canvas>.
         *    It will create a new <Node> of the corresponding kind at the drop location.
         *
         *  Parameters:
         *    {jQuery::Event} event    - The event object passed by the jQuery event handling framework.
         *    {str}           kind     - The kind associated with the dropped shape, e.g., 'basicEvent'.
         *    {Object}        position - An object containing the pixel position of the
         *                               dropped shape ({'x': ..., 'y': ...}).
         */
        _shapeDropped: function(event, kind, position) {
            this.addNode(kind, Canvas.toGrid(position))
                .container.click(); // emulate a click in order to select the new node
        }
    });
});
