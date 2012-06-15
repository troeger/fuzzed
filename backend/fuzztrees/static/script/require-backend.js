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



    return Backend;
});