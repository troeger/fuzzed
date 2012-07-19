define(['require-graph', 'require-oop'], function(Graph) {

    function FaulttreeGraph(id) {
        FaulttreeGraph.Super.constructor.call(this, id);
    }

    FaulttreeGraph.Extends(Graph);

    return FaulttreeGraph;
});
