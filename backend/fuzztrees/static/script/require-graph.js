define(['require-config'], function(Config) {

    function Graph(id) {
        this._id    = id;
        this._nodes = [];
        this._edges = [];
    }

    /*
        Function: id
            Retrieves the id of the graph
     */
    Graph.prototype.id = function() {
        return this._id;
    }

    /*
        Function: addNode
            Adds a given node to this graph.

        Parameters:
            node - Node to add to this graph.
     */
    Graph.prototype.addNode = function(node) {
        this._nodes.push(node);
    }

    /*
        Function: getNodes
            Get all the nodes of the graph.
     */
    Graph.prototype.getNodes = function() {
        return this._nodes;
    }

    return Graph;
});
