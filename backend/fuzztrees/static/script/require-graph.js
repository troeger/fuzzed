define(['require-config'], function(Config) {

    function Graph(id) {
        this.id     = id;
        this._nodes = {};
        this._edges = {};
    }

     /*
        Function: addEdge
            Adds a given edge to this graph.

        Parameters:
            edge - Edge to be added
     */
    Graph.prototype.addEdge = function(edge) {
        this._edges[edge.id] = edge;
    }

    /*
        Function: addNode
            Adds a given node to this graph.

        Parameters:
            node - Node to add to this graph.
     */
    Graph.prototype.addNode = function(node) {
        node.graph(this);
        this._nodes[node.id] = node;
    }

    /*
        Function: deleteEdge
            Deletes the given edges from the graph if present

        Parameters:
            edge - Edge to remove from this graph.
     */
    Graph.prototype.deleteEdge = function(edge) {
        delete this._edges[edge.id];
    }

    /*
        Function: deleteNode
            Deletes the given node from the graph if present

        Parameters:
            node - Node to remove from this graph.
     */
    Graph.prototype.deleteNode = function(node) {
        delete this._nodes[node.id]
    }

    Graph.prototype.getNodeById = function(id) {
        return this._nodes[id];
    }

    /*
        Function: getNodes
            Get all the nodes of the graph.
     */
    Graph.prototype.getNodes = function() {
        return _.values(this._nodes);
    }

    return Graph;
});
