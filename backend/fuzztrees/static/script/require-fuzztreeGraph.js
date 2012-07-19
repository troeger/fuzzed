define(['require-graph', 'require-oop'], function(Graph) {

    function FuzztreeGraph(id) {
        FuzztreeGraph.Super.constructor.call(this, id);
    }

    FuzztreeGraph.Extends(Graph);

    return FuzztreeGraph;
});
