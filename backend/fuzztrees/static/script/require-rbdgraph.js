define(['require-graph', 'require-oop'], function(Graph) {

    function RBDGraph(id) {
        RBDGraph.Super.constructor.call(this, id);
    }

    RBDGraph.Extends(Graph);

    return RBDGraph;
});
