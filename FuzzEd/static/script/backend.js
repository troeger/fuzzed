define(['class', 'config', 'job'], function (Class, Config, Job) {
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
                .on(Config.Events.EDITOR_CALCULATE_CUTSETS, this.calculateCutsets.bind(this))
                .on(Config.Events.EDITOR_CALCULATE_TOPEVENT_PROBABILITY, this.calculateTopeventProbability.bind(this));
        },

        deactivate: function() {
            jQuery(document)
                .off(Config.Events.NODE_PROPERTY_CHANGED)
                .off(Config.Events.GRAPH_NODE_ADDED)
                .off(Config.Events.GRAPH_NODE_DELETED)
                .off(Config.Events.GRAPH_EDGE_ADDED)
                .off(Config.Events.GRAPH_EDGE_DELETED)
                .off(Config.Events.EDITOR_CALCULATE_CUTSETS)
                .off(Config.Events.EDITOR_CALCULATE_TOPEVENT_PROBABILITY);
        },

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
        },
        /*
         Function: graphEdgeAdded
         Adds a new edge from a given source node to a given target node.

         Parameters:
         edgeId       - ID of the edge.
         sourceNodeId - Source node of the new edge.
         targetNodeId - Target node of the new edge.
         success      - [optional] Function that is invoked when the ajax request was successful.
         error        - [optional] Callback that gets called in case of an ajax-error.
         complete     - [optional] Callback that gets invoked in both cases - a successful and an erroneous ajax-call.
         */

        /*
         Function: graphNodeAdded
             Adds a new node to the backend of this graph.

         Parameters:
             nodeId   - The node ID.
             kind     - The node kind.
             success  - [optional] Function that is invoked when the ajax request was successful.
             error    - [optional] Callback that gets called in case of an ajax-error.
             complete - [optional] Callback that gets invoked in both cases - a successful and an erroneous ajax-call.
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
        },

        /*
         Function: graphEdgeDeleted
             Deletes a given edge in the backend.

         Parameters:
             edgeId   - The ID of the edge that should be deleted.
             success  - [optional] Function that is invoked when the ajax request was successful.
             error    - [optional] Callback that gets called in case of an ajax-error.
             complete - [optional] Callback that gets invoked in both cases - a successful and an erroneous ajax-call.
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
        },

        /*
         Function: graphNodeDeleted
             Deletes a given node in the backend.

         Parameters:
             nodeId   - The ID of the node that should be deleted.
             success  - [optional] Function that is invoked when the ajax request was successful.
             error    - [optional] Callback that gets called in case of an ajax-error.
             complete - [optional] Callback that gets invoked in both cases - a successful and an erroneous ajax-call.
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
        },

        /*
         Function: nodePropertyChanged
             Changes the properties of a given node.

         Parameters:
             nodeId     - The node that shall be moved.
             properties - The node's properties that should be changed.
             success    - [optional] Function that is invoked when the ajax request was successful.
             error      - [optional] Callback that gets called in case of an ajax-error.
             complete   - [optional] Callback that gets invoked in both cases - a successful and an erroneous ajax-call.
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
        },

        /*
         Function: getGraph
             Fetch a graph object from the backend as json.

         Parameters:
             success  - [optional] Function that is invoked when the ajax request was successful.
             error    - [optional] Callback that gets called in case of an ajax-error.
             complete - [optional] Callback that gets invoked in both cases - a successful and an erroneous ajax-call.
         */
        getGraph: function(success, error, complete) {
            jQuery.ajax({
                url:      this._fullUrlForGraph(),
                dataType: 'json',

                success:  success  || jQuery.noop,
                error:    error    || jQuery.noop,
                complete: complete || jQuery.noop
            });
        },

        /*
         Function: calculateCutsets
             Tells the server to calculate the minimal cutsets for the given graph and passes the results to the
             provided callback.

         Parameters:
             success  - [optional] Function that is invoked when the ajax request was successful.
             error    - [optional] Callback that gets called in case of an ajax-error.
             complete - [optional] Callback that gets invoked in both cases - a successful and an erroneous ajax-call.
         */
        calculateCutsets: function(event, success, error, complete) {
            jQuery.ajax({
                url:      this._fullUrlForCutsets(),
                dataType: 'json',

                success:  success  || jQuery.noop,
                error:    error    || jQuery.noop,
                complete: complete || jQuery.noop
            });
        },

        /**
         *  Method: calculateTopeventProbability
         *    Tell the backend to calculate the probability of the top event. This is an asynchronous request, i.e. the
         *    success callback will get a <Job> object it can use to receive the final result.
         *
         *  Parameters:
         *    {Function} success  - [optional] Callback function that will receive the <Job> object if the job submission
         *                          was successful.
         *    {Function} error    - [optional] Callback that gets called in case of an error.
         *    {Function} complete - [optional] Callback that gets invoked in either a successful or erroneous request.
         */
        calculateTopeventProbability: function(event, success, error, complete) {
            jQuery.ajax({
                url:      this._fullUrlForTopeventProbability(),
                dataType: 'json',

                statusCode: {
                    201: function(data, status, req) {
                        var jobUrl = req.getResponseHeader('location');
                        if (typeof success !== 'undefined') {
                            success(new Job(jobUrl));
                        }
                    }
                },

                error:    error    || jQuery.noop,
                complete: complete || jQuery.noop
            });
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
        },

        _fullUrlForTopeventProbability: function() {
            return this._fullUrlForGraph() + Config.Backend.TOPEVENT_PROBABILITY_URL;
        }
    });
});
