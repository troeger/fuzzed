define(['faulttree/editor', 'fuzztree/graph', 'fuzztree/config'],
function(FaulttreeEditor, FuzztreeGraph, FuzztreeConfig) {

    /**
     * Class: FaultTreeEditor
     */
    return FaulttreeEditor.extend({
        getConfig: function() {
            return FuzztreeConfig;
        },

        getGraphClass: function() {
            return FuzztreeGraph;
        }
    });
});
