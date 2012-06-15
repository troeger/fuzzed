define(['require-config', 'require-nodes'], function (Config, Nodes) {

    var URLHelper = {
        fullUrlForGraphs: function() {
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL;
        },

        fullUrlForGraph: function(graphID) {
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL + '/' + graphID;
        },

        fullUrlForNodes: function(graph) {
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL + '/'
                + graph().id() + Config.Backend.NODES_URL;
        }

        fullUrlForNode: function(node) {
            return Config.Backend.BASE_URL + Config.Backend.GRAPHS_URL + '/'
                + node.graph().id() + Config.Backend.NODES_URL + '/' + node.id();
        }
    }


    function Backend() {
    }

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
    Backend.prototype.createGraph = function(type, name, callback, errorCallback) {
        var url = URLHelper.fullUrlForGraphs();
        var data = {
            'type': type,
            'name': name
        };
        var ajaxCallback = function(data) {
            //TODO: Fetch graph ID. Maybe returning the graph URL in the backend is not a good idea.
            console.log(data);
        };

        jQuery.post(url, data, ajaxCallback).fail(errorCallback || jQuery.noop);
    }

    /*
         Function: getGraph
             Fetch a Graph object from the backend.

         Parameters:
             id            - ID of the Graph to fetch.
             callback      - [optional] Callback function for asynchronous requests.
                             Will be called when the request returns with the fetched Graph object.
             errorCallback - [optional] Callback that gets called in case of an ajax-error.

         Returns:
            The fetched Graph object.
     */
    Backend.prototype.getGraph = function(id, callback, errorCallback) {
        var url = URLHelper.fullUrlForGraph(id)
        var ajaxCallback = function(json) {
            //TODO: Figure format
            console.log(data);
        };

        jQuery.getJSON(url, ajaxCallback).fail(errorCallback || jQuery.noop);
    }

    /*
         Function: addNode
             Adds a new Node to a given Graph.

         Parameters:
             graph         - The Graph the node should be added to.
             type          - The type of the node. See Config.Node.Types
             parent        - [optional] The parent Node in the graph hierarchy.
             position      - Position object containing an 'x' and an 'y' field specifying the Node's position.
             errorCallback - [optional] Callback that gets called in case of an ajax-error.
     */
    Backend.prototype.addNode = function(graph, type, parent, position, errorCallback) {
        var url = URLHelper.fullUrlForNodes(graph);
        var data = {
            'type': type,
            'xcoord': position.x,
            'ycoord': position.y
        };
        //TODO: see if this works with require
        if (parent instanceof Node) data['parent'] = parent.id();
        var ajaxCallback = function(data) {
            //TODO: Fetch node ID. Maybe returning the graph URL in the backend is not a good idea.
            console.log(data);
        };

        jQuery.post(url, data, ajaxCallback).fail(errorCallback || jQuery.noop);
    }

    /*
         Function: deleteNode
             Deletes a given Node in the backend.

         Parameters:
             node          - The Node that should be deleted.
             errorCallback - [optional] Callback that gets called in case of an ajax-error.
     */
    Backend.prototype.deleteNode = function(node, errorCallback) {
        var url = URLHelper.fullUrlForNode(node);

        jQuer.ajax({
            type: 'DELETE',
            url:  url
        }).fail(errorCallback || jQuery.noop);
    }

    /*
         Function: relinkNode
             Links the given Node to a new parent Node.

         Parameters:
             node          - The Node that should be deleted.
             newParent     - The new parent Node in the graph hierarchy.
             errorCallback - [optional] Callback that gets called in case of an ajax-error.
     */
    Backend.prototype.relinkNode = function(node, newParent, errorCallback) {
        var url = URLHelper.fullUrlForNode(node);
        var data = {
            'parent': newParent,
            //TODO: why?
            'xcoord': node.position().x,
            'ycoord': node.position().y
        }

        jQuery.post(url, data).fail(errorCallback || jQuery.noop);
    }

    /*
         Function: changeNodeProperty
             Changes a property of a given Node.

         Parameters:
             node          - The Node that should be deleted.
             key           - The name of the property.
             value         - The new value for the property.
             errorCallback - [optional] Callback that gets called in case of an ajax-error.
     */
    Backend.prototype.changeNodeProperty = function(node, key, value, errorCallback) {
        var url = URLHelper.fullUrlForNode(node);
        var data = {
            'key': key,
            'value': value
        }

        jQuery.post(url, data).fail(errorCallback || jQuery.noop);
    }

    /*
         Function: changeNodePosition
             Changes the position of a given Node.

         Parameters:
             node          - The Node that should be deleted.
             position      - New position object (with 'x' and 'y' fields) of the node.
             errorCallback - [optional] Callback that gets called in case of an ajax-error.
     */
    Backend.prototype.changeNodePosition = function(node, position, errorCallback) {
        var url = URLHelper.fullUrlForNode(node);
        var data = {
            'xcoord': position.x,
            'ycoord': position.y
        }

        jQuery.post(url, data).fail(errorCallback || jQuery.noop);
    }

    /*
         Function: changeNodeType
             Changes the type of a given Node.

         Parameters:
             node          - The Node that should be deleted.
             newType       - The new type of the node. See Config.Node.Types
             errorCallback - [optional] Callback that gets called in case of an ajax-error.
     */
    Backend.prototype.changeNodeType = function(node, newType, errorCallback) {
        var url = URLHelper.fullUrlForNode(node);
        var data = {
            'type': newType
        }

        jQuery.post(url, data).fail(errorCallback || jQuery.noop);
    }

    return Backend;
});