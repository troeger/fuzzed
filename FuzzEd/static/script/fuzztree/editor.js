define(['faulttree/editor', 'fuzztree/graph'],
function(FaulttreeEditor, FuzztreeGraph) {

    /**
     * Class: FaultTreeEditor
     */
    return FaulttreeEditor.extend({
        _graphClass: function() {
            return FuzztreeGraph;
        }
    });
});
