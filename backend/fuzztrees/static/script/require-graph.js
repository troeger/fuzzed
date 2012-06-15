define(['require-config'], function(Config) {

    function Graph(id) {
        this._id = id;
        this._nodes = [];
        this._edges = [];
    }

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
        node._graph = this;
    }


    return Graph;
});
