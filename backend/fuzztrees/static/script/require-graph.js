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
        node.graph(this);
        this._nodes.push(node);
    }

    /*
        Function: deleteNode
            Deletes the given node from the graph if present

        Parameters:
            node - Node to remove from this graph.
     */
    Graph.prototype.deleteNode = function(node) {
        this._nodes = _.without(this._nodes, node);
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
