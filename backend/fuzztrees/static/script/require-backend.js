define(function () {

    function Backend(baseURL) {
        this._baseURL = baseURL;
    }

    /*
        Function: createGraph
            Creates a new Graph in the backend. Will be asynchronous if a callback
            function was given

        Parameters:
            type     - Type of the Graph. See Config.Graph.Types.
            name     - Name of the Graph.
            callback - [optional] Callback function for asynchronous requests.
                       Will be called when the request returns with the ID of the
                       new Graph.

        Returns:
            The ID of the newly created Graph if no callback was given.
     */
    Backend.prototype.createGraph = function(type, name, callback) {

    }

    /*
         Function: getGraph
             Fetch a Graph object from the backend.

         Parameters:
             id       - ID of the Graph to fetch.
             callback - [optional] Callback function for asynchronous requests.
                        Will be called when the request returns with the fetched Graph object.

         Returns:
            The fetched Graph object.
     */
    Backend.prototype.getGraph = function(id, callback) {

    }

    /*
         Function: addNode
             Adds a new Node to a given Graph.

         Parameters:
             graph         - The Graph the node should be added to.
             type          - The type of the node. See Config.Node.Types
             parent        - The parent Node in the graph hierarchy.
             position      - Position object containing an 'x' and an 'y' field specifying the Node's position.
             errorCallback - [optional] Callback that gets called in case of an ajax-error.
     */
    Backend.prototype.addNode = function(graph, type, parent, position, errorCallback) {

    }

    /*
         Function: deleteNode
             Deletes a given Node in the backend.

         Parameters:
             node          - The Node that should be deleted.
             errorCallback - [optional] Callback that gets called in case of an ajax-error.
     */
    Backend.prototype.deleteNode = function(node, errorCallback) {

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

    }

    return Backend;
});