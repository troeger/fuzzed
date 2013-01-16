define(['class', 'config'], function (Class, Config) {
    return Class.extend({
        _graphId: undefined,

        init: function(graphId) {
            this._graphId = graphId;
        },

        activate: function() {
            jQuery(document)
                .on(Config.Events.NODE_PROPERTY_CHANGED,    this.nodePropertyChanged.bind(this))
                .on(Config.Events.GRAPH_NODE_ADDED,         this.graphNodeAdded.bind(this))
                .on(Config.Events.GRAPH_NODE_DELETED,       this.graphNodeDeleted.bind(this))
                .on(Config.Events.GRAPH_EDGE_ADDED,         this.graphEdgeAdded.bind(this))
                .on(Config.Events.GRAPH_EDGE_DELETED,       this.graphEdgeDeleted.bind(this))
                .on(Config.Events.EDITOR_CALCULATE_CUTSETS, this.calculateCutsets.bind(this));

            return this;
        },

        deactivate: function() {
            jQuery(document)
                .off(Config.Events.NODE_PROPERTY_CHANGED)
                .off(Config.Events.GRAPH_NODE_ADDED)
                .off(Config.Events.GRAPH_NODE_DELETED)
                .off(Config.Events.GRAPH_EDGE_ADDED)
                .off(Config.Events.GRAPH_EDGE_DELETED)
                .off(Config.Events.EDITOR_CALCULATE_CUTSETS);

            return this;
        },

        /*
         Function: graphEdgeAdded
            Adds a new edge from a given source node to a given target node.

         Parameters:
             edgeId       - ID of the edge.
             sourceNodeId - Source node of the new edge.
             targetNodeId - Target node of the new edge.
             success      - [optional] Will be called when the request was successful. Provides e.g. the ID of the new edge.
             error        - [optional] Callback that gets called in case of an ajax-error.
             complete     - [optional] Callback that is invoked in both cases - a successful or an erroneous ajax request
         */
        graphEdgeAdded: function(event, edgeId, sourceNodeId, targetNodeId, success, error, complete) {
            var data = {
                id:          edgeId,
                source:      sourceNodeId,
                destination: targetNodeId
            };

            jQuery.ajax({
                url:      this._fullUrlForEdges(),
                type:     'POST',
                dataType: 'json',

                data:     data,
                success:  success  || jQuery.noop,
                error:    error    || jQuery.noop,
                complete: complete || jQuery.noop
            });

            return this;
        },

        /*
             Function: graphNodeAdded
                 Adds a new node to the backend of this graph.

             Parameters:
                 nodeId   - The node ID.
                 kind     - The node kind.
                 success  - [optional] Will be called on successful node creation transmission to server.
                 error    - [optional] Callback that gets called in case of an ajax-error.
                 complete - [optional] Callback that is invoked when the ajax request completes successful or erroneous.
         */
        graphNodeAdded: function(event, nodeId, kind, x, y, success, error, complete) {
            var data = {
                id:   nodeId,
                kind: kind,
                x:    x,
                y:    y
            };

            jQuery.ajax({
                url:      this._fullUrlForNodes(),
                type:     'POST',
                dataType: 'json',

                data:     data,
                success:  success  || jQuery.noop,
                error:    error    || jQuery.noop,
                complete: complete || jQuery.noop
            });

            return this;
        },

        /*
         Function: graphEdgeDeleted
             Deletes a given edge in the backend.

         Parameters:
             edgeId   - The ID of the edge that should be deleted.
             success  - [optional] Function that is invoked when the ajax request was successful
             error    - [optional] Callback that gets called in case of an ajax-error.
             complete - [optional] Callback that gets invoked in both cases - a successful and an errornous ajax-call.
         */
        graphEdgeDeleted: function(event, edgeId, success, error, complete) {
            jQuery.ajax({
                url:      this._fullUrlForEdge(edgeId),
                type:     'DELETE',
                dataType: 'json',

                success:  success  || jQuery.noop,
                error:    error    || jQuery.noop,
                complete: complete || jQuery.noop
            });

            return this;
        },

        /*
         Function: graphNodeDeleted
             Deletes a given node in the backend.

         Parameters:
             nodeId   - The ID of the node that should be deleted.
             succes   - [optional] Callback that is being called on successful deletion on backend.
             error    - [optional] Callback that gets called in case of an ajax-error.
             complete - [optional] Callback that is invoked in both cases either in an successful or errornous ajax call.
         */
        graphNodeDeleted: function(event, nodeId, success, error, complete) {
            jQuery.ajax({
                url:      this._fullUrlForNode(nodeId),
                type:     'DELETE',
                dataType: 'json',

                success:  success  || jQuery.noop,
                error:    error    || jQuery.noop,
                complete: complete || jQuery.noop
            });

            return this;
        },

        /*
         Function: nodePropertyChanged
             Changes the properties of a given node.

         Parameters:
             nodeId     - The node that shall be moved
             properties - The node's properties that should be changed
             success    - [optional] Function that is invoked when the node's move was successfully transmitted.
             error      - [optional] Callback that gets called in case of an ajax-error.
             complete   - [optional] Callback that is always invoked no matter if ajax request was successful or erroneous.
         */
        nodePropertyChanged: function(event, nodeId, properties, success, error, complete) {
            jQuery.ajax({
                url:      this._fullUrlForNode(nodeId),
                type:     'POST',
                data:{
                    properties: JSON.stringify(properties)
                },
                dataType: 'json',

                success:  success  || jQuery.noop,
                error:    error    || jQuery.noop,
                complete: complete || jQuery.noop
            });

            return this;
        },

        /*
         Function: getGraph
             Fetch a Graph object from the backend.

         Parameters:
             success  - [optional] Callback function for a successful asynchronous request for json representing a graph with given id.
             error    - [optional] Callback that gets called in case of an unsuccessful retrieval of the graph from
                        the database. Will create a new graph in the backend anyway.
             complete - [optional] Callback that gets invoked in either a successful or erroneous graph request.
         */
        getGraph: function(success, error, complete) {
            jQuery.ajax({
                url:      this._fullUrlForGraph(),
                dataType: 'json',

                success:  success  || jQuery.noop,
                error:    error    || jQuery.noop,
                complete: complete || jQuery.noop
            });

            return this;
        },

        /*
             Function: calculateCutsets
                 Tells the server to calculate the minimal cutsets for the given graph and passes
                 the results to the provided callback.

             Parameters:
                 success  - [optional] Callback function for asynchronous requests.
                            Will be called when the request returns with the cutsets.
                 error    - [optional] Callback that gets called in case of an error.
                 complete - [optional] Callback that gets invoked in either a successful or erroneous request.
         */
        calculateCutsets: function(event, success, error, complete) {
            jQuery.ajax({
                url:      this._fullUrlForCutsets(),
                dataType: 'json',

                success:  success  || jQuery.noop,
                error:    error    || jQuery.noop,
                complete: complete || jQuery.noop
            });

            return this;
        },

        /* Section: Internal */

        /* Section: Helper */

        _fullUrlForGraph: function() {
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL + '/' + this._graphId;
        },

        _fullUrlForNodes: function() {
            return this._fullUrlForGraph() + Config.Backend.NODES_URL;
        },

        _fullUrlForNode: function(nodeId) {
            return this._fullUrlForNodes() + '/' + nodeId;
        },

        _fullUrlForEdges: function() {
            return this._fullUrlForGraph() + Config.Backend.EDGES_URL;
        },

        _fullUrlForEdge: function(edgeId) {
            return this._fullUrlForEdges() + '/' + edgeId;
        },

        _fullUrlForCutsets: function() {
            return this._fullUrlForGraph() + Config.Backend.CUTSETS_URL;
        }
    });
});
