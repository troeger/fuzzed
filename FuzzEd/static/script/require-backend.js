define(['require-config', 'require-graph'], function (Config, Graph) {

    var URLHelper = {
        fullUrlForGraphs: function() {
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL;
        },

        fullUrlForGraph: function(graphID) {
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL + '/' + graphID;
        },

        fullUrlForNodes: function(graph) {
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL + '/'
                + graph.id + Config.Backend.NODES_URL;
        },

        fullUrlForNode: function(node) {
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL + '/'
                + node.graph().id + Config.Backend.NODES_URL + '/' + node.id;
        },

        fullUrlForEdges: function(graph) {
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL + '/' + graph.id + Config.Backend.EDGES_URL;
        },

        fullUrlForEdge: function(edge) {
            var graph = edge.source.data(Config.Keys.NODE).graph;
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL + '/' + graph.id
                + Config.Backend.EDGES_URL + '/' + edge._fuzzedID;
        }
    }

    var Backend = {}

    /*
     Function: addEdge
        Adds a new edge from a given source node to a given target node.

     Parameters:
        sourceNode - Source node of the new edge.
        targetNode - Target node of the new edge.
        success    - [optional] Will be called when the request was successful. Provides e.g. the ID of the new edge.
        error      - [optional] Callback that gets called in case of an ajax-error.
        complete   - [optional] Callback that is invoked in both cases - a successful or an erroneous ajax request
     */
    Backend.addEdge = function(edgeID, sourceNode, targetNode, success, error, complete) {
        var url = URLHelper.fullUrlForEdges(sourceNode.graph());
        var data = {
            id:          edgeID,
            source:      sourceNode.id,
            destination: targetNode.id
        };

        jQuery.ajax({
            url:      url,
            type:     'POST',
            dataType: 'json',

            data:     data,
            success:  success  || jQuery.noop,
            error:    error    || jQuery.noop,
            complete: complete || jQuery.noop
        });
    }

    /*
         Function: addNode
             Adds a new node to the backend of this graph.

         Parameters:
             node     - The node object
             success  - [optional] Will be called on successful node creation transmission to server
             error    - [optional] Callback that gets called in case of an ajax-error.
             complete - [optional] Callback that is invoked when the ajax request completes successful or erroneous
     */
    Backend.addNode = function(node, success, error, complete) {
        var url = URLHelper.fullUrlForNodes(node.graph());
        var data = {
            id:         node.id,
            kind:       node.kind,
            x:          node.x,
            y:          node.y
        };

        var successCallback = function(json) {
            //XXX: improve this later (send properties already in data)
            //TODO: remove
            _.each(node.properties(), function(property) {
                Backend.changeProperty(node, property.name(), property.value());
            });
            if (success) success(json);
        }

        jQuery.ajax({
            url:      url,
            type:     'POST',
            dataType: 'json', 

            data:     data, 
            success:  successCallback,
            error:    error    || jQuery.noop,
            complete: complete || jQuery.noop
        });
    }

    /*
     Function: deleteEdge
     Deletes a given edge in the backend.

     Parameters:
     edge     - The edge that should be deleted.
     success  - [optional] Function that is invoked when the ajax request was successful
     error    - [optional] Callback that gets called in case of an ajax-error.
     complete - [optional] Callback that gets invoked in both cases - a successful and an errornous ajax-call.
     */
    Backend.deleteEdge = function(edge, success, error, complete) {
        var url = URLHelper.fullUrlForEdge(edge);

        jQuery.ajax({
            url:      url,
            type:     'DELETE',
            dataType: 'json',

            success:  success  || jQuery.noop,
            error:    error    || jQuery.noop,
            complete: complete || jQuery.noop
        });
    }

    /*
         Function: deleteNode
             Deletes a given node in the backend.

         Parameters:
             node     - The node that should be deleted.
             succes   - [optional] Callback that is being called on successful deletion on backend.
             error    - [optional] Callback that gets called in case of an ajax-error.
             complete - [optional] Callback that is invoked in both cases either in an successful or errornous ajax call.
     */
    Backend.deleteNode = function(node, success, error, complete) {
        var url = URLHelper.fullUrlForNode(node);

        jQuery.ajax({
            url:      url,
            type:     'DELETE',
            dataType: 'json',

            success:  success  || jQuery.noop,
            error:    error    || jQuery.noop,
            complete: complete || jQuery.noop
        });
    }

    /*
         Function: getGraph
             Fetch a Graph object from the backend.

         Parameters:
             id       - ID of the Graph to fetch.
             success  - [optional] Callback function for a successful asynchronous request for json representing a graph with given id.
             error    - [optional] Callback that gets called in case of an unsuccessful retrieval of the graph from
                        the database. Will create a new graph in the backend anyway.
             complete - [optional] Callback that gets invoked in either a successful or erroneous graph request.
     */
    Backend.getGraph = function(id, success, error, complete) {
        var url = URLHelper.fullUrlForGraph(id);

        var successCallback = function(json) {
            // call the passed success function if present
            if (success) success(json);
        };

        var errorCallback = function(response, textStatus, errorThrown) {
            // TODO: do proper create graph here on backend
            var graph = new Graph(id);
            if (error) error(graph, response, textStatus, errorThrown);
        }

        jQuery.ajax({
            url:      url,
            dataType: 'json',

            success:  successCallback,
            error:    errorCallback,
            complete: complete || jQuery.noop
        });
    }

    /*
         Function: changeNode
             Changes the properties of a given node.

         Parameters:
             node       - The node that shall be moved
             properties - The node's properties that should be changed
             success    - [optional] Function that is invoked when the node's move was successfully transmitted.
             error      - [optional] Callback that gets called in case of an ajax-error.
             complete   - [optional] Callback that is always invoked no matter if ajax request was successful or erroneous.
     */
    Backend.changeNode = function(node, properties, success, error, complete) {
        var url = URLHelper.fullUrlForNode(node);

        jQuery.ajax({
            url:      url,
            type:     'POST',
            dataType: 'json',

            data:     properties,
            success:  success  || jQuery.noop,
            error:    error    || jQuery.noop,
            complete: complete || jQuery.noop
        });
    }

    /* TODO From here on*/

    /*
        Function: createGraph
            Creates a new Graph in the backend. Will be asynchronous if a callback
            function was given

        Parameters:
            type          - Type of the Graph. See Config.Graph.Types.
            name          - Name of the Graph.
            callback      - Callback function for asynchronous requests.
                            Will be called when the request returns with the ID of the
                            new Graph.
            errorCallback - [optional] Callback that gets called in case of an ajax-error.
     */
    Backend.createGraph = function(type, name, callback, errorCallback) {
        var url = URLHelper.fullUrlForGraphs();
        var data = {
            'type': type,
            'name': name
        };
        var ajaxCallback = function(data) {
            //TODO: Fetch graph ID.
            console.log(data);
        };

        jQuery.post(url, data, ajaxCallback).fail(errorCallback || jQuery.noop);
    }

    return Backend;
});