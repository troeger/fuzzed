define(['factory', 'faulttree/editor', 'fuzztree/graph', 'fuzztree/config', 'fuzztree/node'],
function(Factory, FaulttreeEditor, FuzztreeGraph, FuzztreeConfig) {
    /**
     * Package: Fuzztree
     */

    /**
     * Class: FuzztreeEditor
     *      Fuzztree-specific <Base::Editor> class.
     *
     * Extends: <Faulttree::FaultTreeEditor>
     */
    return FaulttreeEditor.extend({
        init: function(graphId) {
            Factory.kind = 'fuzztree';
            this._super(graphId);
        }
    });
});
